import unittest
from src.lexer.AFD.AFDOperadoresAritmeticosRelacionais import AFDOperadoresAritmeticosRelacionais

class TestAFDOperadoresAritmeticosRelacionais(unittest.TestCase):
    """Testes unitários para o AFD de operadores aritméticos e relacionais."""
    
    def setUp(self):
        """Inicializa um AFD novo para cada teste."""
        self.afd = AFDOperadoresAritmeticosRelacionais()
    
    def test_operador_aritmetico_simples(self):
        """Testa reconhecimento de operadores aritméticos simples."""
        operadores = ["+", "-", "*", "/"]
        for op in operadores:
            with self.subTest(operador=op):
                resultado = self.afd.match(op)
                self.assertIsNotNone(resultado, f"Deveria reconhecer o operador {op}")
                self.assertEqual(resultado[2], "OPERADOR_ARITMETICO", "Tipo do token deveria ser OPERADOR_ARITMETICO")
                self.assertEqual(resultado[0], op, "Lexema deveria ser o operador")
    
    def test_operador_aritmetico_composto(self):
        """Testa reconhecimento de operadores aritméticos compostos."""
        operadores = ["+=", "-=", "*=", "/=", "++", "--"]
        for op in operadores:
            with self.subTest(operador=op):
                resultado = self.afd.match(op)
                self.assertIsNotNone(resultado, f"Deveria reconhecer o operador {op}")
                self.assertEqual(resultado[2], "OPERADOR_ATRIBUICAO", "Tipo do token deveria ser OPERADOR_ATRIBUICAO")
                self.assertEqual(resultado[0], op, "Lexema deveria ser o operador completo")
    
    def test_operador_relacional(self):
        """Testa reconhecimento de operadores relacionais."""
        operadores = ["==", "!=", "<", ">", "<=", ">="]
        for op in operadores:
            with self.subTest(operador=op):
                resultado = self.afd.match(op)
                self.assertIsNotNone(resultado, f"Deveria reconhecer o operador {op}")
                self.assertEqual(resultado[2], "OPERADOR_RELACIONAL", "Tipo do token deveria ser OPERADOR_RELACIONAL")
                self.assertEqual(resultado[0], op, "Lexema deveria ser o operador")
    
    def test_atribuicao_simples(self):
        """Testa reconhecimento de operador de atribuição simples."""
        entrada = "="
        resultado = self.afd.match(entrada)
        self.assertIsNotNone(resultado, "Deveria reconhecer operador de atribuição")
        self.assertEqual(resultado[2], "OPERADOR_ATRIBUICAO", "Tipo do token deveria ser OPERADOR_ATRIBUICAO")
    
    def test_rejeita_operador_invalido(self):
        """Testa rejeição de sequências que não são operadores válidos."""
        invalidos = ["@", "$", "abc", "&", "=>"]
        for op in invalidos:
            with self.subTest(operador=op):
                resultado = self.afd.match(op)
                self.assertIsNone(resultado, f"Não deveria reconhecer {op} como operador")
    
    def test_rejeita_vazio(self):
        """Testa rejeição de string vazia."""
        entrada = ""
        resultado = self.afd.match(entrada)
        self.assertIsNone(resultado, "Não deveria reconhecer string vazia")
    
    def test_operador_parcial(self):
        """Testa reconhecimento parcial quando seguido de caractere inválido."""
        entrada = "++x"
        resultado = self.afd.match(entrada)
        self.assertIsNotNone(resultado, "Deveria reconhecer a parte válida do operador")
        self.assertEqual(resultado[0], "++", "Deveria reconhecer apenas o operador válido")

if __name__ == '__main__':
    unittest.main()