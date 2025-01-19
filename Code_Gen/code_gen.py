from Parser.parse_tree import TreeNode


register_table = {
  'r0': '$a0',
  'sp': '$sp',
  't1': '$t1',
}

current_method = ''
current_class = ''

class_call_id = ''
method_call_id = ''

class_methods= {
  # 'class1': {
  #   'vars': [
  #     {'id': '', 'offset': '-4*m'}
  #   ],
  #   'methods': {
  #     'metodoA': {
  #       'vars': [
  #         {'id': '', 'offset': '-4*m'}
  #       ],
  #       'params': [
  #         {'id': '', 'offset': '4*m'}
  #       ]
  #     }
  #   }
  # }
}

def add_method(method_id: str, class_id=None):
  if (class_id is not None):
    class_methods[class_id][method_id] = { 'vars': [], 'params': [] }
  else:
    if (method_id not in class_methods[current_class]['methods'].keys()):
      class_methods[current_method]['methods'][method_id] = { 'vars': [], 'params': [] }  


def add_var(var_id: str):
  method = class_methods[current_class]['methods'][current_method]
  position = len(class_methods[current_class]['vars']) + len(method['vars']) + 1
  method['vars'].append(
    {'id': var_id, 'offset': -4 * position }
  )


def add_param(param_id: str, position: int):
  method = class_methods[current_class]['methods'][current_method]
  if (len(method['params']) > 0):
    method['params'][position]['id'] = param_id
  else:
    position = len(method['params']) + 1
    method['params'].append(
      {'id': param_id, 'offset': 4 * position }
    )


def add_call_param(param_id: str, method_id: str, class_id: str):
  method = class_methods[class_id]['methods'][method_id]
  position = len(method['params']) + 1
  method['params'].append(
    {'id': param_id, 'offset': 4 * position }
  )


def add_class(class_id: str):
  if (class_id not in class_methods.keys()):
    class_methods[class_id] = { 'vars': [], 'methods': {} }


def add_class_var(var_id: str):
  method = class_methods[current_class]['methods'][current_method]
  position = len(class_methods[current_class]['vars']) + 1
  method['vars'].append(
    {'id': var_id, 'offset': -4 * position }
  )


def get_var(var_id: str) -> dict | None:
  method = class_methods[current_class]['methods'][current_method]
  vars = method['vars'] + method['params'] + class_methods[current_class]['vars']
  result = None
  for var in vars:
    if (var['id'] == var_id):
      result = var
  return result


def code_gen(root, level=0):
  tab = ''
  for _ in range(level):
    tab += '| '
  
  if (root.children_count != 0):
    print(f"{tab}{root.token}:")
    level += 1
    for child in root.children:
      code_gen(child, level)
  else:
    # if(root.token != 'ε'):
    print(f"{tab}( {root.token} ): {root.lexeme}")

############################# CGEN METHODS #############################

def cgen_prog(prog: TreeNode):
  cgen_main(prog.children[0])
  cgen_class_list(prog.children[1])


def cgen_main(main: TreeNode):
  cgen_cmd(main.child('CMD'))


def cgen_class_list(class_list: TreeNode):
  cgen_class(class_list.children[0])
  if (not class_list.children[1].is_empty()):
    cgen_class_list(class_list.children[1])


def cgen_class(classe: TreeNode):
  add_class(classe.children[1].lexeme)
  current_class = classe.children[1].lexeme
  cgen_classe_d(classe.children[2])
  if (not classe.children[3].is_empty()):
    cgen_class_list(classe.children[3])


def cgen_classe_d(classe_d: TreeNode):
  if (classe_d.children[0].token == 'extends'):
    cgen_class_var_list(classe_d.children[3])
    cgen_metodo_list(classe_d.children[4])
  else:
    cgen_class_var_list(classe_d.children[1])
    cgen_metodo_list(classe_d.children[2])


def cgen_class_var_list(var_list: TreeNode):
  add_class_var(var_list.children[0].children[1].lexeme)
  if (not var_list.children[1].is_empty()):
    cgen_class_var_list(var_list.children[1])


