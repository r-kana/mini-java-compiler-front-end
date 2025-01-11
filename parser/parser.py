from Parser.parse_tree import TreeNode
from Scanner.token import Token
from Parser.production_rules import PARSING_TABLE, EPSILON

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
  'public',
  'static',
  'void',
  'main',
  '(',
  'String',
  '[',
  ']',
  ')',
  '}',
  'extends',
  ';',
  'public',
  'return',
  ',',
  'int',
  'boolean',
  'if',
  'else',
  'while',
  'System.out.println',
  '=',
  '&&',
  '<',
  '==',
  '!=',
  '+',
  '-',
  '*',
  '!',
  'true',
  'false',
  'num',
  'null',
  'new int',
  '.length',
  'this',
  'new',
  '.',
  '$'
]

START_SYMBOL = 'PROG'

ROOT = TreeNode(None, "root")

def stack_top(stack):
  if (len(stack) > 0):
    return stack[-1]
  else:
    return None


def is_terminal_symbol(token):
  return token in TERMINAL_SYMBOLS


def is_non_terminal_symbol(token):
  return token in NON_TERMINAL_SYMBOLS


def get_production(input_symbol, stack_input):
  try:
    return PARSING_TABLE[input_symbol][stack_input]
  except KeyError:
    return None


def initialize_stack():
  STACK.append('$')
  STACK.append(START_SYMBOL)


def append_production(production):
  for i in range(len(production)):
    STACK.append(production[i])
    

def print_parse_tree(root: TreeNode, level=0):
  tab = ""
  for _ in range(level):
    tab += "."
    
  if (root.children_count != 0):
    children = ''
    for child in root.children:
      children += f" {child.token} "
    
    print(f"{tab} ↳ {root.token} ({children})")
    level += 1
    for child in root.children:
      print_parse_tree(child, level)
  else:
    print(f"{tab} < {root.token} | {root.lexeme} >")
  

def parser (tokens: list[Token]):
  initialize_stack()
  cursor = 0
  end_of_input = tokens[cursor].value == '$'
  ROOT.children_count = 1
  parent_stack = [ROOT]
  
  while(not end_of_input):
    stack_input = stack_top(STACK)
    
    if (stack_input is None):
      end_of_input = True
      print(f"ERRO:\n  Erro de sintaxe: Fim da pilha sintatica")
      
    elif (is_terminal_symbol(stack_input)):
      if (stack_input == tokens[cursor].value):
        if (stack_input != '$') :
          tree_node = TreeNode(parent_stack[-1], STACK.pop(), tokens[cursor].lexeme)
          parent_stack[-1].children.append(tree_node)
          
          if (parent_stack[-1].is_complete()):
            parent_stack.pop()
          
          cursor += 1
        
        else:
          end_of_input = True
          print("FIM DO ARQUIVO\n\n")
          
      else:
        end_of_input = True
        print(f"ERRO:\n  Erro de sintaxe: Sem correspondencia com simbolo terminal\n    Token: {tokens[cursor].value}\n    Pilha: {stack_input}")
        
    elif (is_non_terminal_symbol(stack_input)):
      production = get_production(tokens[cursor].value, stack_input)
      
      if (production is None) :
        end_of_input = True
        print(f"ERRO:\n  Erro de sintaxe: Não existe produção possível\n    Token: {tokens[cursor].value}\n    Pilha: {stack_input}")
      
      else:
        tree_node = TreeNode(parent_stack[-1], STACK.pop())
        parent_stack[-1].children.append(tree_node)
        
        if (parent_stack[-1].is_complete()):
          parent_stack.pop()
        
        parent_stack.append(tree_node)
        
        if (production != EPSILON):
          tree_node.append_children(production)
          append_production(production[::-1])
          
        else:
          tree_node.children.append(TreeNode(tree_node, EPSILON, tokens[cursor].lexeme))
          tree_node.children_count += 1
          parent_stack.pop()
          
    else:
      end_of_input = True
      print("ERRO:\n  Falha de parser: Simmbolo não é nem terminal nem não-terminal")
