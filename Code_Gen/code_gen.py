from Parser.parse_tree import TreeNode


register_table = {
  'r0': '$a0',
  'sp': '$sp',
  't1': '$t1',
}

label_counter = 0

def create_label() -> str:
  global label_counter
  label_counter += 1 
  return f'label{label_counter}'

current_method = ''
current_class = ''

class_call_id = ''
method_call_id = ''

def set_method_call_id(method_id: str):
  global method_call_id
  method_call_id = method_id


def get_method_call_id() -> str:
  global method_call_id
  return method_call_id


def set_class_call_id(class_id: str):
  global class_call_id
  class_call_id = class_id

CLASS_METHODS = {}

def get_current_class() -> str:
  global current_class
  return current_class


def set_current_class (class_id: str):
  global current_class
  current_class = class_id


def get_current_method() -> str:
  global current_method
  return current_method


def set_current_method (method_id: str):
  global current_method
  current_method = method_id


def add_method(method_id: str, class_id=None):
  global current_method
  global current_class
  if (class_id is not None):
    CLASS_METHODS[class_id]['methods'][method_id] = { 'vars': [], 'params': [] }
  else:
    if (method_id not in CLASS_METHODS[current_class]['methods'].keys()):
      CLASS_METHODS[current_class]['methods'][method_id] = { 'vars': [], 'params': [] }  


def add_var(var_id: str):
  global current_method
  global current_class
  method = CLASS_METHODS[current_class]['methods'][current_method]
  position = len(CLASS_METHODS[current_class]['vars']) + len(method['vars']) + 1
  method['vars'].append(
    {'id': var_id, 'offset': -4 * position }
  )


def add_param(param_id: str, position: int):
  global current_method
  global current_class
  method = CLASS_METHODS[current_class]['methods'][current_method]
  if (len(method['params']) > 0):
    method['params'][position]['id'] = param_id
  else:
    position = len(method['params']) + 1
    method['params'].append(
      {'id': param_id, 'offset': 4 * position }
    )


def add_call_param(param_id: str, method_id: str, class_id: str):
  method = CLASS_METHODS[class_id]['methods'][method_id]
  position = len(method['params']) + 1
  method['params'].append(
    {'id': param_id, 'offset': 4 * position }
  )


def add_class(class_id: str):
  if (class_id not in CLASS_METHODS.keys()):
    CLASS_METHODS[class_id] = { 'vars': [], 'methods': {} }


def add_class_var(var_id: str):
  global current_class
  position = len(CLASS_METHODS[current_class]['vars']) + 1
  CLASS_METHODS[current_class]['vars'].append(
    {'id': var_id, 'offset': -4 * position }
  )


def get_var(var_id: str) -> dict | None:
  global current_method
  global current_class
  method = CLASS_METHODS[current_class]['methods'][current_method]
  vars = method['vars'] + method['params'] + CLASS_METHODS[current_class]['vars']
  result = None
  for var in vars:
    if (var['id'] == var_id):
      result = var
  return result


def print_ast(root, level=0):
  tab = ''
  for _ in range(level):
    tab += '| '
  
  if (root.children_count != 0):
    print(f"{tab}{root.token}:")
    level += 1
    for child in root.children:
      print_ast(child, level)
  else:
    # if(root.token != 'ε'):
    print(f"{tab}( {root.token} ): {root.lexeme}")
    
def code_gen(root):
  cgen_prog(root.children[0])


############################# CGEN METHODS #############################

def cgen_prog(prog: TreeNode):
  cgen_main(prog.children[0])
  cgen_class_list(prog.children[1])
  print('prog_end:\n')


def cgen_main(main: TreeNode):
  cgen_cmd(main.child('CMD'))
  print('j prog_end\n')


def cgen_class_list(class_list: TreeNode):
  cgen_class(class_list.children[0])
  if (not class_list.children[1].is_empty()):
    cgen_class_list(class_list.children[1])


def cgen_class(classe: TreeNode):
  add_class(classe.children[1].lexeme)
  set_current_class(classe.children[1].lexeme)
  cgen_classe_d(classe.children[2])


