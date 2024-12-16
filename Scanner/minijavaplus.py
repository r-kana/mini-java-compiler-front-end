import sys
from Scanner.scanner import Scanner

class MiniJava:
    had_error = False

    @staticmethod
    def main(path):
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
        #     print(token)
        return tokens
    
    
    @staticmethod
    def report(line, where, message):
        print(f"[line {line}] Error{where}: {message}", file=sys.stderr)

        global had_error
        MiniJava.had_error = True


if __name__ == "__main__":
    MiniJava.main()
