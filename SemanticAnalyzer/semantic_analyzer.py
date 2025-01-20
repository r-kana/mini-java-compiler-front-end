from SemanticAnalyzer.annotated_tree import AnnotadedTreeNode
from Parser.parser import parser
from Scanner.minijavaplus import MiniJava
from SemanticAnalyzer.attributes import Attributes
from SemanticAnalyzer.symbol_table import SymbolTable

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.attributes = Attributes(self.symbol_table)
        
    def semantic_analysis(symbol_table, symbol_name):
        symbol = symbol_table.get(symbol_name)
        if symbol is None:
            print(f"ERRO: Símbolo {symbol_name} não declarado.")
            return None
        return symbol


    def analyze(self, source_file):
        """
        Realiza a análise semântica a partir do arquivo fonte.
        :param source_file: Caminho para o arquivo fonte em MiniJava.
        """
        ast = parser(MiniJava.main(source_file))

        if ast is None:
            print("ERRO: A árvore de sintaxe não foi gerada corretamente.")
            return None
      
        self.process_PROG(ast)
        annotated_ast = self.annotate_tree(ast)
        
        return annotated_ast


    def annotate_tree(self, parse_tree):
        """Transforma a árvore de parse em uma árvore anotada."""
        if parse_tree is None:
            return None

        node = TreeNode(name=parse_tree.get("type"),
                        tipo=parse_tree.get("tipo"))

        for child in parse_tree.get("children", []):
            node.add_child(self.annotate_tree(child))

        return node

    def process_PROG(self, prog):      
        self.process_MAIN(prog.main)
        for classe in prog.classes:
            self.process_CLASSE(classe)
        prog.tipo = prog.main.tipo

    def process_MAIN(self, main):
        if self.symbol_table.is_class_declared(main.id):
            raise Exception(f"Erro: Classe '{main.id}' já declarada.")
        self.symbol_table.add_class(main.id)
        main.tipo = "void"
        self.process_CMD(main.cmd)

    def process_CLASSE(self, classe):
        if self.symbol_table.is_class_declared(classe.id):
            raise Exception(f"Erro: Classe '{classe.id}' já declarada.")
        self.symbol_table.add_class(classe.id)
        if classe.extends and not self.symbol_table.is_class_declared(classe.extends):
            raise Exception(
                f"Erro: Classe base '{classe.extends}' não declarada.")
        for var in classe.vars:
            self.process_VAR(var)
        for metodo in classe.methods:
            self.process_METODO(metodo)

    def process_METODO(self, metodo):
        if self.symbol_table.is_method_declared(metodo.id):
            raise Exception(f"Erro: Método '{metodo.id}' já declarado.")
        self.symbol_table.add_method(metodo.id, metodo.tipo, metodo.params)

        for param in metodo.params:
            if self.symbol_table.is_variable_declared(param.id):
                raise Exception(
                    f"Erro: Parâmetro '{param.id}' já declarado no escopo.")
            self.symbol_table.add_variable(param.id, param.tipo)

        for var in metodo.vars:
            self.process_VAR(var)

        for cmd in metodo.cmds:
            self.process_CMD(cmd)

        if metodo.return_expr:
            return_type = self.attributes.process_EXP(metodo.return_expr)
            if return_type != metodo.tipo:
                raise Exception(
                    f"Erro: Tipo de retorno '{return_type}' incompatível com o tipo declarado '{metodo.tipo}' no método '{metodo.id}'."
                )

    def process_CMD(self, cmd):
        if cmd.type == "assign":
            if not self.symbol_table.is_variable_declared(cmd.var):
                raise Exception(f"Erro: Variável '{cmd.var}' não declarada.")
            var_type = self.symbol_table.get_variable_type(cmd.var)
            expr_type = self.attributes.process_EXP(cmd.expr)
            if var_type != expr_type:
                raise Exception(
                    f"Erro: Atribuição incompatível. Variável '{cmd.var}' é do tipo '{var_type}', mas recebeu '{expr_type}'."
                )
        elif cmd.type == "if":
            cond_type = self.attributes.process_EXP(cmd.cond)
            if cond_type != "boolean":
                raise Exception(
                    f"Erro: Condição de 'if' deve ser do tipo 'boolean', mas recebeu '{cond_type}'.")
            for inner_cmd in cmd.if_cmds:
                self.process_CMD(inner_cmd)
            for inner_cmd in cmd.else_cmds:
                self.process_CMD(inner_cmd)
        elif cmd.type == "while":
            cond_type = self.attributes.process_EXP(cmd.cond)
            if cond_type != "boolean":
                raise Exception(
                    f"Erro: Condição de 'while' deve ser do tipo 'boolean', mas recebeu '{cond_type}'.")
            for inner_cmd in cmd.body_cmds:
                self.process_CMD(inner_cmd)
        elif cmd.type == "call":
            self.process_CALL(cmd.call)