def cgen_classe_d(classe_d: TreeNode):
  var_list = classe_d.child('VAR_LIST')
  metodo_list = classe_d.child('METODO_LIST')
  if (not var_list.is_empty()):
    cgen_class_var_list(var_list)
    
  if (not metodo_list.is_empty()):
    cgen_metodo_list(metodo_list)


def cgen_class_var_list(var_list: TreeNode):
  add_class_var(var_list.children[0].children[1].lexeme)
  if (not var_list.children[1].is_empty()):
    cgen_class_var_list(var_list.children[1])


def cgen_metodo_list(metodo_list: TreeNode):
  cgen_metodo(metodo_list.children[0])
  if (not metodo_list.children[1].is_empty()):  
    cgen_metodo_list(metodo_list.children[1])


def cgen_metodo(metodo: TreeNode):
  global current_class
  
  set_current_method(metodo.children[2].lexeme)
  add_method(metodo.children[2].lexeme)
  
  print(f"{metodo.child('id').lexeme}_entry:\n")
  print("move $fp, $sp\n")
  print("sw $ra, 0($sp)\n")
  print("addiu $sp, $sp, -4\n")
  
  cgen_metodo_d(metodo.child('METODO_D'))
  current_method = get_current_method()
  class_vars_len = len(CLASS_METHODS[current_class]['vars'])
  vars_len = len(CLASS_METHODS[current_class]['methods'][current_method]['vars'])
  params_len = len(CLASS_METHODS[current_class]['methods'][current_method]['params'])
  
  print(f"lw $ra, {4 * (class_vars_len + vars_len + 1)}($sp)\n") # offset = method vars + class vars
  print(f"addiu $sp, $sp, {8 + 4 * (vars_len + params_len + class_vars_len)}\n")
  print("lw $fp, 0($sp)\n")
  print("jr $ra\n")


def cgen_metodo_d(metodo_d: TreeNode): 
  if (metodo_d.children[0].token == "PARAMS"):
    cgen_params(metodo_d.children[0], 0) # Nomeando parâmetros
    
  cgen_class_vars() # Alocando variáveis da classe
  cgen_var_list(metodo_d.child("VAR_LIST")) # Alocando variáveis
  cgen_cmd_list(metodo_d.child("CMD_LIST"))
  cgen_exp(metodo_d.child("EXP"))


def cgen_params(params: TreeNode, position: int):
  add_param(params.children[1].lexeme, position)
  if (not params.children[2].is_empty()):
    position += 1
    cgen_params_list(params.children[2], position)


def cgen_params_list(params_list: TreeNode, position: int):
  add_param(params_list.children[2].lexeme, position)
  if (not params_list.children[3].is_empty()):
    position += 1
    cgen_params_list(params_list.children[3], position)


def cgen_var_list(var_list: TreeNode):
  add_var(var_list.children[0].children[1].lexeme)
  
  print('addiu $sp, $sp, -4\n')
  
  if (not var_list.children[1].is_empty()):
    cgen_var_list(var_list.children[1])


def cgen_class_vars():
  global current_class
  
  for _ in CLASS_METHODS[current_class]['vars']:
    print('addiu $sp, $sp, -4\n')


def cgen_cmd_list(cmd_list: TreeNode):
  cgen_cmd(cmd_list.children[0])
  if(not cmd_list.children[1].is_empty()):
    cgen_cmd_list(cmd_list.children[1])


def cgen_cmd(cmd: TreeNode):
  first_child = cmd.children[0]
  if first_child.token == "{":
    cgen_cmd_list(cmd.children[1])
    
  elif first_child.token == "if":
    cgen_if(cmd)
    
  elif first_child.token == "while":
    cgen_while(cmd)
    
  elif first_child.token == "System.out.println":
    cgen_print(cmd.children[2])
    
  elif first_child.token == "id":
    # CASO: CMD -> id CMD_D
    if (cmd.children[1].children[0].token == '='):
      # CASO: CMD -> id CMD_D
      # CASO: CMD_D -> = EXP ;
      cgen_attribution(cmd)
    else:
      # CASO: CMD_D -> [ EXP ] = EXP ;
      # CASO: CMD -> id [ EXP ] = EXP ;
      cgen_array_attribution(cmd)


