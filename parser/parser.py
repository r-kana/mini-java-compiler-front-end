from parser.parse_tree import TreeNode
from Scanner.mytoken import Token
from parser.parsing_table import PARSING_TABLE
from parser.production_rules import PRODUCTION_RULES, EPSILON

STACK = []

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
    