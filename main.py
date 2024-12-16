from Parser.parser import parser, print_parse_tree, ROOT
from Scanner.minijavaplus import MiniJava

parser(MiniJava.main('./example.java'))

print_parse_tree(ROOT)