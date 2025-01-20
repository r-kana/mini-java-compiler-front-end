from SemanticAnalyzer.semantic_analyzer import SemanticAnalyzer
from SemanticAnalyzer.annotated_tree import print_annotated_tree

def semantic_analysis(root):
    # Criar o analisador semântico
    semantic_analyzer = SemanticAnalyzer()

    try:
        # Analisar semântica
        annotated_tree = semantic_analyzer.analyze(root)

        # Imprimir a árvore anotada
        print("Árvore sintática anotada:")
        print_annotated_tree(annotated_tree)
    except Exception as e:
        print(f"Erro durante a análise semântica: {e}")