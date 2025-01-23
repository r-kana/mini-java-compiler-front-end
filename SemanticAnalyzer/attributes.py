from Parser.parse_tree import TreeNode
from SemanticAnalyzer.symbol_table import SymbolTable
class Attributes:
    def __init__(self, symbol_table: SymbolTable):
        self.symbol_table = symbol_table


    def process_EXP(self, exp: TreeNode) -> str:
        """Processa expressões dentro do código"""
        if exp.token == "EXP":
            if not exp.child('EXP_R').is_empty():
                return "boolean"
            else:
                return self.process_EXP(exp.children[0])
            
        if exp.token == "REXP":
            if not exp.child('REXP_R').is_empty():
                return "boolean"
            else:
                return self.process_EXP(exp.children[0])
            
        if exp.token == "AEXP":
            if not exp.child('AEXP_R').is_empty():
                return "int"
            else:
                return self.process_EXP(exp.children[0])
            
        if exp.token == "MEXP":
            if not exp.child('MEXP_R').is_empty():
                return "int"
            else:
                return self.process_EXP(exp.children[0])
            
        if exp.token == "SEXP":
            if exp.child('SEXP') is not None:
                return self.process_EXP(exp.child('SEXP'))
            else:
                return self.process_EXP(exp.child('BASE_SXP'))
            
        if exp.token == "BASE_SXP":
            first_child = exp.children[0].token
            if first_child == 'true' or first_child == 'false' or first_child == 'null' :
                return "boolean"
            elif first_child == 'new int' or first_child == 'num':
                return "int"
            else:
                return self.process_EXP(exp.child('PEXP'))
            
        if exp.token == "PEXP":
            if exp.child('EXP') is not None: # PEXP -> ( EXP ) REST_PEXP
                return self.process_EXP(exp.child('EXP'))
            
            elif exp.child("id").lexeme: # PEXP -> id REST_PEXP
                return self.symbol_table.get_variable_type(exp.child("id").lexeme)
            
            else:
                return "int"


    def process_CALL(self, metodo: TreeNode):
        if metodo.children[0] == '.' : # REST_PEXP -> . id REST_PEXP_TAIL
            method_args: list[TreeNode]
            method_args = []
            metodo_id = metodo.child('id').lexeme
            if not self.symbol_table.is_method_declared(metodo_id):
                raise Exception(f"Erro: Método '{metodo_id}' não declarado.")

            declared_params = self.symbol_table.get_method_params(metodo_id)        
            opt_exps = metodo.child('REST_PEXP_TAIL').child('OPT_EXPS')
            if not opt_exps.is_empty():
                exps = opt_exps.child('EXPS')
                more_exps = exps.child('MORE_EXPS')
                method_args.append(exps.child('EXP'))
                while not more_exps.is_empty():
                    method_args.append(more_exps.child('EXP'))
                    more_exps = more_exps.child('MORE_EXPS')

            if len(method_args) != len(declared_params):
                call_id_print   = metodo_id
                len_params      = len(declared_params)
                call_params     = method_args
                
                raise Exception(
                    f"Erro: Método '{call_id_print}' esperado {len_params} argumentos, "
                    f"mas recebeu {call_params}."
                )

            for arg, param in zip(method_args, declared_params):
                arg_type = self.process_EXP(arg)
                if arg_type != param['tipo']:
                    raise Exception(
                        f"Erro: Tipo do argumento '{arg}' ({arg_type}) incompatível com o parâmetro '' ()."
                    )
        else: 
            self.process_EXP(metodo.child('EXP'))


    def process_VAR(self, var: TreeNode):
        var_id = var.child("id").lexeme
        """Adiciona uma variável à tabela de símbolos após checar se já foi declarada"""
        if self.symbol_table.is_variable_declared(var_id):
            raise Exception(f"Erro: Variável '{var_id}' já declarada.")

        var_type = var.child("TIPO").children[0].token
        self.symbol_table.add_variable(var_id, var_type)
