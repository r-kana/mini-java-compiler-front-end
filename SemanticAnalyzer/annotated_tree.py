class AnnotadedTreeNode:
    def __init__(self, name, tipo=None):
        self.name = name
        self.tipo = tipo
        self.children = []

    def add_child(self, child):
        self.children.append(child)


def print_annotated_tree(node, level=0):
    """Imprime a árvore de parse anotada com seus atributos."""
    if node is None:
        return

    indent = "  " * level
    attributes = f" [tipo={node.tipo}]" if node.tipo else ""
    print(f"{indent}{node.name}{attributes}")

    for child in node.children:
        print_annotated_tree(child, level + 1)
