from parser.parse_tree import TreeNode
from Scanner.mytoken import Token

EPSILON = 'ε'

STACK = []

PRODUCTION_RULES = [
  ['MAIN','CLASSE_LIST'], #1
  ['class', 'id', '{', 'public', 'static', 'void', 'main', '(', 'String', '[', ']', 'id', ')', '{', 'CMD', '}', '}'], #2
  ['CLASSE', 'CLASSE_LIST'], #3
  ['class', 'id', 'CLASSE_D'], #4
  [EPSILON],# 5
  
  [EPSILON],
  [EPSILON],
  ['CMD', 'CMD_LIST'],# 12
  ['id', 'CMD_D'],# 13
  ['REXP', 'EXP_R'],# 14
  ['AEXP', 'REXP_R'],# 15
  ['MEXP', 'AEXP_R'],# 17
  ['SEXP', 'MEXP_R'],# 18
  ['BASE_SXP'],# 19
  ['PEXP', 'PEXP_TAIL'],# 20
  ['id', 'REST_PEXP'],# 21
  ['EXPS'],# 22
  ['EXP', 'MORE_EXPS'],# 23
  
  ['{', 'VAR_LIST', 'METODO_LIST', '}'],# 24
  [EPSILON],# 25
  ['CMD', 'CMD_LIST'],# 26
  ['{', 'CMD_LIST', '}'],# 27
  
  ['REXP', 'EXP_R'],# 28
  ['AEXP', 'REXP_R'],# 29
  ['MEXP', 'AEXP_R'],
  ['SEXP', 'MEXP_R'],
  ['BASE_SXP'],
  ['PEXP', 'PEXP_TAIL'],
  ['(', 'EXP', ')', 'REST_PEXP'],
  ['(', 'OPT_EXPS', ')', 'REST_PEXP'],
  ['EXPS'],
  ['EXP', 'MORE_EXPS'],
  
  ['[', ']'],
  ['[', 'EXP', ']', '=', 'EXP', ';'],
  ['[', 'EXP', ']'],
  [EPSILON],
  ['REST_PEXP'],
  
  [EPSILON],
  [EPSILON],
  [EPSILON],
  [EPSILON],
  [EPSILON],
  [EPSILON],
  ['REST_PEXP'],
  
  [')', '{', 'VAR_LIST', 'CMD_LIST', 'return', 'EXP', ';', '}'],
  [EPSILON],
  [EPSILON],
  [EPSILON],
  [EPSILON],
  [EPSILON],
  [EPSILON],
  [EPSILON],
  ['REST_PEXP'],
  [EPSILON],
  [EPSILON],
  
  [EPSILON],
  [EPSILON],
  [EPSILON],
  
  ['extends', 'id', '{', 'VAR_LIST', 'METODO_LIST', '}'],
  
  [EPSILON],
  [EPSILON],
  [EPSILON],
  [EPSILON],
  [EPSILON],
  [EPSILON],
  ['REST_PEXP'],
  
  [EPSILON],
  ['METODO', 'METODO_LIST'],
  ['public', 'TIPO', 'id', '(', 'METODO_D'],
  
  [EPSILON],
  [EPSILON],
  
  [',', 'TIPO', 'id', 'PARAMS_LIST'],
  [EPSILON],
  [EPSILON],
  [EPSILON],
  [EPSILON],
  [EPSILON],
  [EPSILON],
  ['REST_PEXP'],
  [',', 'EXP', 'MORE_EXPS'],
  
  ['VAR', 'VAR_LIST'],
  ['TIPO', 'id', ';'],
  ['PARAMS', ')', '{', 'VAR_LIST', 'CMD_LIST', 'return', 'EXP', ';', '}'],
  ['TIPO', 'id', 'PARAMS_LIST'],
  ['int', 'TIPO_D'],
  
  ['VAR', 'VAR_LIST'],
  ['TIPO', 'id', ';'],
  ['PARAMS', ')', '{', 'VAR_LIST', 'CMD_LIST', 'return', 'EXP', ';', '}'],
  ['TIPO', 'id', 'PARAMS_LIST'],
  ['boolean'],
  
  [EPSILON],
  ['CMD', 'CMD_LIST'],
  ['while', '(', 'EXP', ')', 'CMD'],
  
  [EPSILON],
  ['CMD', 'CMD_LIST'],
  ['System.out.println', '(', 'EXP', ')', ';'],
  
  ['=', 'EXP', ';'],
  
  ['&&', 'REXP', 'EXP_R'],
  [EPSILON],
  [EPSILON],
  [EPSILON],
  [EPSILON],
  [EPSILON],
  ['REST_PEXP'],
  
  ['REXP_D', 'REXP_R'],
  ['<', 'AEXP'],
  [EPSILON],
  [EPSILON],
  [EPSILON],
  [EPSILON],
  ['REST_PEXP'],
  
  ['REXP_D', 'REXP_R'],
  ['==', 'AEXP'],
  [EPSILON],
  [EPSILON],
  [EPSILON],
  [EPSILON],
  ['REST_PEXP'],
  
  ['REXP_D', 'REXP_R'],
  ['!=', 'AEXP'],
  [EPSILON],
  [EPSILON],
  [EPSILON],
  [EPSILON],
  ['REST_PEXP'],
  
  ['AEXP_D', 'AEXP_R'],
  ['+', 'MEXP'],
  [EPSILON],
  [EPSILON],
  [EPSILON],
  ['REST_PEXP'],
  
  ['REXP', 'EXP_R'],
  ['AEXP', 'REXP_R'],
  ['MEXP', 'AEXP_R'],
  ['AEXP_D', 'AEXP_R'],
  ['-', 'MEXP'],
  ['SEXP', 'MEXP_R'],
  [EPSILON],
  ['PREFIX', 'SEXP'],
  ['-'],
  [EPSILON],
  [EPSILON],
  ['REST_PEXP'],
  ['EXPS'],
  ['EXP', 'MORE_EXPS'],
  
  ['*', 'SEXP', 'MEXP_R'],
  [EPSILON],
  [EPSILON],
  ['REST_PEXP'],
  
  ['REXP', 'EXP_R'],
  ['AEXP', 'REXP_R'],
  ['MEXP', 'AEXP_R'],
  ['SEXP', 'MEXP_R'],
  ['PREFIX', 'SEXP'],
  ['!'],
  ['EXPS'],
  ['EXP', 'MORE_EXPS'],
  
  ['REXP', 'EXP_R'],
  ['AEXP', 'REXP_R'],
  ['MEXP', 'AEXP_R'],
  ['SEXP', 'MEXP_R'],
  ['BASE_SXP'],
  ['true'],
  ['EXPS'],
  ['EXP', 'MORE_EXPS'],
  
  ['REXP', 'EXP_R'],
  ['AEXP', 'REXP_R'],
  ['MEXP', 'AEXP_R'],
  ['SEXP', 'MEXP_R'],
  ['BASE_SXP'],
  ['false'],
  ['EXPS'],
  ['EXP', 'MORE_EXPS'],
  
  ['REXP', 'EXP_R'],
  ['AEXP', 'REXP_R'],
  ['MEXP', 'AEXP_R'],
  ['SEXP', 'MEXP_R'],
  ['BASE_SXP'],
  ['num'],
  ['EXPS'],
  ['EXP', 'MORE_EXPS'],
  
  ['REXP', 'EXP_R'],
  ['AEXP', 'REXP_R'],
  ['MEXP', 'AEXP_R'],
  ['SEXP', 'MEXP_R'],
  ['BASE_SXP'],
  ['null'],
  ['EXPS'],
  ['EXP', 'MORE_EXPS'],
  
  ['REXP', 'EXP_R'],
  ['AEXP', 'REXP_R'],
  ['MEXP', 'AEXP_R'],
  ['SEXP', 'MEXP_R'],
  ['BASE_SXP'],
  ['new int', '[', 'EXP', ']'], #NOTE token conjunto
  ['EXPS'],
  ['EXP', 'MORE_EXPS'],
  
  ['.length'], #NOTE token conjunto
  [EPSILON],
  ['REST_PEXP'],
  
  ['REXP', 'EXP_R'],
  ['AEXP', 'REXP_R'],
  ['MEXP', 'AEXP_R'],
  ['SEXP', 'MEXP_R'],
  ['BASE_SXP'],
  ['PEXP', 'PEXP_TAIL'],
  ['this', 'REST_PEXP'],
  ['EXPS'],
  ['EXP', 'MORE_EXPS'],
  
  ['REXP', 'EXP_R'],
  ['AEXP', 'REXP_R'],
  ['MEXP', 'AEXP_R'],
  ['SEXP', 'MEXP_R'],
  ['BASE_SXP'],
  ['PEXP', 'PEXP_TAIL'],
  ['new', 'id', '(', ')', 'REST_PEXP'],
  ['EXPS'],
  ['EXP', 'MORE_EXPS'],
  
  ['.', 'id', 'REST_PEXP_TAIL'],
  ['REST_PEXP'],
  
  [EPSILON],
  [EPSILON],
]