def cgen_if(cmd: TreeNode):
  # CMD -> if ( EXP ) CMD else CMD
  label = create_label()
  cgen_exp(cmd.children[2])
  
  print(f"beq $a0, $zero, {label}_if_false\n")
  
  cgen_cmd(cmd.children[4])
  
  print(f"b {label}_end_if\n")
  print(f"{label}_if_false:\n")
  
  cgen_cmd(cmd.children[6])
  
  print(f"{label}_end_if:\n")


def cgen_while(cmd: TreeNode):
  # while ( EXP ) CMD
  label = create_label()
  
  print(f"{label}_start:\n")
  
  cgen_exp(cmd.children[2])
  
  print(f"beq $a0, $zero, {label}_end\n")
  
  cgen_cmd(cmd.children[4])
  
  print(f"j {label}_start\n")
  print(f"{label}_end:\n")


def cgen_print(exp: TreeNode):
  cgen_exp(exp)
  
  print("li $v0, 1\n")
  print("syscall\n")


def cgen_attribution(cmd: TreeNode):
  # CASO: CMD -> id CMD_D
  # CASO: CMD_D -> = EXP ;
  var_id = cmd.children[0].lexeme
  offset = get_var(var_id)['offset']
  cmd_d = cmd.children[1]
  cgen_exp(cmd_d.children[1])
  
  print(f'sw $a0, {offset}($fp)\n')


def cgen_array_attribution(cmd: TreeNode):
  var_id = cmd.children[0].lexeme
  offset = get_var(var_id)['offset']
  
  cmd_d = cmd.child('CMD_D')
  cgen_exp(cmd_d.children[4]) # Valor
  
  print('sw $a0, 0($sp)\n')
  print('addiu $sp, $sp, -4\n')

  cgen_exp(cmd_d.children[1]) # Array index
  
  print('li $t1, 4\n')
  print('mul $a0, $a0, $t1\n')
  
  print(f'lw $t1, {offset}($fp)\n')
  print('sub $a0, $t1, $a0\n')
  print('lw $t1, 4($sp)\n')
  print('sw $t1, 0($a0)\n')
  
  print('addiu $sp, $sp, 4\n')


def cgen_exp(exp: TreeNode):
  if (not exp.child('EXP_R').is_empty()):
    cgen_and(exp)
  else:
    cgen_rexp(exp.child('REXP'))


def cgen_and(exp: TreeNode):
  # EXP -> REXP EXP_R( && REXP EXP_R )
  label = create_label()
  cgen_rexp(exp.child('REXP'))
  
  print(f'beq $a0, $zero, {label}_and_false\n')
  
  exp_r = exp.child('EXP_R')
  cgen_rexp(exp_r.child('REXP'))
  
  print(f'beq $a0, $zero, {label}_and_false\n')
  print('li $a0, 1\n')
  print(f'j {label}_and_end\n')
  print(f'{label}_and_false:\n')
  print('li $a0, 1\n')
  print(f'{label}_and_end:\n')
  
  if(not exp_r.child('EXP_R').is_empty()):
    cgen_next_and(exp_r.child('EXP_R'))


def cgen_next_and(exp_r: TreeNode):
  label = create_label()
  
  print(f'beq $a0, $zero, {label}_and_false\n')
  
  cgen_rexp(exp_r.child('REXP'))
  
  print(f'beq $a0, $zero, {label}_and_false\n')
  print('li $a0, 1\n')
  print('j _and_end\n')
  print(f'{label}_and_false:\n')
  print('li $a0, 1\n')
  print(f'{label}_and_end:\n')
  
  if(not exp_r.child('EXP_R').is_empty()):
    cgen_next_and(exp_r)


def cgen_rexp(rexp: TreeNode):
  if (not rexp.child('REXP_R').is_empty()):
    cgen_compare(rexp)
  else:
    cgen_aexp(rexp.child('AEXP'))


def cgen_compare(rexp: TreeNode, next=False):
  if (not next):
    cgen_aexp(rexp.child('AEXP'))
  
  comparison_type = rexp.child('REXP_R').child('REXP_D').children[0]
  if (comparison_type == '<'):
    cgen_grt_than(rexp.child('REXP_R'))
    
  elif (comparison_type == '=='):
    cgen_equality(rexp.child('REXP_R'))
    
  elif (comparison_type == '!='):
    cgen_difference(rexp.child('REXP_R'))


