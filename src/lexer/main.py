import sys
# importa scanner usando caminho absoluto
import os
import sys

# adiciona o diretório src ao path do Python
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, src_dir)

from lexer.scanner import Scanner

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <arquivo.coral>")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        with open(filename, "r", encoding="utf-8") as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Erro: arquivo {filename} não encontrado.")
        sys.exit(1)

    try:
        scanner = Scanner(source)
        tokens = scanner.tokenize()

        print(f"{'TOKEN':20} | {'TIPO'}")
        print("-" * 40)
        for token, tipo in tokens:
            print(f"{token:20} | {tipo}")

    except ValueError as e:
        print(f"Erro léxico: {e}")

if __name__ == "__main__":
    main()
