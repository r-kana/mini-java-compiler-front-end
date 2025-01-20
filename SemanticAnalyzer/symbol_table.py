class SymbolTable:
    def __init__(self):
        self.classes = {}
        self.variables = {}
        self.methods = {}
        self.current_scope = {}

    def is_class_declared(self, class_id):
        return class_id in self.classes

    def add_class(self, class_id):
        self.classes[class_id] = True

    def is_variable_declared(self, var_id):
        return var_id in self.current_scope

    def add_variable(self, var_id, var_type):
        self.current_scope[var_id] = var_type

    def get_variable_type(self, var_id):
        return self.current_scope.get(var_id, None)

    def is_method_declared(self, method_id):
        return method_id in self.methods

    def add_method(self, method_id, return_type, params):
        self.methods[method_id] = {"return_type": return_type, "params": params}

    def get_method_return_type(self, method_id):
        return self.methods.get(method_id, {}).get("return_type", None)

    def get_method_params(self, method_id):
        return self.methods.get(method_id, {}).get("params", [])