def cgen_grt_than(rexp_r: TreeNode):
  print('sw $a0, 0($sp)\n')
  print('addiu $sp, $sp, -4\n')
  
  cgen_aexp(rexp_r.child('REXP_D').child('AEXP'))
  
  print('lw $t1, 4($sp)\n')
  print('slt $a0, $t1, $a0\n')
  print('addiu $sp, $sp, 4\n')
  
  if (not rexp_r.child('REXP_R').is_empty()):
    cgen_compare(rexp_r.child('REXP_R'), True)


def cgen_equality(rexp_r: TreeNode):
  print('sw $a0, 0($sp)\n')
  print('addiu $sp, $sp, -4\n')
  
  cgen_aexp(rexp_r.child('REXP_D').child('AEXP'))
  
  print('lw $t1, 4($sp)\n')
  print('xor $a0, $t1, $a0\n')
  print('slti $a0, $a0, 1\n')
  print('addiu $sp, $sp, 4\n')
  
  if (not rexp_r.child('REXP_R').is_empty()):
    cgen_compare(rexp_r.child('REXP_R'), True)
  pass


def cgen_difference(rexp_r: TreeNode):
  print('sw $a0, 0($sp)\n')
  print('addiu $sp, $sp, -4\n')
  
  cgen_aexp(rexp_r.child('REXP_D').child('AEXP'))
  
  print('lw $t1, 4($sp)\n')
  print('xor $a0, $t1, $a0\n')
  print('sltu $a0, $zero, $a0\n')
  print('addiu $sp, $sp, 4\n')
  
  if (not rexp_r.child('REXP_R').is_empty()):
    cgen_compare(rexp_r.child('REXP_R'), True)


def cgen_aexp(aexp: TreeNode):
  aexp_r = aexp.child('AEXP_R')
  if (not aexp_r.is_empty()):
    if (aexp_r.child('AEXP_D').children[0].token == '+'):
      cgen_add(aexp)
    else:
      cgen_sub(aexp)
  else:
    cgen_mexp(aexp.child('MEXP'))


def cgen_add(aexp: TreeNode): 
  cgen_mexp(aexp.child('MEXP'))
  
  print('sw $a0, 0($sp)\n')
  print('addiu $sp, $sp, -4\n')
  
  mexp = aexp.child('AEXP_R').child('AEXP_D').child('MEXP')
  cgen_mexp(mexp)
  
  print('lw $t1, 4($sp)\n')
  print('add $a0, $t1, $a0\n')
  print('addiu $sp, $sp, 4\n')
  
  next_aexp_r = aexp.child('AEXP_R').child('AEXP_R')
  if (not next_aexp_r.is_empty()):
    if (next_aexp_r.child('AEXP_D').children[0].token == '+'):
      cgen_next_add(next_aexp_r)
    else:
      cgen_next_sub(next_aexp_r)


def cgen_sub(aexp: TreeNode):
  cgen_mexp(aexp.child('MEXP'))
  
  print('sw $a0, 0($sp)\n')
  print('addiu $sp, $sp, -4\n')
  
  mexp = aexp.child('AEXP_R').child('AEXP_D').child('MEXP')
  cgen_mexp(mexp)
  
  print('lw $t1, 4($sp)\n')
  print('sub $a0, $t1, $a0\n')
  print('addiu $sp, $sp, 4\n')
  
  next_aexp_r = aexp.child('AEXP_R').child('AEXP_R')
  if (not next_aexp_r.is_empty()):
    if (next_aexp_r.child('AEXP_D').children[0].token == '+'):
      cgen_next_add(next_aexp_r)
    else:
      cgen_next_sub(next_aexp_r)


def cgen_next_add(aexp_r: TreeNode):
  print('sw $a0, 0($sp)\n')
  print('addiu $sp, $sp, -4\n')
  
  mexp = aexp_r.child('AEXP_D').child('MEXP')
  cgen_mexp(mexp)
  
  print('lw $t1, 4($sp)\n')
  print('add $a0, $t1, $a0\n')
  print('addiu $sp, $sp, 4\n')
  
  next_aexp_r = aexp_r.child('AEXP_R')
  if (not next_aexp_r.is_empty()):
    if (next_aexp_r.child('AEXP_D').children[0].token == '+'):
      cgen_next_add(next_aexp_r)
    else:
      cgen_next_sub(next_aexp_r)


