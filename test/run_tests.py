"""
Runner de testes para o analisador léxico.
Executa todos os testes unitários dos AFDs.
"""
import unittest
import sys
import os

# Adiciona o diretório raiz ao path para permitir imports relativos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importa todos os testes
from test.lexer_test.AFDComentariosLinha_test import TestAFDComentariosLinha
from test.lexer_test.AFDDecimal_test import TestAFDDecimal
from test.lexer_test.AFDIdentificadores_test import TestAFDIdentificadores
from test.lexer_test.AFDOperadoresAritmeticosRelacionais_test import TestAFDOperadoresAritmeticosRelacionais
from test.lexer_test.AFDOperadoresBooleanos_test import TestAFDOperadoresBooleanos
from test.lexer_test.AFDOperadoresLogicos_test import TestAFDOperadoresLogicos
from test.lexer_test.AFDStringLiteral_test import TestAFDStringLiteral

def run_tests():
    """Executa todos os testes unitários."""
    # Cria um test suite com todos os testes
    test_suite = unittest.TestSuite()
    
    # Adiciona todas as classes de teste
    test_classes = [
        TestAFDComentariosLinha,
        TestAFDDecimal,
        TestAFDIdentificadores,
        TestAFDOperadoresAritmeticosRelacionais,
        TestAFDOperadoresBooleanos,
        TestAFDOperadoresLogicos,
        TestAFDStringLiteral
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Executa os testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Retorna código de saída apropriado
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests())