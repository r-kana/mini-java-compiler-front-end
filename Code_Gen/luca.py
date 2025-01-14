from Parser.parse_tree import TreeNode


register_table = {
  'r0': '$a0',
  'sp': '$sp',
  't1': '$t1',
}

label_count = 0

def create_label():
  label_count += 1
  return f"label_{label_count}"

def stack_up():
  return f"addiu $sp $sp - 4"

def unstack():
  return f"addiu $sp $sp 4"

def store_acc():
  return f"sw $a0 0($sp)\naddiu $sp $sp -4"

def load_from_stack(reg):
  return f"lw {register_table[reg]} 4($sp)"

def add_to_acc(reg):
  return f"add $a0 {register_table[reg]} $a0"

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

def cgen_exp(exp):
  ...
  
  
def alloc_params(exps: TreeNode):
  more_exps = exps.child('MORE_EXPS')
  if (more_exps.is_empty()):
    alloc_params(more_exps)
    
  cgen(exps.child('EXP'))
  
  print(store_acc())
  
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
    # CASO: ['new int', '[', 'EXP', ']'] => Vetor de inteiros de EXP posições
    ...


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
    if (not pexp.child('REST_PEXP').is_empty()):
      cgen_rest_pexp(pexp.child('REST_PEXP'))
    ...

def cgen_rest_pexp(rest_pexp: TreeNode):
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
  #TODO: Chamar método para armazenar parametro do método
  print('sw $a0 0($sp)')
  print('addiu $sp $sp -4')
  
  
def cgen_more_exps(exps: TreeNode):
  if(not exps.children[2].is_empty()):
    cgen_more_exps(exps.children[2])
  cgen_exp(exps.children[1])
  #TODO: Chamar método para armazenar parametro do método
  print('sw $a0 0($sp)')
  print('addiu $sp $sp -4')













#cantinho do luca
#fehcado temporariamente







method_params = {
  'metodo_id': {'4': '', '8': '' }
}

def param_count(metodo_id):
  return method_params[metodo_id].count




#cantinho do luca

def cgen_metodo_list(metodo_list: TreeNode):
  cgen_metodo(metodo_list.children[0])
  if (not metodo_list.children[1].is_empty()):  
    cgen_metodo_list(metodo_list.children[1])


def cgen_metodo(metodo: TreeNode):
  print(f"{metodo.child("id").lexeme}_entry:\n")
  print("move $fp $sp")
  print("sw $ra 0($sp)")
  print("addiu $sp $sp -4")
  
  param_number = cgen_metodo_d(metodo.child('METODO_D'))
  # param_number = param_count(metodo.child("id").lexeme)
  print("lw $ra 4($sp)")
  print(f"$sp $sp {8 + 4*param_number}")
  print("lw $fp 0($sp)")
  print("jr $ra")
  


def cgen_metodo_d(metodo_d: TreeNode):
  param_number = 0
  if metodo_d.children[0].token == "PARAMS":
    metod_d_child = metodo_d.children[0].child("PARAMS_LIST")
    while metod_d_child != None: #TODO trocar para o method list
      param_number += 1
      metod_d_child = metod_d_child.child("PARAMS_LIST")
  cgen_var_list(metodo_d.child("VAR_LIST"))
  cgen_cmd_list(metodo_d.child("CMD_LIST"))
  cgen_exp(metodo_d.child("EXP"))
    
  return param_number



def cgen_var_list(var_list: TreeNode):
  pass
#   #TODO alocação extra para int[]
#   var_number = 0
#   local_variables = {}
#   current_child = var_list.child("VAR_LIST")
#   while current_child: 
#     local_variables(current_child.child("VAR").child("id").lexeme) = var_number*4
#     var_number += 1
#     current_child = current_child.child("VAR_LIST")
#   if var_number>0: 
#     (f"addiu $sp $sp -{var_number*4}")
#   return local_variables 


def cgen_cmd_list(cmd_list: TreeNode):
  cgen_cmd(cmd_list.children[0])

  if(not cmd_list.children[1].is_empty()):
      cgen_cmd_list(cmd_list.children[1])
      
      
def cgen_cmd(cmd: TreeNode):
  if cmd.children[0].token == "{":
    cgen_cmd_list(cmd.children[1])
  if cmd.children[0].token == "if":
    cgen_if(cmd.children[2],cmd.children[4],cmd.children[6])
  if cmd.children[0] == "while":
    cgen_while(cmd.child[2], cmd.children[4])
  if cmd.children[0] == "System.out.println":
    cgen_print(cmd.child[2])
  if cmd.children[0] == "id":
    cmd_d = cmd.children[1]
    if (cmd_d.children[0].token == '='):
      # CASO: CMD -> id = EXP ;
      cgen_attrib(cmd)
    else:
      # CASO: CMD -> id [ EXP ] = EXP ;
      cgen_array_attrib(cmd)
    
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

def cgen_attrib(cmd: TreeNode):
  cgen_exp(cmd.children[1])
  
  print('sw $a0 0($sp)\n')
  print('addiu $sp $sp -4\n')
  
  
def cgen_array_attrib(cmd: TreeNode):
  cmd_d = cmd.child('CMD_D')
  cgen_exp(cmd_d.children[4])
  
  print('sw $a0 0($sp)\n')
  print('addiu $sp $sp -4\n')

  cgen_exp(cmd_d.children[1])
  
  print('li $t1 4')
  print('mul $a0 $a0 $t1\n')
  print('sub $a0 $s0 $a0')
  print('lw $t1 4($sp)\n')
  print('lw $t1 $a0\n')
  
  print('addiu $sp $sp 4\n')