NON_TERMINAL_SYMBOLS = [
  'PROG',
  'MAIN',
  'CLASSE_LIST',
  'CLASSE',
  'CLASSE_D',
  'VAR_LIST',
  'VAR',
  'METODO_LIST',
  'METODO',
  'METODO_D',
  'PARAMS',
  'PARAMS_LIST',
  'TIPO',
  'TIPO_D',
  'CMD_LIST',
  'CMD',
  'CMD_D',
  'EXP',
  'EXP_R',
  'REXP',
  'REXP_R',
  'REXP_D',
  'AEXP',
  'AEXP_R',
  'AEXP_D',
  'MEXP',
  'MEXP_R',
  'SEXP',
  'PREFIX',
  'BASE_SXP',
  'PEXP_TAIL',
  'PEXP',
  'REST_PEXP',
  'REST_PEXP_TAIL',
  'OPT_EXPS',
  'EXPS',
  'MORE_EXPS'
]

TERMINAL_SYMBOLS = [
  'class',
  'id',
  '{',
  '}',
  '(',
  ')',
  '[',
  ']',
  'public static void main',
  'String',
  'extends',
  'public',
  'return',
  'int',
  'boolean',
  'if',
  'else',
  'while',
  'System.out.println',
  'true',
  'false',
  'num',
  'null',
  'nem int',
  '.length',
  'this',
  'new',
  '.',
  ',',
  ';',
  '=',
  '&&',
  '<',
  '==',
  '!=',
  '+',
  '-',
  '*',
  '!',
  '$'
]

