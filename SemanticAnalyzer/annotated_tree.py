class AnnotadedTreeNode:
    def __init__(self, token, semantic_type=None, lexeme=None, literal=None):
        self.token = token
        self.semantic_type = semantic_type
        self.lexeme = lexeme
        self.literal = literal
        self.children = []

    def add_child(self, child):
        self.children.append(child)
        
    def __str__(self):
        return f"AnnotatedTreeNode(token={self.token}, semantic_type={self.semantic_type}, lexeme={self.lexeme}, literal={self.literal})"


def print_annotated_tree(node, level=0):
    """Imprime a árvore de parse anotada com seus atributos."""
    if node is None:
        return

    indent = "  " * level
    attributes = f" [semantic_type={node.semantic_type}]" if node.semantic_type else ""
    print(f"{indent}{node.token}{attributes}")

    for child in node.children:
        print_annotated_tree(child, level + 1)