def cgen_metodo_list(metodo_list: TreeNode):
  cgen_metodo(metodo_list.children[0])
  if (not metodo_list.children[1].is_empty()):  
    cgen_metodo_list(metodo_list.children[1])


def cgen_metodo(metodo: TreeNode):
  add_method(metodo.children[2].lexeme)
  current_method = metodo.children[2].lexeme
  
  print(f"{metodo.child('id').lexeme}_entry:\n")
  print("move $fp $sp")
  print("sw $ra 0($sp)")
  print("addiu $sp $sp -4")
  
  cgen_metodo_d(metodo.child('METODO_D'))
  vars_len = len(class_methods[current_class][current_method]['vars'])
  paras_len = len(class_methods[current_class][current_method]['params'])
  
  print("lw $ra 4($sp)")
  print(f"$sp $sp {8 + 4 * (vars_len + paras_len)}")
  print("lw $fp 0($sp)")
  print("jr $ra")


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
  
  print('addiu $sp $sp -4')
  
  if (not var_list.children[1].is_empty()):
    cgen_var_list(var_list.children[1])


def cgen_class_vars():
  for _ in class_methods[current_class]['vars']:
    print('addiu $sp $sp -4')


def cgen_cmd_list(cmd_list: TreeNode):
  cgen_cmd(cmd_list.children[0])
  if(not cmd_list.children[1].is_empty()):
    cgen_cmd_list(cmd_list.children[1])


def cgen_cmd(cmd: TreeNode): #NOTE - cgen_cmd
  if cmd.children[0].token == "{":
    cgen_cmd_list(cmd.children[1])
    
  if cmd.children[0].token == "if":
    cgen_if(cmd.children[2],cmd.children[4],cmd.children[6])
    
  if cmd.children[0] == "while":
    cgen_while(cmd.child[2], cmd.children[4])
    
  if cmd.children[0] == "System.out.println":
    cgen_print(cmd.child[2])
    
  if cmd.children[0] == "id":
    # CASO: CMD -> id CMD_D
    if (cmd.children[1].children[0].token == '='):
      # CASO: CMD -> id CMD_D
      # CASO: CMD_D -> = EXP ;
      cgen_attribution(cmd)
    else:
      # CASO: CMD_D -> [ EXP ] = EXP ;
      # CASO: CMD -> id [ EXP ] = EXP ;
      cgen_array_attribution(cmd)


def cgen_if(if_expression: TreeNode, then_cmd: TreeNode, else_cmd: TreeNode ):
  label = create_label()
  cgen(if_expression)
  
  print(f"beq $a0, $zero {label}_if_false")
  
  cgen(then_cmd)
  
  print(f"b {label}_end_if")
  print(f"{label}_if_false:")
  
  cgen_cmd(else_cmd)
  
  print(f"{label}_end_if:")
  print()


def cgen_while(condition_expression: TreeNode, cmd_instructions: TreeNode):
  label = create_label()
  
  print(f"{label}_start:")
  
  cgen_exp(condition_expression)
  
  print(f"beq $a0, $zero, {label}_end")
  
  cgen_cmd(cmd_instructions)
  
  print(f"J {label}_start")
  print(f"{label}_end:")


def cgen_print(exp: TreeNode):
  cgen_exp(exp)
  
  print("li $v0, 1")
  print("syscall")


def cgen_attribution(cmd: TreeNode):
  # CASO: CMD -> id CMD_D
  # CASO: CMD_D -> = EXP ;
  var_id = cmd.children[0].lexeme
  offset = get_var(var_id)['offset']
  cmd_d = cmd.children[1]
  cgen_exp(cmd_d.children[1])
  
  print(f'sw $a0 {offset}($fp)\n')


def cgen_array_attribution(cmd: TreeNode):
  var_id = cmd.children[0].lexeme
  offset = get_var(var_id)['offset']
  
  cmd_d = cmd.child('CMD_D')
  cgen_exp(cmd_d.children[4]) # Valor
  
  print('sw $a0 0($sp)\n')
  print('addiu $sp $sp -4\n')

  cgen_exp(cmd_d.children[1]) # Array index
  
  print('li $t1 4')
  print('mul $a0 $a0 $t1\n')
  
  print(f'lw $t1 {offset}($fp)')
  print('sub $a0 $t1 $a0')
  print('lw $t1 4($sp)\n')
  print('sw $t1 $a0\n')
  
  print('addiu $sp $sp 4\n')