START_SYMBOL = 'PROG'

PARSING_TABLE = {
  'class': {
    'PROG': 1,
    'MAIN': 2,
    'CLASSE_LIST': 3,
    'CLASSE': 4,
    'CLASSE_D': 0,
    'VAR_LIST': 5,
    'VAR': 0,
    'METODO_LIST': 0,
    'METODO': 0,
    'METODO_D': 0,
    'PARAMS': 0,
    'PARAMS_LIST': 0,
    'TIPO': 0,
    'TIPO_D': 0,
    'CMD_LIST': 0,
    'CMD': 0,
    'CMD_D': 0,
    'EXP': 0,
    'EXP_R': 0,
    'REXP': 0,
    'REXP_R': 0,
    'REXP_D': 0,
    'AEXP': 0,
    'AEXP_R': 0,
    'AEXP_D': 0,
    'MEXP': 0,
    'MEXP_R': 0,
    'SEXP': 0,
    'PREFIX': 0,
    'BASE_SXP': 0,
    'PEXP_TAIL': 0,
    'PEXP': 0,
    'REST_PEXP': 0,
    'REST_PEXP_TAIL': 0,
    'OPT_EXPS': 0,
    'EXPS': 0,
    'MORE_EXPS': 0
  },
  'id': {
    'PROG': 0,
    'MAIN': 0,
    'CLASSE_LIST': 0,
    'CLASSE': 0,
    'CLASSE_D': 0,
    'VAR_LIST': 6,
    'VAR': 0,
    'METODO_LIST': 0,
    'METODO': 0,
    'METODO_D': 0,
    'PARAMS': 0,
    'PARAMS_LIST': 0,
    'TIPO': 0,
    'TIPO_D': 7,
    'CMD_LIST': 8,
    'CMD': 9,
    'CMD_D': 0,
    'EXP': 10,
    'EXP_R': 0,
    'REXP': 11,
    'REXP_R': 0,
    'REXP_D': 0,
    'AEXP': 12,
    'AEXP_R': 0,
    'AEXP_D': 0,
    'MEXP': 13,
    'MEXP_R': 0,
    'SEXP': 14,
    'PREFIX': 0,
    'BASE_SXP': 15,
    'PEXP_TAIL': 0,
    'PEXP': 16,
    'REST_PEXP': 0,
    'REST_PEXP_TAIL': 0,
    'OPT_EXPS': 17,
    'EXPS': 18,
    'MORE_EXPS': 0
  },
  '{': {
    'PROG': 0,
    'MAIN': 0,
    'CLASSE_LIST': 0,
    'CLASSE': 0,
    'CLASSE_D': 0,
    'VAR_LIST': 0,
    'VAR': 0,
    'METODO_LIST': 0,
    'METODO': 0,
    'METODO_D': 0,
    'PARAMS': 0,
    'PARAMS_LIST': 0,
    'TIPO': 0,
    'TIPO_D': 0,
    'CMD_LIST': 0,
    'CMD': 0,
    'CMD_D': 0,
    'EXP': 0,
    'EXP_R': 0,
    'REXP': 0,
    'REXP_R': 0,
    'REXP_D': 0,
    'AEXP': 0,
    'AEXP_R': 0,
    'AEXP_D': 0,
    'MEXP': 0,
    'MEXP_R': 0,
    'SEXP': 0,
    'PREFIX': 0,
    'BASE_SXP': 0,
    'PEXP_TAIL': 0,
    'PEXP': 0,
    'REST_PEXP': 0,
    'REST_PEXP_TAIL': 0,
    'OPT_EXPS': 0,
    'EXPS': 0,
    'MORE_EXPS': 0
  },
  "public static void main": {
    'PROG': 0,
    'MAIN': 0,
    'CLASSE_LIST': 0,
    'CLASSE': 0,
    'CLASSE_D': 0,
    'VAR_LIST': 0,
    'VAR': 0,
    'METODO_LIST': 0,
    'METODO': 0,
    'METODO_D': 0,
    'PARAMS': 0,
    'PARAMS_LIST': 0,
    'TIPO': 0,
    'TIPO_D': 0,
    'CMD_LIST': 0,
    'CMD': 0,
    'CMD_D': 0,
    'EXP': 0,
    'EXP_R': 0,
    'REXP': 0,
    'REXP_R': 0,
    'REXP_D': 0,
    'AEXP': 0,
    'AEXP_R': 0,
    'AEXP_D': 0,
    'MEXP': 0,
    'MEXP_R': 0,
    'SEXP': 0,
    'PREFIX': 0,
    'BASE_SXP': 0,
    'PEXP_TAIL': 0,
    'PEXP': 0,
    'REST_PEXP': 0,
    'REST_PEXP_TAIL': 0,
    'OPT_EXPS': 0,
    'EXPS': 0,
    'MORE_EXPS': 0
  },
  '(': {
    'PROG': 0,
    'MAIN': 0,
    'CLASSE_LIST': 0,
    'CLASSE': 0,
    'CLASSE_D': 0,
    'VAR_LIST': 0,
    'VAR': 0,
    'METODO_LIST': 0,
    'METODO': 0,
    'METODO_D': 0,
    'PARAMS': 0,
    'PARAMS_LIST': 0,
    'TIPO': 0,
    'TIPO_D': 0,
    'CMD_LIST': 0,
    'CMD': 0,
    'CMD_D': 0,
    'EXP': 0,
    'EXP_R': 0,
    'REXP': 0,
    'REXP_R': 0,
    'REXP_D': 0,
    'AEXP': 0,
    'AEXP_R': 0,
    'AEXP_D': 0,
    'MEXP': 0,
    'MEXP_R': 0,
    'SEXP': 0,
    'PREFIX': 0,
    'BASE_SXP': 0,
    'PEXP_TAIL': 0,
    'PEXP': 0,
    'REST_PEXP': 0,
    'REST_PEXP_TAIL': 0,
    'OPT_EXPS': 0,
    'EXPS': 0,
    'MORE_EXPS': 0
  }
}

