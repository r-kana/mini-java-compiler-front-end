from Parser.parse_tree import TreeNode
class SymbolTable:
    def __init__(self):
        self.classes = {}
        self.variables = {}
        self.methods = {}
        self.current_scope = {}
    
    def is_class_declared(self, class_id: str) -> bool:
        return class_id in self.classes

    def add_class(self, class_id: str):
        self.classes[class_id] = True
        self.current_scope = {}

    def is_variable_declared(self, var_id: str) -> bool:
        return var_id in self.current_scope

    def add_variable(self, var_id: str, var_type: str):
        self.current_scope[var_id] = var_type

    def get_variable_type(self, var_id: str) -> str | None:
        return self.current_scope.get(var_id, None)

    def is_method_declared(self, method_id: str) -> bool:
        return method_id in self.methods

    def add_method(self, method_id: str, return_type: str, params: list[dict]):
        self.methods[method_id] = {"return_type": return_type, "params": params}
        
    def remove_method_scope(self, method_id: str):
        self.methods[method_id] 
        for var_id in self.current_scope:
            for param in self.methods[method_id]['params']:
                if param['id'] == var_id:
                    self.current_scope.pop(param['id'])

    def get_method_return_type(self, method_id: str) -> str | None:
        return self.methods.get(method_id, {}).get("return_type", None)

    def get_method_params(self, method_id) -> list[dict] | list:
        return self.methods.get(method_id, {}).get("params", [])
