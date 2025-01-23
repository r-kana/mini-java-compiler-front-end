from SemanticAnalyzer.annotated_tree import AnnotatedTreeNode
from Parser.parser import parser
from Parser.parse_tree import TreeNode
from Scanner.minijavaplus import MiniJava
from SemanticAnalyzer.attributes import Attributes
from SemanticAnalyzer.symbol_table import SymbolTable

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        self.attributes = Attributes(self.symbol_table)

    def analyze(self, ast):

        if ast is None:
            print("ERRO: A árvore de sintaxe não foi gerada corretamente.")
            return None

        self.parseTree(ast.children[0])

    def parseTree(self, node):
        if (node.token == 'PROG'):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == "MAIN"):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == "class"):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == "id"):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == 'public'):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == "static"):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == 'void'):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == "main"):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == 'String'):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == "CMD"):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == 'System.out.println'):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == "EXP"):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == 'REXP'):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == "AEXP"):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == 'MEXP'):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == "SEXP"):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == 'BASE_SXP'):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == "PEXP"):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == 'new'):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == "REST_PEXP"):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == 'REST_PEXP_TAIL'):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == "OPT_EXPS"):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == 'num'):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == "MEXP_R"):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == 'AEXP_R'):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == "REXP_R"):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == 'EXP_R'):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == "MORE_EXPS"):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == 'PEXP_TAIL'):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == "CLASSE_LIST"):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == 'CLASSE'):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == "CLASSE_D"):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == 'VAR_LIST'):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == "VAR"):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == 'TIPO'):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == "METODO_LIST"):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == 'METODO'):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == "public"):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == 'TIPO'):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == "TIPO_D"):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == 'METODO_D'):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == "PARAMS"):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == 'PARAMS_LIST'):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == "CMD_LIST"):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == 'CMD_D'):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == "AEXP_D"):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == "AEXP_D"):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == "REXP_D"):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == "else"):
            for child in node.children:
                self.parseTree(child)
        elif (node.token == "return"):
            for child in node.children:
                self.parseTree(child)
        else:
            print(node.token)
