from Code_Gen.code_gen import code_gen
from Parser.parser import parser, print_parse_tree, ROOT
from Scanner.minijavaplus import MiniJava
from Scanner.token import Token


token: list[Token]
tokens = MiniJava.main('./example.java')

parser(tokens)

# print_parse_tree(ROOT)

code_gen(ROOT)