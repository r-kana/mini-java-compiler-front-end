class Attributes:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table

    def process_EXP(self, expr):
        """Processa expressões dentro do código"""
        if expr.token == "const":
            return self.determine_constant_type(expr.literal)

        elif expr.token == "binop":
            left_value = self.process_EXP(expr.childrenren('left'))
            right_value = self.process_EXP(expr.childrenren('right'))
            return self.check_binop_types(expr, left_value, right_value)

        elif expr.token == "unop":
            inner_value = self.process_EXP(expr.childrenren('expr'))
            return self.check_unop_type(expr, inner_value)

        elif expr.token == "var":
            return self.process_VAR(expr.childrenren('var'))

        elif expr.token == "call":
            return self.process_CALL(expr.childrenren('call'))

    def determine_constant_type(self, value):
        """Determina o tipo de uma constante"""
        if isinstance(value, bool):
            return "boolean"
        elif isinstance(value, int):
            return "int"
        elif value is None:
            return "null"
        else:
            raise Exception(f"Erro: Tipo desconhecido para constante '{value}'.")

    def check_binop_types(self, expr, left_value, right_value):
        """Verifica os tipos de operandos para operações binárias"""
        if expr.children('op').lexeme in ["&&", "||"]:
            if left_value != "boolean" or right_value != "boolean":
                raise Exception("Erro: Operadores lógicos requerem operandos do tipo 'boolean'.")
            return "boolean"
        elif expr.children('op').lexeme in ["+", "-", "*"]:
            if left_value != "int" or right_value != "int":
                raise Exception("Erro: Operadores aritméticos requerem operandos do tipo 'int'.")
            return "int"
        else:
            raise Exception(f"Erro: Operação binária '{expr.children('op').lexeme}' incompatível.")

    def check_unop_type(self, expr, value):
        """Verifica os tipos de operandos para operações unárias"""
        if expr.children('op').lexeme == "!":
            if value != "boolean":
                raise Exception("Erro: Operador '!' requer um operando do tipo 'boolean'.")
            return "boolean"
        elif expr.children('op').lexeme == "-":
            if value != "int":
                raise Exception("Erro: Operador '-' requer um operando do tipo 'int'.")
            return "int"
        else:
            raise Exception(f"Erro: Operação unária '{expr.children('op').lexeme}' incompatível.")
        
    def process_CALL(self, call):
        if not self.symbol_table.is_method_declared(call.children('method_id').lexeme):
            raise Exception(f"Erro: Método '{call.children('method_id').lexeme}' não declarado.")

        declared_params = self.symbol_table.get_method_params(call.children('method_id').lexeme)

        if len(call.children('arguments').children) != len(declared_params):
            raise Exception(
                f"Erro: Método '{call.children('method_id').lexeme}' esperado {len(declared_params)} argumentos, "
                f"mas recebeu {len(call.children('arguments').children)}."
            )

        for arg, param in zip(call.children('arguments').children, declared_params):
            arg_type = self.process_EXP(arg)
            if arg_type != param.semantic_type:
                raise Exception(
                    f"Erro: Tipo do argumento ({arg_type}) incompatível com o parâmetro '{param.lexeme}' ({param.semantic_type})."
                )

    def process_VAR(self, var):
        """Adiciona uma variável à tabela de símbolos após checar se já foi declarada"""
        if self.symbol_table.is_variable_declared(var.children('id').lexeme):
            raise Exception(f"Erro: Variável '{var.children('id').lexeme}' já declarada.")

        self.symbol_table.add_variable(var.children('id').lexeme, var.semantic_type)