def cgen_next_sub(aexp_r: TreeNode):
  print('sw $a0, 0($sp)\n')
  print('addiu $sp, $sp, -4\n')
  
  mexp = aexp_r.child('AEXP_D').child('MEXP')
  cgen_mexp(mexp)
  
  print('lw $t1, 4($sp)\n')
  print('sub $a0, $t1, $a0\n')
  print('addiu $sp, $sp, 4\n')
  
  next_aexp_r = aexp_r.child('AEXP_R')
  if (not next_aexp_r.is_empty()):
    if (next_aexp_r.child('AEXP_D').children[0].token == '+'):
      cgen_next_add(next_aexp_r)
    else:
      cgen_next_sub(next_aexp_r)


def cgen_mexp(mexp: TreeNode):
  if (not mexp.child('MEXP_R').is_empty()):
    cgen_mul(mexp)
  else:
    cgen_sexp(mexp.child('SEXP'))


def cgen_mul(mexp: TreeNode):
  cgen_sexp(mexp.child('SEXP'))
  
  print('sw $a0, 0($sp)\n')
  print('addiu $sp, $sp, -4\n')
  
  mexp_r = mexp.child('MEXP_R')
  cgen_sexp(mexp_r.child('SEXP'))

  print('lw $t1, 4($sp)\n')
  print('mul $a0, $t1, $a0\n')
  print('addiu $sp, $sp, 4\n')

  next_mexp_r = mexp_r.child('MEXP_R')
  if(not next_mexp_r.is_empty()):
    cgen_next_mul(next_mexp_r)


def cgen_next_mul(mexp_r: TreeNode):
  print('sw $a0, 0($sp)\n')
  print('addiu $sp, $sp, -4\n')
  
  cgen_sexp(mexp_r.child('SEXP'))

  print('lw $t1, 4($sp)\n')
  print('mul $a0, $t1, $a0\n')
  print('addiu $sp, $sp, 4\n')

  next_mul = mexp_r.child('MEXP_R')
  if(not next_mul.is_empty()):
    cgen_next_mul(next_mul)


def cgen_sexp(sexp: TreeNode):
  if (sexp.children[0].token == 'PREFIX'):
    cgen_sexp(sexp.child('SEXP'))
    
    print('subu $a0, $zero, $a0\n')
    
  else:
    cgen_base_exp(sexp.child('BASE_SXP'))


def cgen_base_exp(base_exp: TreeNode):
  first_child = base_exp.children[0]
  if(first_child.token == 'PEXP'):
    cgen_pexp(first_child)
    
    pexp_tail = base_exp.child('PEXP_TAIL')
    if(not pexp_tail.is_empty()):
      cgen_pexp_tail(pexp_tail)
    
  elif (first_child.token == 'true'):
    print('li $a0, 1\n')

  elif (first_child.token == 'false'):
    print('li $a0, 0\n')

  elif (first_child.token == 'num'):
    print(f"li $a0, {first_child.lexeme}\n")

  elif (first_child.token == 'null'):
    print('li $a0, 0\n')

  elif (first_child.token == 'new int'):
    # CASO:  new int [ EXP ]
    cgen_alloc_array(base_exp.children[2])


def cgen_alloc_array(exp: TreeNode):
    cgen_exp(exp)               # $a0 contem o tamanho do vetor
    
    print('li $t1, 4\n')
    print('mul $t1, $t1, $a0\n')  # $t1 tem 4 * $a0
    print('move $a0, $sp\n')       # $a0 aponta para o inicio da lista
    print('sub $sp, $sp, $t1\n')


def cgen_pexp_tail(pexp_tail: TreeNode):
  first_child = pexp_tail.children[0]
  if (first_child.token == '['):
    #CASO: PEXP_TAIL -> [ EXP ] => Vetor de EXP posições
    cgen_exp(first_child.children[1])
  else:
    #CASO: PEXP_TAIL -> .length
    # TODO: Implementar funcao que recupera o tamanho de um vetor
    ...


