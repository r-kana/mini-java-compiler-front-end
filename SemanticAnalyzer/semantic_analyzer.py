from SemanticAnalyzer.annotated_tree import AnnotadedTreeNode
from Parser.parse_tree import TreeNode
from Parser.parser import parser
from Scanner.minijavaplus import MiniJava
from SemanticAnalyzer.attributes import Attributes
from SemanticAnalyzer.symbol_table import SymbolTable

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.attributes = Attributes(self.symbol_table)

    def analyze(self, ast: TreeNode):
        """
        Realiza a análise semântica a partir do arquivo fonte.
        :param source_file: Caminho para o arquivo fonte em MiniJava.
        """

        if ast is None:
            print("ERRO: A árvore de sintaxe não foi gerada corretamente.")
            return None

        self.process_PROG(ast.child('PROG'))
        annotated_ast = self.annotate_tree(ast)

        return annotated_ast


    def annotate_tree(self, parse_node: TreeNode):
        """Função recursiva que converte a árvore do parser para a árvore semântica anotada."""
        if parse_node is None:
            return None

        token = parse_node.token
        lexeme = parse_node.lexeme
        literal = parse_node.literal

        annotated_node = AnnotadedTreeNode(
            token=token,
            semantic_type=None,
            lexeme=lexeme,
            literal=literal
        )

        for child in parse_node.children:
            annotated_child = self.annotate_tree(child)
            annotated_node.add_child(annotated_child)

        return annotated_node

    def process_PROG(self, prog: TreeNode):
        self.process_MAIN(prog.child('MAIN'))
        
        classe_list = prog.child('CLASSE_LIST')
        self.process_CLASSE(classe_list.child('CLASSE'))
        classe_list = classe_list.child('CLASSE_LIST')
        while (not classe_list.is_empty()):
            self.process_CLASSE(classe_list.child('CLASSE'))
            classe_list = classe_list.child('CLASSE_LIST')
        
        #prog.semantic_type = prog.main.semantic_type

    def process_MAIN(self, main: TreeNode):
        if self.symbol_table.is_class_declared(main.child("id").lexeme):
            classe_print = main.child("id").token
            raise Exception(f"Erro: Classe '{classe_print}' já declarada.")
        
        self.symbol_table.add_class(main.child("id").lexeme)
        #main.semantic_type = "void"
        self.process_CMD(main.child("CMD"))

    def process_CLASSE(self, classe: TreeNode):
        if self.symbol_table.is_class_declared(classe.child('id').lexeme):
            classe_print = classe.child("id").lexeme
            raise Exception(f"Erro: Classe '{classe_print}' já declarada.")
        
        self.symbol_table.add_class(classe.child("id").lexeme)
        classe_d = classe.child('CLASSE_D')
        if (classe_d.children[0] == 'extends' and 
            not self.symbol_table.is_class_declared(classe_d.children[1].lexeme)):
            classes_print = classe_d.children[1].lexeme
            raise Exception(
                f"Erro: Classe base '{classes_print}' não declarada.")
        
        var_list = classe_d.child('VAR_LIST')
        while (not var_list.is_empty()):
            self.attributes.process_VAR(var_list.child('VAR'))
            var_list = var_list.child('VAR_LIST')
        
        metodo_list = classe_d.child('METODO_LIST')
        while (not metodo_list.is_empty()):
            self.process_METODO(metodo_list.child('METODO'))
            metodo_list = metodo_list.child('METODO_LIST')


    def process_METODO(self, metodo: TreeNode):
        if self.symbol_table.is_method_declared(metodo.child("id").lexeme):
            metodo_print = metodo.child("id").lexeme
            raise Exception(f"Erro: Método '{metodo_print}' já declarado.")
        
        metodo_d = metodo.child('METODO_D')
        params = metodo_d.child('PARAMS')
        method_params = [] # [ { tipo: 'int', id: 'x'} ]
        while params is not None and not params.is_empty():
            param_type = params.child('TIPO').children[0].lexeme
            param_id = params.child('id').lexeme
            if self.symbol_table.is_variable_declared(param_id):
                param_print = params.child("id").lexeme
                raise Exception(
                    f"Erro: Parâmetro '{param_print}' já declarado no escopo.")
                
            self.symbol_table.add_variable(params.child("id").lexeme, param_type)
            method_params.append({ 'type': param_type, 'id': param_id })
            params = params.child('PARAMS_LIST')
        
        metodo_type = metodo.child("TIPO").children[0].lexeme
        self.symbol_table.add_method(metodo.child("id").lexeme, metodo_type, method_params)

        var_list = metodo_d.child('VAR_LIST')
        while (not var_list.is_empty()):
            self.attributes.process_VAR(var_list.child('VAR'))
            var_list = var_list.child('VAR_LIST')

        cmd_list = metodo_d.child('CMD_LIST')
        while (not cmd_list.is_empty()):
            self.process_CMD(cmd_list.child('CMD'))
            cmd_list = cmd_list.child('CMD_LIST')
        
        return_type = self.attributes.process_EXP(metodo_d.child('EXP'))
        if return_type != metodo_type:
            metodo_print = metodo.child("id").lexeme
            raise Exception(
                f"Erro: semantic_type de retorno '{return_type}' incompatível com o semantic_type declarado '{metodo_type}' no método '{metodo_print}'."
            )

    def process_CMD(self, cmd: TreeNode):
        cmd_d = cmd.child("CMD_D")
        if (cmd_d is not None):
            if not self.symbol_table.is_variable_declared(cmd.child('id').lexeme):
                var_print = cmd.child('id').lexeme
                raise Exception(f"Erro: Variável '{var_print}' não declarada.")
            
            var_type = self.symbol_table.get_variable_type(cmd.child('id').lexeme)
            exp = cmd_d.children[-2] # CMD_D -> [..., 'EXP', ';']
            expr_type = self.attributes.process_EXP(exp)
            if var_type != expr_type:
                print_var = cmd.child('id').lexeme
                raise Exception(
                    f"Erro: Atribuição incompatível. Variável '{print_var}' é do semantic_type '{var_type}', mas recebeu '{expr_type}'."
                )

        elif cmd.child("if") is not None:
            cond_type = self.attributes.process_EXP(cmd.child("EXP"))
            if cond_type != "boolean":
                raise Exception(
                    f"Erro: Condição de 'if' deve ser do semantic_type 'boolean', mas recebeu '{cond_type}'.")
            
            cmd_if = cmd.children[4]
            self.process_CMD(cmd_if)
            
            cmd_else = cmd.children[6]
            self.process_CMD(cmd_else)
            
        elif cmd.child("while") is not None:
            cond_type = self.attributes.process_EXP(cmd.child("EXP"))
            if cond_type != "boolean":
                raise Exception(
                    f"Erro: Condição de 'while' deve ser do semantic_type 'boolean', mas recebeu '{cond_type}'.")
            
            cmd_while = cmd.child('CMD')
            self.process_CMD(cmd_while)
            
        elif cmd.child("System.out.println") is not None:
            self.attributes.process_CALL(cmd)

