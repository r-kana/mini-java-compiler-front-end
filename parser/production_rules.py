EPSILON = 'ε'

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