def cgen_exp(exp: TreeNode):
  if (not exp.child('EXP_R').is_empty()):
    cgen_and(exp)
  else:
    cgen_rexp(exp.child('REXP'))


def cgen_rexp(rexp: TreeNode):
  if (not rexp.child('REXP_R').is_empty()):
    cgen_compare(rexp)
  else:
    cgen_aexp(rexp.child('AEXP'))


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
  
  print('sw $a0 0($sp)\n')
  print('addiu $sp $sp -4\n')
  
  mexp = aexp.child('AEXP_R').child('AEXP_D').child('MEXP')
  cgen_mexp(mexp)
  
  print('lw $t1 4($sp)\n')
  print('add $a0 $t1 $a0\n')
  print('addiu $sp $sp 4\n')
  
  next_aexp_r = aexp.child('AEXP_R').child('AEXP_R')
  if (not next_aexp_r.is_empty()):
    if (next_aexp_r.child('AEXP_D').children[0] == '+'):
      cgen_next_add(next_aexp_r)
    else:
      cgen_next_sub(next_aexp_r)


def cgen_sub(aexp: TreeNode):
  cgen_mexp(aexp.child('MEXP'))
  
  print('sw $a0 0($sp)\n')
  print('addiu $sp $sp -4\n')
  
  mexp = aexp.child('AEXP_R').child('AEXP_D').child('MEXP')
  cgen_mexp(mexp)
  
  print('lw $t1 4($sp)\n')
  print('sub $a0 $t1 $a0\n')
  print('addiu $sp $sp 4\n')
  
  next_aexp_r = aexp.child('AEXP_R').child('AEXP_R')
  if (not next_aexp_r.is_empty()):
    if (next_aexp_r.child('AEXP_D').children[0] == '+'):
      cgen_next_add(next_aexp_r)
    else:
      cgen_next_sub(next_aexp_r)


def cgen_next_add(aexp_r: TreeNode):
  print('sw $a0 0($sp)\n')
  print('addiu $sp $sp -4\n')
  
  mexp = aexp_r.child('AEXP_D').child('MEXP')
  cgen_mexp(mexp)
  
  print('lw $t1 4($sp)\n')
  print('add $a0 $t1 $a0\n')
  print('addiu $sp $sp 4\n')
  
  next_aexp_r = aexp_r.child('AEXP_R')
  if (not next_aexp_r.is_empty()):
    if (next_aexp_r.child('AEXP_D').children[0] == '+'):
      cgen_next_add(next_aexp_r)
    else:
      cgen_next_sub(next_aexp_r)


def cgen_next_sub(aexp_r: TreeNode):
  print('sw $a0 0($sp)\n')
  print('addiu $sp $sp -4\n')
  
  mexp = aexp_r.child('AEXP_D').child('MEXP')
  cgen_mexp(mexp)
  
  print('lw $t1 4($sp)\n')
  print('sub $a0 $t1 $a0\n')
  print('addiu $sp $sp 4\n')
  
  next_aexp_r = aexp_r.child('AEXP_R')
  if (not next_aexp_r.is_empty()):
    if (next_aexp_r.child('AEXP_D').children[0] == '+'):
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
  
  print('sw $a0 0($sp)\n')
  print('addiu $sp $sp -4\n')
  
  mexp_r = mexp.child('MEXP_R')
  cgen_sexp(mexp_r.child('SEXP'))

  print('lw $t1 4($sp)\n')
  print('mul $a0 $t1 $a0\n')
  print('addiu $sp $sp 4\n')

  next_mexp_r = mexp_r.child('MEXP_R')
  if(not next_mexp_r.is_empty()):
    cgen_next_mul(next_mexp_r)


