import sys
from Scanner.scanner import Scanner
from Scanner.tokentype import TokenType

class MiniJava:
    had_error = False

    @staticmethod
    def main(path):
        # if len(sys.argv) > 2:
        #     print("Usage: minijavaplus [script]")
        #     sys.exit(64)
        # elif len(sys.argv) == 2:
            # MiniJava.run_file(sys.argv[1])
        return MiniJava.run_file(path)

    @staticmethod
    def run_file(path):
        try:
            with open(path, 'r', encoding='latin-1') as file:
                script = file.read()
                return MiniJava.run(script)

        except IOError as e:
            print(f"Erro ao ler o arquivo: {e}")

            if (MiniJava.hadError):
                exit(65)

    @staticmethod
    def run(source):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        # for token in tokens:
        #     if token.type in [
        #             TokenType.BOOLEAN, TokenType.CLASS, TokenType.EXTENDS,
        #             TokenType.PUBLIC, TokenType.STATIC, TokenType.VOID,
        #             TokenType.MAIN, TokenType.STRING, TokenType.RETURN,
        #             TokenType.INT, TokenType.IF, TokenType.ELSE,
        #             TokenType.WHILE, TokenType.SYSTEM_OUT_PRINTLN,
        #             TokenType.LENGTH, TokenType.TRUE, TokenType.FALSE,
        #             TokenType.THIS, TokenType.NEW, TokenType.NULL]:
        #         print(f"reserved word: {token.lexeme}")
        #     elif token.type == TokenType.ID:
        #         print(f"{token.type.value}, name = {token.lexeme}")
        #     elif token.type in [TokenType.NUM, TokenType.STR]:
        #         print(f"{token.type.value}, value = {token.literal}")
        #     else:
        #         print(token.lexeme) 
        return tokens
    
    
    @staticmethod
    def report(line, where, message):
        print(f"[line {line}] Error{where}: {message}", file=sys.stderr)

        global had_error
        MiniJava.had_error = True


if __name__ == "__main__":
    MiniJava.main()
