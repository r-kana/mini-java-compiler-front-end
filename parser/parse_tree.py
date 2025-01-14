from typing import Self

from Parser.production_rules import EPSILON

class TreeNode:
  def __init__(self, parent=None, token='', lexeme=None):
    self.children: list[TreeNode]
    self.parent: TreeNode | None
    self.token: str
    self.lexeme: str | None
    self.parent = parent
    self.children = []
    self.token = token
    self.children_count = 0
    self.lexeme = lexeme
    
    
  def append_children(self, production):
    self.children_count = len(production)
    

  def is_complete(self) -> bool:
    return self.children_count == len(self.children)
  
  def child(self, token: str) -> Self | None:
    for child in self.children:
      if(child.token == token):
        return child
    return None
  
  def is_empty(self):
    return self.children[0].token == EPSILON
    
  