ROOT = TreeNode(None, "root")

def stack_top (stack):
  return stack[len(stack) - 1]


def is_terminal_symbol (token):
  return token in TERMINAL_SYMBOLS


def is_non_terminal_symboll (token):
  return token in NON_TERMINAL_SYMBOLS


def get_production(input_symbol, stack_symbol):
  rule_index = PARSING_TABLE[input_symbol][stack_symbol] - 1
  if (rule_index >= 0):
    return PRODUCTION_RULES[rule_index]
  else:
    return None


def initialize_stack():
  STACK.append('$')
  STACK.append(START_SYMBOL)


def append_production(production):
  for i in range(len(production)):
    STACK.append(production[i])
    

def print_parse_tree(root: TreeNode, level =0):
  tab = ""
  for _ in range(level):
    tab += " "
    
  if (root.children_count != 0):
    print(f"{tab}{root.token}: {'{'}")
    level += 1
    for child in root.children:
      print_parse_tree(child, level)
    print(f"{tab}{'}'}")
  else:
    print(f"{tab}{root.token}")
  

def parser (tokens: list[Token]):
  initialize_stack()
  cursor = 0
  end_of_input = tokens[cursor].lexeme == '$'
  ROOT.children_count = 1
  parent_stack = [ROOT]
  
  while(not end_of_input):
    print(STACK)
    stack_symbol = stack_top(STACK)
    
    if (is_terminal_symbol(stack_symbol)):
      if (stack_symbol == tokens[cursor]):
        tree_node = TreeNode(parent_stack[-1], STACK.pop())
        parent_stack[-1].children.append(tree_node)
        print(tree_node.token)
        
        if (parent_stack[-1].is_complete()):
          parent_stack.pop()
        
        cursor += 1
      else:
        end_of_input = True
        print("ERRO: erro de sintaxe. Sem correspondencia com simbolo terminal")
        
    elif (is_non_terminal_symboll(stack_symbol)):
      production = get_production(tokens[cursor].lexeme, stack_symbol)
      if (production is None) :
        end_of_input = True
        print("ERRO: erro de sintaxe. Não existe produção possível")
      else:
        tree_node = TreeNode(parent_stack[-1], STACK.pop())
        print(tree_node.token)
        parent_stack[-1].children.append(tree_node)
        
        if (parent_stack[-1].is_complete()):
          parent_stack.pop()
          
        parent_stack.append(tree_node)
        
        if (production != EPSILON):  
          tree_node.append_children(production)    
          append_production(production[::-1])
        else:
          tree_node.children.append(TreeNode(tree_node, EPSILON))
          tree_node.children_count += 1
          parent_stack.pop()
      
    end_of_input = tokens[cursor].lexeme == '$'
    
    
def test_parser(tokens):
  for token in tokens:
    print(token)

# print_parse_tree(ROOT)
    