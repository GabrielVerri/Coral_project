"""
Runner de testes para o projeto Coral.
Wrapper simplificado para executar pytest com as configurações adequadas.

Uso:
    python test/run_tests.py           # Roda todos os testes
    python test/run_tests.py -v        # Modo verboso
    python test/run_tests.py --help    # Ajuda do pytest
"""
import subprocess
import sys
import os

def run_tests():
    # Muda para o diretório raiz do projeto
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    
    # Configuração padrão do pytest
    pytest_args = [
        sys.executable, "-m", "pytest",
        "test/lexer_test/",
        "-v",                # Modo verboso (mostra cada teste)
        "--tb=short",        # Traceback curto em caso de erro
    ]
    
    # Adiciona argumentos extras do usuário (se houver)
    if len(sys.argv) > 1:
        pytest_args.extend(sys.argv[1:])
    
    print(f"Executando testes do Coral Lexer...")
    print(f"Diretório: {project_root}")
    print(f"Comando: {' '.join(pytest_args[2:])}\n")
    
    # Executa pytest
    result = subprocess.run(pytest_args)
    
    return result.returncode

if __name__ == '__main__':
    sys.exit(run_tests())