def cgen_next_mul(mexp_r: TreeNode):
  print('sw $a0 0($sp)\n')
  print('addiu $sp $sp -4\n')
  
  cgen_sexp(mexp_r.child('SEXP'))

  print('lw $t1 4($sp)\n')
  print('mul $a0 $t1 $a0\n')
  print('addiu $sp $sp 4\n')

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
    print('li $a0 1\n')

  elif (first_child.token == 'false'):
    print('li $a0 0\n')

  elif (first_child.token == 'num'):
    print(f"li $a0 {first_child.lexeme}\n")

  elif (first_child.token == 'null'):
    print('li $a0 0\n')

  elif (first_child.token == 'new int'):
    # CASO:  new int [ EXP ]
    cgen_alloc_array(base_exp.children[2])


def cgen_alloc_array(exp: TreeNode):
    cgen_exp(exp) # $a0 contem o tamanho do vetor
    print('li $t1 4\n')
    print('mul $t1 $t1 $a0\n') # $t1 tem 4 * $a0
    print('move $a0 $sp') # $a0 aponta para o inicio da lista
    print('sub $sp $sp $t1\n')


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
    if (not pexp.child('REST_PEXP').is_empty()):
      cgen_rest_pexp(pexp.child('REST_PEXP'))
    ...
  elif (first_child.token == '('):
    #CASO: BASE_SXP -> ( EXP ) REST_PEXP PEXP_TAIL
    cgen_exp(pexp.child('EXP'))
    if (not pexp.child('REST_PEXP').is_empty()):
      cgen_rest_pexp(pexp.child('REST_PEXP'))
    ...
  elif (first_child.token == 'this'):
    if (not pexp.child('REST_PEXP').is_empty()):
      cgen_rest_pexp(pexp.child('REST_PEXP'))
    ...
  elif (first_child.token == 'new'):
    #CASO: PEXP -> new id ( ) REST_PEXP => Instancia de classe
    add_class(pexp.children[1].lexeme)
    class_call_id = pexp.children[1].lexeme
    if (not pexp.child('REST_PEXP').is_empty()):
      cgen_rest_pexp(pexp.child('REST_PEXP'))


def cgen_rest_pexp(rest_pexp: TreeNode):
  if (rest_pexp.parent.children[0] == 'new'):
    class_id = rest_pexp.parent.children[1].lexeme
    method_id = rest_pexp.children[1].lexeme
    add_method(method_id, class_id)
    method_call_id = method_id
        
  cgen_rest_pexp_tail(rest_pexp.child('REST_PEXP_TAIL'))


def cgen_rest_pexp_tail(rest_pexp_tail: TreeNode):
  first_child = rest_pexp_tail.children[0]
  if (first_child.token == 'REST_PESP'):
    cgen_rest_pexp(first_child)
  else:
    #CASO: REST_PEXP_TAIL -> ( OPT_EXPS ) REST_PEXP
    opt_exps = first_child.child('OPT_EXPS')
    if (not opt_exps.is_empty()):
      cgen_opt_exps(opt_exps)
    
    cgen_rest_pexp(first_child.child('REST_PEXP'))


def cgen_opt_exps(opt_exps: TreeNode):
  #CASO: REST_PEXP -> . id ( EXPS ) REST_PEXP => Chama de função. 
  #   EXPS são parametros da função
  metodo_id = opt_exps.parent.parent.child('id').lexeme
  print('sw $fp 0($sp)\n')
  print('addiu $sp $sp -4\n')
  
  cgen_exps(opt_exps.children[0])
  
  print('sw $a0 0($sp)\n')
  print('addiu $sp $sp -4\n')
  print(f"jal {metodo_id}_entry\n")


def cgen_exps(exps: TreeNode):
  if(not exps.children[1].is_empty()):
    cgen_more_exps(exps.children[1])
  cgen_exp(exps.children[0])
  add_call_param('', method_call_id, class_call_id)
  
  print('sw $a0 0($sp)')
  print('addiu $sp $sp -4')
  
  
def cgen_more_exps(exps: TreeNode):
  if(not exps.children[2].is_empty()):
    cgen_more_exps(exps.children[2])
  cgen_exp(exps.children[1])
  add_call_param('', method_call_id, class_call_id)
  
  print('sw $a0 0($sp)')
  print('addiu $sp $sp -4')