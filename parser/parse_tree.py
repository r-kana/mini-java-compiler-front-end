class TreeNode:
  def __init__(self, parent=None, token=''):
    self.parent = parent
    self.children = []
    self.token = token
    self.children_count = 0
    
    
  def append_children(self, production):
    self.children_count = len(production)
    

  def is_complete(self):
    self.children_count == len(self.children)
    
  