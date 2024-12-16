from Scanner.token import Token
from Scanner.token_type import TokenType
from typing import List, Dict


class Scanner:

    keywords: Dict[str, TokenType] = {}

    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1

    @classmethod
    def initialize_keywords(cls):
        cls.keywords = {
            "boolean": TokenType.BOOLEAN,
            "class": TokenType.CLASS,
            "extends": TokenType.EXTENDS,
            "public": TokenType.PUBLIC,
            "static": TokenType.STATIC,
            "void": TokenType.VOID,
            "main": TokenType.MAIN,
            "String": TokenType.STRING,
            "return": TokenType.RETURN,
            "int": TokenType.INT,
            "if": TokenType.IF,
            "else": TokenType.ELSE,
            "while": TokenType.WHILE,
            "System.out.println": TokenType.SYSTEM_OUT_PRINTLN,
            ".length": TokenType.LENGTH,
            "true": TokenType.TRUE,
            "false": TokenType.FALSE,
            "this": TokenType.THIS,
            "new": TokenType.NEW,
            "new int": TokenType.NEW_INT,
            "null": TokenType.NULL
        }

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def is_at_end(self):
        return self.current >= len(self.source)

    def scan_token(self):
        c = self.advance()

        match c:
            case '(':
                self.add_token(TokenType.LEFT_PAR)
            case ')':
                self.add_token(TokenType.RIGHT_PAR)
            case '[':
                self.add_token(TokenType.LEFT_BRACKET)
            case ']':
                self.add_token(TokenType.RIGHT_BRACKET)
            case '{':
                self.add_token(TokenType.LEFT_CURLY)
            case '}':
                self.add_token(TokenType.RIGHT_CURLY)
            case '.':
                self.add_token(TokenType.PERIOD)
            case ',':
                self.add_token(TokenType.COMMA)
            case ';':
                self.add_token(TokenType.SEMICOLON)
            case '-':
                self.add_token(TokenType.MINUS)
            case '+':
                self.add_token(TokenType.PLUS)
            case '*':
                self.add_token(TokenType.TIMES)
            case '&':
                if self.match('&'):
                    self.add_token(TokenType.AND)
            case '<':
                if self.match('='):
                    self.add_token(TokenType.LESS_EQUAL)
                else:
                    self.add_token(TokenType.LESS_THEN)
            case '>':
                if self.match('='):
                    self.add_token(TokenType.GREATER_EQUAL)
                else:
                    self.add_token(TokenType.GREATER_THEN)
            case '=':
                if self.match('='):
                    self.add_token(TokenType.DOUBLE_EQUAL)
                else:
                    self.add_token(TokenType.EQUAL)
            case '!':
                if self.match('='):
                    self.add_token(TokenType.NOT_EQUAL)
                else:
                    self.add_token(TokenType.NOT)
            case '"':
                self.string()
            case ' ' | '\r' | '\t' | '\f':
                pass
            case '\n':
                self.line += 1
            case '/':
                if self.match('*'):
                    while True:
                        if self.peek() == '*' and self.peek_next() == '/':
                            self.advance()
                            self.advance()
                            break
                        elif self.is_at_end():
                            raise SyntaxError(
                                f"Unterminated block comment at line {self.line}")
                        elif self.peek() == '\n':
                            self.line += 1
                        self.advance()
                elif self.match('/'):
                    while self.peek() != '\n' and not self.is_at_end():
                        self.advance()
            case _:
                if c.isdigit():
                    self.number()
                elif c.isalpha():
                    self.identifier()
                else:
                    raise SyntaxError(
                        f'Unexpected character "{c}" at line {self.line}')

    def advance(self):
        current_char = self.source[self.current]
        self.current += 1

        return current_char

    def add_token(self, type, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self):
        if self.is_at_end():
            return '\0'

        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                raise SyntaxError(
                    f"{self.line} String literals cannot span multiple lines.")
            self.advance()

        if self.is_at_end():
            raise SyntaxError(f" {self.line} Unterminated string.")

        self.advance()
        value = self.source[self.start + 1:self.current - 1]

        self.add_token(TokenType.STR, value)
        # valor de uma string, para não confundir com a palavra reservada

    def is_alpha_numeric(self, c):
        return c.isalnum() or c == '_'

    def number(self):
        while self.peek().isdigit():
            self.advance()

        self.add_token(TokenType.NUM, int(
            self.source[self.start:self.current]))

    def identifier(self):
        while self.is_alpha_numeric(self.peek()):
            self.advance()

        text = self.source[self.start:self.current]

        if 'System' in text:
            while self.is_alpha_numeric(self.peek()) or self.peek() == '.':
                self.advance()
            text = self.source[self.start:self.current]

        if 'new' in text and self.source[(self.start + 4):(self.current + 4)] == 'int':
            for _ in range(4):
                self.advance()
            text = self.source[self.start:self.current]
    
        token_type = Scanner.keywords.get(text)

        if token_type is None:
            token_type = TokenType.ID

        self.add_token(token_type)


Scanner.initialize_keywords()
