from Code_Gen.code_gen import code_gen, print_ast
from SemanticAnalyzer.semantic_analysis import semantic_analysis
from Parser.parser import parser, print_parse_tree, ROOT
from Scanner.minijavaplus import MiniJava
from Scanner.token import Token


token: list[Token]
tokens = MiniJava.main('./example.java')

parser(tokens)

# print_parse_tree(ROOT)
# print('AST:\n')
# print_ast(ROOT)
# print('\n')
semantic_analysis(ROOT)
print('Code Gen:\n')
code_gen(ROOT)