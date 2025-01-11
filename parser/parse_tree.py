class TreeNode:
  def __init__(self, parent=None, token='', lexeme=None):
    self.parent = parent
    self.children = []
    self.token = token
    self.children_count = 0
    self.lexeme = lexeme
    
    
  def append_children(self, production):
    self.children_count = len(production)
    

  def is_complete(self):
    return self.children_count == len(self.children)
    
  