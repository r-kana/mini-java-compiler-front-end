EPSILON = 'ε'

PARSING_TABLE = {
  'class': {
    'PROG': ['MAIN','CLASSE_LIST'], #1
    'MAIN': ['class', 'id', '{', 'public', 'static', 'void', 'main', '(', 'String', '[', ']', 'id', ')', '{', 'CMD', '}', '}'], #2
    'CLASSE_LIST': ['CLASSE', 'CLASSE_LIST'], #3
    'CLASSE': ['class', 'id', 'CLASSE_D'], #4
    'VAR_LIST': EPSILON,# 5
  },
  'id': {
    'VAR_LIST': EPSILON, # 6
    'VAR': ['TIPO', 'id', ';'], # 7
    'METODO_D': ['PARAMS', ')', '{', 'VAR_LIST', 'CMD_LIST', 'return', 'EXP', ';', '}'],# 8
    'PARAMS': [ 'TIPO', 'id', 'PARAMS_LIST'], # 9
    'TIPO': ['id'], # 10
    'TIPO_D': EPSILON, # 11
    'CMD_LIST': ['CMD', 'CMD_LIST'], # 12
    'CMD': ['id', 'CMD_D'],# 13
    'EXP': ['REXP', 'EXP_R'],# 14
    'REXP': ['AEXP', 'REXP_R'],# 15
    'AEXP': ['MEXP', 'AEXP_R'],# 17
    'MEXP': ['SEXP', 'MEXP_R'],# 18
    'SEXP': ['BASE_SXP'],# 19
    'BASE_SXP': ['PEXP', 'PEXP_TAIL'],# 20
    'PEXP': ['id', 'REST_PEXP'],# 21
    'OPT_EXPS': ['EXPS'],# 22
    'EXPS': ['EXP', 'MORE_EXPS'],# 23
  },
  
  '{':{
    'CLASSE_D': ['{', 'VAR_LIST', 'METODO_LIST', '}'],# 24
    'VAR_LIST': EPSILON,# 25
    'CMD_LIST': ['CMD', 'CMD_LIST'],# 26
    'CMD': ['{', 'CMD_LIST', '}'],# 27
  },
  
  'public': {
    'VAR_LIST': EPSILON,
    'METODO_LIST': ['METODO', 'METODO_LIST'],
    'METODO': ['public', 'TIPO' 'id' '(', 'METODO_D']
  },
  
  '(': {
    'EXP': ['REXP', 'EXP_R'],# 28
    'REXP': ['AEXP', 'REXP_R'],# 29
    'AEXP': ['MEXP', 'AEXP_R'],
    'MEXP': ['SEXP', 'MEXP_R'],
    'SEXP': ['BASE_SXP'],
    'BASE_SXP': ['PEXP', 'PEXP_TAIL'],
    'PEXP': ['(', 'EXP', ')', 'REST_PEXP'],
    'REST_PEXP_TAIL': ['(', 'OPT_EXPS', ')', 'REST_PEXP'],
    'OPT_EXPS': ['EXPS'],
    'EXPS': ['EXP', 'MORE_EXPS'],
  },
  
  '[': {
    'TIPO_D': ['[', ']'],
    'CMD_D': ['[', 'EXP', ']', '=', 'EXP', ';'],
    'PEXP_TAIL': ['[', 'EXP', ']'],
    'REST_PEXP': EPSILON,
    'REST_PEXP_TAIL': ['REST_PEXP'],
  },
  
  ']':{
    'EXP_R': EPSILON,
    'REXP_R': EPSILON,
    'AEXP_R': EPSILON,
    'MEXP_R': EPSILON,
    'PEXP_TAIL': EPSILON,
    'REST_PEXP': EPSILON,
    'REST_PEXP_TAIL': ['REST_PEXP'],
  },
  
  ')': {
    'METODO_D': [')', '{', 'VAR_LIST', 'CMD_LIST', 'return', 'EXP', ';', '}'],
    'PARAMS_LIST': EPSILON,
    'EXP_R': EPSILON,
    'REXP_R': EPSILON,
    'AEXP_R': EPSILON,
    'MEXP_R': EPSILON,
    'PEXP_TAIL': EPSILON,
    'REST_PEXP': EPSILON,
    'REST_PEXP_TAIL': ['REST_PEXP'],
    'OPT_EXPS': EPSILON,
    'MORE_EXPS': EPSILON,
  },
  
  '}': {
    'VAR_LIST': EPSILON,
    'METODO_LIST': EPSILON,
    'CMD_LIST': EPSILON,
  },
  
  'extends': {
    'CLASSE_D': ['extends', 'id', '{', 'VAR_LIST', 'METODO_LIST', '}'],
  },
  
  ';': {
    'EXP_R': EPSILON,
    'REXP_R': EPSILON,
    'AEXP_R': EPSILON,
    'MEXP_R': EPSILON,
    'PEXP_TAIL': EPSILON,
    'REST_PEXP': EPSILON,
    'REST_PEXP_TAIL': ['REST_PEXP'],
  },
  
  'public': {
    'VAR_LIST': EPSILON,
    'METODO_LIST': ['METODO', 'METODO_LIST'],
    'METODO': ['public', 'TIPO', 'id', '(', 'METODO_D'],
  },
  
  'return': {
    'VAR_LIST': EPSILON,
    'CMD_LIST': EPSILON,
  },
  
  ',': {
    'PARAMS_LIST': [',', 'TIPO', 'id', 'PARAMS_LIST'],
    'EXP_R': EPSILON,
    'REXP_R': EPSILON,
    'AEXP_R': EPSILON,
    'MEXP_R':EPSILON,
    'PEXP_TAIL': EPSILON,
    'REST_PEXP': EPSILON,
    'REST_PEXP_TAIL': ['REST_PEXP'],
    'MORE_EXPS': [',', 'EXP', 'MORE_EXPS'],
  },
  
  'int': {
    'VAR_LIST': ['VAR', 'VAR_LIST'],
    'VAR': ['TIPO', 'id', ';'],
    'METODO_D': ['PARAMS', ')', '{', 'VAR_LIST', 'CMD_LIST', 'return', 'EXP', ';', '}'],
    'PARAMS': ['TIPO', 'id', 'PARAMS_LIST'],
    'TIPO': ['int', 'TIPO_D'],
  },
  
  'boolean': {
    'VAR_LIST': ['VAR', 'VAR_LIST'],
    'VAR': ['TIPO', 'id', ';'],
    'METODO_D': ['PARAMS', ')', '{', 'VAR_LIST', 'CMD_LIST', 'return', 'EXP', ';', '}'],
    'PARAMS': ['TIPO', 'id', 'PARAMS_LIST'],
    'TIPO': ['boolean'],
  },
  
  'if': {
    'VAR_LIST': EPSILON,
    'CMD_LIST': ['CMD', 'CMD_LIST'],
    'CMD': ['if', '(', 'EXP', ')', 'CMD', 'else', 'CMD'],
  },
  
  'while': {
    'VAR_LIST': EPSILON,
    'CMD_LIST': ['CMD', 'CMD_LIST'],
    'CMD': ['while', '(', 'EXP', ')', 'CMD'],
  },
  
  'System.out.println': {
    'VAR_LIST': EPSILON,
    'CMD_LIST': ['CMD', 'CMD_LIST'],
    'CMD': ['System.out.println', '(', 'EXP', ')', ';']
  },
  
  '=': {
    'CMD_D': ['=', 'EXP', ';'],
  },
  
  '&&': {
    'EXP_R': ['&&', 'REXP', 'EXP_R'],
    'REXP_R': EPSILON,
    'AEXP_R': EPSILON,
    'MEXP_R': EPSILON,
    'PEXP_TAIL': EPSILON,
    'REST_PEXP': EPSILON,
    'REST_PEXP_TAIL': ['REST_PEXP'],
  },
  
  '<': {
    'REXP_R': ['REXP_D', 'REXP_R'],
    'REXP_D': ['<', 'AEXP'],
    'AEXP_R': EPSILON,
    'MEXP_R': EPSILON,
    'PEXP_TAIL': EPSILON,
    'REST_PEXP': EPSILON,
    'REST_PEXP_TAIL': ['REST_PEXP'],
  },
  
  '==': {
    'REXP_R': ['REXP_D', 'REXP_R'],
    'REXP_D': ['==', 'AEXP'],
    'AEXP_R': EPSILON,
    'MEXP_R': EPSILON,
    'PEXP_TAIL': EPSILON,
    'REST_PEXP': EPSILON,
    'REST_PEXP_TAIL': ['REST_PEXP'],
  },
  
  '!=': {
    'REXP_R': ['REXP_D', 'REXP_R'],
    'REXP_D': ['!=', 'AEXP'],
    'AEXP_R': EPSILON,
    'MEXP_R': EPSILON,
    'PEXP_TAIL': EPSILON,
    'REST_PEXP': EPSILON,
    'REST_PEXP_TAIL': ['REST_PEXP'],
  },

  '+': {
    'AEXP_R': ['AEXP_D', 'AEXP_R'],
    'AEXP_D': ['+', 'MEXP'],
    'MEXP_R': EPSILON,
    'PEXP_TAIL': EPSILON,
    'REST_PEXP': EPSILON,
    'REST_PEXP_TAIL': ['REST_PEXP'],
  },
  
  '-': {
    'EXP': ['REXP', 'EXP_R'],
    'REXP': ['AEXP', 'REXP_R'],
    'AEXP': ['MEXP', 'AEXP_R'],
    'AEXP_R': ['AEXP_D', 'AEXP_R'],
    'AEXP_D': ['-', 'MEXP'],
    'MEXP': ['SEXP', 'MEXP_R'],
    'MEXP_R': EPSILON,
    'SEXP': ['PREFIX', 'SEXP'],
    'PREFIX': ['-'],
    'PEXP_TAIL': EPSILON,
    'REST_PEXP': EPSILON,
    'REST_PEXP_TAIL': ['REST_PEXP'],
    'OPT_EXPS': ['EXPS'],
    'EXPS': ['EXP', 'MORE_EXPS'],
  },
  
  '*': {
    'MEXP_R': ['*', 'SEXP', 'MEXP_R'],
    'PEXP_TAIL': EPSILON,
    'REST_PEXP': EPSILON,
    'REST_PEXP_TAIL': ['REST_PEXP'],
  },
  
  '!': {
    'EXP': ['REXP', 'EXP_R'],
    'REXP': ['AEXP', 'REXP_R'],
    'AEXP': ['MEXP', 'AEXP_R'],
    'MEXP': ['SEXP', 'MEXP_R'],
    'SEXP': ['PREFIX', 'SEXP'],
    'PREFIX': ['!'],
    'OPT_EXPS': ['EXPS'],
    'EXPS': ['EXP', 'MORE_EXPS'],
  },
  
  'true': {
    'EXP': ['REXP', 'EXP_R'],
    'REXP': ['AEXP', 'REXP_R'],
    'AEXP': ['MEXP', 'AEXP_R'],
    'MEXP': ['SEXP', 'MEXP_R'],
    'SEXP': ['BASE_SXP'],
    'BASE_SXP': ['true'],
    'OPT_EXPS': ['EXPS'],
    'EXPS': ['EXP', 'MORE_EXPS'],
  },
  
  'false': {
    'EXP': ['REXP', 'EXP_R'],
    'REXP': ['AEXP', 'REXP_R'],
    'AEXP': ['MEXP', 'AEXP_R'],
    'MEXP': ['SEXP', 'MEXP_R'],
    'SEXP': ['BASE_SXP'],
    'BASE_SXP': ['false'],
    'OPT_EXPS': ['EXPS'],
    'EXPS': ['EXP', 'MORE_EXPS'],
  },
  
  'num': {
    'EXP': ['REXP', 'EXP_R'],
    'REXP': ['AEXP', 'REXP_R'],
    'AEXP': ['MEXP', 'AEXP_R'],
    'MEXP': ['SEXP', 'MEXP_R'],
    'SEXP': ['BASE_SXP'],
    'BASE_SXP': ['num'],
    'OPT_EXPS': ['EXPS'],
    'EXPS': ['EXP', 'MORE_EXPS'],
  },
  
  'null': {
    'EXP': ['REXP', 'EXP_R'],
    'REXP': ['AEXP', 'REXP_R'],
    'AEXP': ['MEXP', 'AEXP_R'],
    'MEXP': ['SEXP', 'MEXP_R'],
    'SEXP': ['BASE_SXP'],
    'BASE_SXP': ['null'],
    'OPT_EXPS': ['EXPS'],
    'EXPS': ['EXP', 'MORE_EXPS'],
  },
  
  'new int': {
    'EXP': ['REXP', 'EXP_R'],
    'REXP': ['AEXP', 'REXP_R'],
    'AEXP': ['MEXP', 'AEXP_R'],
    'MEXP': ['SEXP', 'MEXP_R'],
    'SEXP': ['BASE_SXP'],
    'BASE_SXP': ['new int', '[', 'EXP', ']'], 
    'OPT_EXPS': ['EXPS'],
    'EXPS': ['EXP', 'MORE_EXPS'],
  },
  
  '.lenght': {
    'PEXP_TAIL': ['.length'],
    'REST_PEXP': EPSILON,
    'REST_PEXP_TAIL': ['REST_PEXP'],
  },
  
  'this': {
    'EXP': ['REXP', 'EXP_R'],
    'REXP': ['AEXP', 'REXP_R'],
    'AEXP': ['MEXP', 'AEXP_R'],
    'MEXP': ['SEXP', 'MEXP_R'],
    'SEXP': ['BASE_SXP'],
    'BASE_SXP': ['PEXP', 'PEXP_TAIL'],
    'PEXP': ['this', 'REST_PEXP'],
    'OPT_EXPS': ['EXPS'],
    'EXPS': ['EXP', 'MORE_EXPS'],
  },
  
  'new': {
    'EXP': ['REXP', 'EXP_R'],
    'REXP': ['AEXP', 'REXP_R'],
    'AEXP': ['MEXP', 'AEXP_R'],
    'MEXP': ['SEXP', 'MEXP_R'],
    'SEXP': ['BASE_SXP'],
    'BASE_SXP': ['PEXP', 'PEXP_TAIL'],
    'PEXP': ['new', 'id', '(', ')', 'REST_PEXP'],
    'OPT_EXPS': ['EXPS'],
    'EXPS': ['EXP', 'MORE_EXPS'],
  },
  
  '.': {
    'REST_PEXP': ['.', 'id', 'REST_PEXP_TAIL'],
    'REST_PEXP_TAIL': ['REST_PEXP'],
  },
  
  '$': {
    'CLASSE_LIST': EPSILON,
    'VAR_LIST': EPSILON,
  }
}