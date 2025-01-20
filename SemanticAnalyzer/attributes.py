class Attributes:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table

    def process_EXP(self, expr):
        """Processa expressões dentro do código"""
        if expr.type == "const":
            return self.determine_constant_type(expr.value)

        elif expr.type == "binop":
            left_value = self.process_EXP(expr.left)
            right_value = self.process_EXP(expr.right)
            return self.check_binop_types(expr, left_value, right_value)

        elif expr.type == "unop":
            inner_value = self.process_EXP(expr.expr)
            return self.check_unop_type(expr, inner_value)

        elif expr.type == "var":
            return self.process_var(expr)

        elif expr.type == "call":
            return self.process_CALL(expr.call)

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
        if expr.op in ["&&", "||"]:
            if left_value != "boolean" or right_value != "boolean":
                raise Exception("Erro: Operadores lógicos requerem operandos do tipo 'boolean'.")
            return "boolean"
        elif expr.op in ["+", "-", "*"]:
            if left_value != "int" or right_value != "int":
                raise Exception("Erro: Operadores aritméticos requerem operandos do tipo 'int'.")
            return "int"
        else:
            raise Exception(f"Erro: Operação binária '{expr.op}' incompatível.")

    def check_unop_type(self, expr, value):
        """Verifica os tipos de operandos para operações unárias"""
        if expr.op == "!":
            if value != "boolean":
                raise Exception("Erro: Operador '!' requer um operando do tipo 'boolean'.")
            return "boolean"
        elif expr.op == "-":
            if value != "int":
                raise Exception("Erro: Operador '-' requer um operando do tipo 'int'.")
            return "int"
        else:
            raise Exception(f"Erro: Operação unária '{expr.op}' incompatível.")

    def process_CALL(self, call):
        if not self.symbol_table.is_method_declared(call.method_id):
            raise Exception(f"Erro: Método '{call.method_id}' não declarado.")

        declared_params = self.symbol_table.get_method_params(call.method_id)

        if len(call.arguments) != len(declared_params):
            raise Exception(
                f"Erro: Método '{call.method_id}' esperado {len(declared_params)} argumentos, "
                f"mas recebeu {len(call.arguments)}."
            )

        for arg, param in zip(call.arguments, declared_params):
            arg_type = self.process_EXP(arg)
            if arg_type != param.tipo:
                raise Exception(
                    f"Erro: Tipo do argumento '{arg}' ({arg_type}) incompatível com o parâmetro '{param.id}' ({param.tipo})."
                )

    def process_VAR(self, var):
        """Adiciona uma variável à tabela de símbolos após checar se já foi declarada"""
        if self.symbol_table.is_variable_declared(var.id):
            raise Exception(f"Erro: Variável '{var.id}' já declarada.")

        self.symbol_table.add_variable(var.id, var.tipo)