def cgen_pexp(pexp: TreeNode):
  first_child = pexp.children[0]
  if (first_child.token == 'id'):
    offset = get_var(first_child.lexeme)['offset']
    
    if (pexp.child('REST_PEXP').is_empty()):
      pexp_tail = pexp.parent.child('PEXP_TAIL')
      if(pexp_tail.children[0] == '['):
        # PEXP_TAIL -> [ EXP ]
        cgen_exp(pexp_tail.children[1])
        
        print('li $t1, 4\n')
        print('mul $a0, $a0, $t1\n')
        
        print(f'lw $t1, {offset}($fp)\n')
        print('sub $a0, $t1, $a0\n')
        print('lw $a0, 0($a0)\n')
        
      elif(pexp.parent.child('PEXP_TAIL').is_empty()):
        print(f'lw $a0, {offset}($fp)\n')
        
    else:
      cgen_rest_pexp(pexp.child('REST_PEXP'))
    
  elif (first_child.token == '('):
    #CASO: BASE_SXP -> ( EXP ) REST_PEXP PEXP_TAIL
    cgen_exp(pexp.child('EXP'))
    if (not pexp.child('REST_PEXP').is_empty()):
      cgen_rest_pexp(pexp.child('REST_PEXP'))
    
  elif (first_child.token == 'this'):
    if (not pexp.child('REST_PEXP').is_empty()):
      cgen_rest_pexp(pexp.child('REST_PEXP'))
    
  elif (first_child.token == 'new'):
    #CASO: PEXP -> new id ( ) REST_PEXP => Instancia de classe
    add_class(pexp.children[1].lexeme)
    set_class_call_id(pexp.children[1].lexeme)
    if (not pexp.child('REST_PEXP').is_empty()):
      cgen_rest_pexp(pexp.child('REST_PEXP'))


def cgen_rest_pexp(rest_pexp: TreeNode):
  if (rest_pexp.parent.children[0].token == 'new'):
    class_id = rest_pexp.parent.children[1].lexeme
    method_id = rest_pexp.children[1].lexeme
    add_method(method_id, class_id)
    set_method_call_id(method_id)

  cgen_rest_pexp_tail(rest_pexp.child('REST_PEXP_TAIL'))


def cgen_rest_pexp_tail(rest_pexp_tail: TreeNode):
  first_child = rest_pexp_tail.children[0]
  if (first_child.token == 'REST_PEXP'):
    if(not first_child.is_empty()):
      cgen_rest_pexp(first_child)
  else:
    #CASO: REST_PEXP_TAIL -> ( OPT_EXPS ) REST_PEXP
    opt_exps = rest_pexp_tail.child('OPT_EXPS')
    if (not opt_exps.is_empty()):
      cgen_opt_exps(opt_exps)

    rest_pexp = rest_pexp_tail.child('REST_PEXP')
    if (not rest_pexp.is_empty()):
      cgen_rest_pexp(rest_pexp)


def cgen_opt_exps(opt_exps: TreeNode):
  #CASO: REST_PEXP -> . id ( EXPS ) REST_PEXP => Chama de função. 
  #   EXPS são parametros da função
  metodo_id = opt_exps.parent.parent.child('id').lexeme
  print('sw $fp, 0($sp)\n')
  print('addiu $sp, $sp, -4\n')
  
  cgen_exps(opt_exps.children[0])
  
  print(f"jal {metodo_id}_entry\n")


def cgen_exps(exps: TreeNode):
  global class_call_id
  global method_call_id
  if(not exps.children[1].is_empty()):
    cgen_more_exps(exps.children[1])
  cgen_exp(exps.children[0])
  add_call_param('', method_call_id, class_call_id)
  
  print('sw $a0, 0($sp)\n')
  print('addiu $sp, $sp, -4\n')


def cgen_more_exps(exps: TreeNode):
  global class_call_id
  global method_call_id
  if(not exps.children[2].is_empty()):
    cgen_more_exps(exps.children[2])
  cgen_exp(exps.children[1])
  add_call_param('', method_call_id, class_call_id)
  
  print('sw $a0, 0($sp)\n')
  print('addiu $sp, $sp, -4\n')