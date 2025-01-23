from Code_Gen.code_gen import code_gen, print_ast
from SemanticAnalyzer.semantic_analysis import semantic_analysis
from Parser.parser import parser, ROOT
from Scanner.minijavaplus import MiniJava
from Scanner.token import Token


token: list[Token]
tokens = MiniJava.main('./example.java')

parser(tokens)
# print('AST:\n')
# print_ast(ROOT)
# print('\n')
semantic_analysis(ROOT)
print('Code Gen:\n')
code_gen(ROOT)