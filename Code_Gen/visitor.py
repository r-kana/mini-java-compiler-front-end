from Parser.parse_tree import TreeNode


class Visitor:
  def __init__(self, root: TreeNode):
    self.node = root
    self.children = root.children
    self.token = root.token
    self.lexeme = root.lexeme
    self.parent = root.parent
    
  def descend_to(self, token: str):
    self.node = self.node.child(token)
    self.children = self.node.children
    self.token = self.node.token
    self.lexeme = self.node.lexeme
    self.parent = self.node.parent
    

  def ascend(self):
    self.node = self.node.parent
    self.children = self.node.children
    self.token = self.node.token
    self.lexeme = self.node.lexeme
    self.parent = self.node.parent