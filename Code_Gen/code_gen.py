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
    # CASO: ['new int', '[', 'EXP', ']'] -> Vetor de inteiros de EXP posições
    ...

def cgen_pexp(pexp: TreeNode):
  first_child = pexp.children[0]
  if (first_child.token == 'id'):
    cgen_rest_pexp()
    ...
  elif (first_child.token == '('):
    ...
  elif (first_child.token == 'this'):
    ...
  elif (first_child.token == 'new'):
    ...














#cantinho do luca
#fehcado temporariamente
