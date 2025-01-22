from SemanticAnalyzer.annotated_tree import AnnotatedTreeNode
from Parser.parser import parser
from Scanner.minijavaplus import MiniJava
from SemanticAnalyzer.attributes import Attributes
from SemanticAnalyzer.symbol_table import SymbolTable

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.attributes = Attributes(self.symbol_table)

    def analyze(self, source_file):
        """
        Realiza a análise semântica a partir do arquivo fonte.
        :param source_file: Caminho para o arquivo fonte em MiniJava.
        """
        ast = parser(MiniJava.run(source_file))

        if ast is None:
            print("ERRO: A árvore de sintaxe não foi gerada corretamente.")
            return None

        self.process_PROG(ast)
        annotated_ast = self.annotate_tree(ast)

        return annotated_ast


    def annotate_tree(self, parse_node):
        """Função recursiva que converte a árvore do parser para a árvore semântica anotada."""
        if parse_node is None:
            return None

        token = parse_node.token
        lexeme = parse_node.lexeme
        literal = parse_node.literal

        annotated_node = AnnotatedTreeNode(
            token=token,
            semantic_type=None,
            lexeme=lexeme,
            literal=literal
        )

        for child in parse_node.children:
            annotated_child = self.annotate_tree(child)
            annotated_node.add_child(annotated_child)

        return annotated_node

    def process_PROG(self, prog):
        main = prog.children('main')  
        if main:
            self.process_MAIN(main)
        
        for classe in prog.children:
            if classe.token == 'class':  
                self.process_CLASSE(classe)
        
        if main:
            prog.semantic_type = main.semantic_type

    def process_MAIN(self, main):
        if self.symbol_table.is_class_declared(main.lexeme):
            raise Exception(f"Erro: Classe '{main.lexeme}' já declarada.")
        
        self.symbol_table.add_class(main.lexeme)
        main.semantic_type = "volexeme"
        self.process_CMD(main.children('cmd'))

    def process_CLASSE(self, classe):
        if self.symbol_table.is_class_declared(classe.lexeme):
            raise Exception(f"Erro: Classe '{classe.lexeme}' já declarada.")
        self.symbol_table.add_class(classe.lexeme)
        
        if classe.children('extends') and not self.symbol_table.is_class_declared(classe.children('extends').lexeme):
            raise Exception(f"Erro: Classe base '{classe.extends}' não declarada.")
        
        for var in classe.children:
            if var.token == 'var':
                self.attributes.process_VAR(var)
        
        for metodo in classe.children:
            if metodo.token == 'method':
                self.process_METODO(metodo)

    def process_METODO(self, metodo):
        if self.symbol_table.is_method_declared(metodo.lexeme):
            raise Exception(f"Erro: Método '{metodo.lexeme}' já declarado.")
        self.symbol_table.add_method(metodo.lexeme, metodo.semantic_type, metodo.params)

        for param in metodo.children:
            if param.token == 'param' and self.symbol_table.is_variable_declared(param.lexeme):
                raise Exception(f"Erro: Parâmetro '{param.lexeme}' já declarado no escopo.")
            self.symbol_table.add_variable(param.lexeme, param.semantic_type)

        for var in metodo.children:
            if var.token == 'var':
                self.attributes.process_VAR(var)

        for cmd in metodo.children:
            if cmd.token == 'cmd':
                self.process_CMD(cmd)

        if metodo.children('return_expr'):
            return_type = self.attributes.process_EXP(metodo.children('return_expr'))
            if return_type != metodo.semantic_type:
                raise Exception(f"Erro: tipo de retorno incompatível no método '{metodo.lexeme}'.")

    def process_CMD(self, cmd):
        if cmd.token == "assign":
            if not self.symbol_table.is_variable_declared(cmd.children('var').lexeme):
                raise Exception(f"Erro: Variável '{cmd.var}' não declarada.")
            var_type = self.symbol_table.get_variable_type(cmd.var)
            expr_type = self.attributes.process_EXP(cmd.expr)
            if var_type != expr_type:
                raise Exception(
                    f"Erro: Atribuição incompatível. Variável '{cmd.var}' é do tipo '{var_type}', mas recebeu '{expr_type}'."
                )
        elif cmd.token == "if":
            cond_type = self.attributes.process_EXP(cmd.children('cond'))
            if cond_type != "boolean":
                raise Exception(f"Erro: Condição de 'if' deve ser do tipo 'boolean', mas recebeu '{cond_type}'.")
            for inner_cmd in cmd.children:
                if inner_cmd.token == 'cmd':
                    self.process_CMD(inner_cmd)
        elif cmd.token == "while":
            cond_type = self.attributes.process_EXP(cmd.children('cond'))
            if cond_type != "boolean":
                raise Exception(f"Erro: Condição de 'while' deve ser do tipo 'boolean', mas recebeu '{cond_type}'.")
            for inner_cmd in cmd.children:
                if inner_cmd.token == 'cmd':
                    self.process_CMD(inner_cmd)
        elif cmd.token == "call":
            self.attributes.process_CALL(cmd.children('call'))