import unittest
from src.lexer.AFD.AFDOperadoresBooleanos import AFDOperadoresBooleanos

class TestAFDOperadoresBooleanos(unittest.TestCase):
    """Testes unitários para o AFD de operadores booleanos."""
    
    def setUp(self):
        """Inicializa um AFD novo para cada teste."""
        self.afd = AFDOperadoresBooleanos()
    
    def test_verdade(self):
        """Testa reconhecimento do operador VERDADE."""
        entrada = "VERDADE"
        resultado = self.afd.match(entrada)
        self.assertIsNotNone(resultado, "Deveria reconhecer VERDADE")
        self.assertEqual(resultado[2], "BOOLEANO", "Tipo do token deveria ser BOOLEANO")
        self.assertEqual(resultado[0], "VERDADE", "Lexema deveria ser VERDADE")
    
    def test_falso(self):
        """Testa reconhecimento do operador FALSO."""
        entrada = "FALSO"
        resultado = self.afd.match(entrada)
        self.assertIsNotNone(resultado, "Deveria reconhecer FALSO")
        self.assertEqual(resultado[2], "BOOLEANO", "Tipo do token deveria ser BOOLEANO")
        self.assertEqual(resultado[0], "FALSO", "Lexema deveria ser FALSO")
    
    def test_rejeita_variacao_verdade(self):
        """Testa rejeição de variações do operador VERDADE."""
        invalidos = ["VERDADEIRO", "Verdade", "verdade", "VERD"]
        for entrada in invalidos:
            with self.subTest(entrada=entrada):
                resultado = self.afd.match(entrada)
                self.assertIsNone(resultado, f"Não deveria reconhecer {entrada}")
    
    def test_rejeita_variacao_falso(self):
        """Testa rejeição de variações do operador FALSO."""
        invalidos = ["FALSE", "Falso", "falso", "FAL"]
        for entrada in invalidos:
            with self.subTest(entrada=entrada):
                resultado = self.afd.match(entrada)
                self.assertIsNone(resultado, f"Não deveria reconhecer {entrada}")
    
    def test_rejeita_vazio(self):
        """Testa rejeição de string vazia."""
        entrada = ""
        resultado = self.afd.match(entrada)
        self.assertIsNone(resultado, "Não deveria reconhecer string vazia")
    
    def test_booleano_com_sufixo(self):
        """Testa reconhecimento quando seguido de outros caracteres."""
        entradas = ["VERDADE123", "FALSO_TESTE"]
        for entrada in entradas:
            with self.subTest(entrada=entrada):
                resultado = self.afd.match(entrada)
                self.assertIsNotNone(resultado, "Deveria reconhecer a parte válida")
                self.assertTrue(resultado[0] in ["VERDADE", "FALSO"], 
                              "Deveria reconhecer apenas o operador booleano válido")

if __name__ == '__main__':
    unittest.main()