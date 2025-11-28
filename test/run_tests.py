"""
Runner de testes para o projeto Coral.
Wrapper simplificado para executar pytest com as configurações adequadas.

Uso:
    python test/run_tests.py              # Roda todos os testes
    python test/run_tests.py lexer        # Roda apenas testes do lexer
    python test/run_tests.py parser       # Roda apenas testes do parser
    python test/run_tests.py llvmir       # Roda apenas testes de LLVM IR
    python test/run_tests.py -v           # Modo verboso
    python test/run_tests.py --help       # Ajuda do pytest
"""
import subprocess
import sys
import os

def run_tests():
    # Muda para o diretório raiz do projeto
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    
    # Determina quais testes rodar
    test_dirs = []
    custom_args = []
    
    for arg in sys.argv[1:]:
        if arg == "lexer":
            test_dirs.append("test/lexer_test/")
        elif arg == "parser":
            test_dirs.append("test/parser_test/")
        elif arg == "llvmir":
            test_dirs.append("test/llvmir_test/")
        else:
            custom_args.append(arg)
    
    # Se não especificou nenhum diretório, roda todos
    if not test_dirs:
        test_dirs = ["test/lexer_test/", "test/parser_test/", "test/llvmir_test/"]
    
    # Configuração padrão do pytest
    pytest_args = [
        sys.executable, "-m", "pytest",
        *test_dirs,
        "-v",                # Modo verboso (mostra cada teste)
        "--tb=short",        # Traceback curto em caso de erro
        *custom_args,
    ]
    
    print(f"=== Executando Testes do Coral ===")
    print(f"Diretório: {project_root}")
    print(f"Testes: {', '.join(test_dirs)}")
    print(f"Comando: {' '.join(pytest_args[2:])}\n")
    
    # Executa pytest
    result = subprocess.run(pytest_args)
    
    return result.returncode

if __name__ == '__main__':
    sys.exit(run_tests())