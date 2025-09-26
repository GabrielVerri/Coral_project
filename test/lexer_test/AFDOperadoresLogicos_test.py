import unittest
from src.lexer.AFD.AFDOperadoresLogicos import AFDOperadoresLogicos

class TestAFDOperadoresLogicos(unittest.TestCase):
    """Testes unitários para o AFD de operadores lógicos."""
    
    def setUp(self):
        """Inicializa um AFD novo para cada teste."""
        self.afd = AFDOperadoresLogicos()
    
    def test_operador_e(self):
        """Testa reconhecimento do operador E."""
        entrada = "E"
        resultado = self.afd.match(entrada)
        self.assertIsNotNone(resultado, "Deveria reconhecer E")
        self.assertEqual(resultado[2], "OPERADOR_LOGICO", "Tipo do token deveria ser OPERADOR_LOGICO")
        self.assertEqual(resultado[0], "E", "Lexema deveria ser E")
    
    def test_operador_ou(self):
        """Testa reconhecimento do operador OU."""
        entrada = "OU"
        resultado = self.afd.match(entrada)
        self.assertIsNotNone(resultado, "Deveria reconhecer OU")
        self.assertEqual(resultado[2], "OPERADOR_LOGICO", "Tipo do token deveria ser OPERADOR_LOGICO")
        self.assertEqual(resultado[0], "OU", "Lexema deveria ser OU")
    
    def test_operador_nao(self):
        """Testa reconhecimento do operador NAO."""
        entrada = "NAO"
        resultado = self.afd.match(entrada)
        self.assertIsNotNone(resultado, "Deveria reconhecer NAO")
        self.assertEqual(resultado[2], "OPERADOR_LOGICO", "Tipo do token deveria ser OPERADOR_LOGICO")
        self.assertEqual(resultado[0], "NAO", "Lexema deveria ser NAO")
    
    def test_rejeita_variacao_e(self):
        """Testa rejeição de variações do operador E."""
        invalidos = ["e", "AND", "&&", "E1", "Ex"]
        for entrada in invalidos:
            with self.subTest(entrada=entrada):
                resultado = self.afd.match(entrada)
                self.assertIsNone(resultado, f"Não deveria reconhecer {entrada}")
    
    def test_rejeita_variacao_ou(self):
        """Testa rejeição de variações do operador OU."""
        invalidos = ["ou", "OR", "||", "O"]
        for entrada in invalidos:
            with self.subTest(entrada=entrada):
                resultado = self.afd.match(entrada)
                self.assertIsNone(resultado, f"Não deveria reconhecer {entrada}")
    
    def test_rejeita_variacao_nao(self):
        """Testa rejeição de variações do operador NAO."""
        invalidos = ["nao", "NOT", "!", "Na"]
        for entrada in invalidos:
            with self.subTest(entrada=entrada):
                resultado = self.afd.match(entrada)
                self.assertIsNone(resultado, f"Não deveria reconhecer {entrada}")
    
    def test_rejeita_vazio(self):
        """Testa rejeição de string vazia."""
        entrada = ""
        resultado = self.afd.match(entrada)
        self.assertIsNone(resultado, "Não deveria reconhecer string vazia")
    
    def test_operador_com_sufixo(self):
        """Testa reconhecimento quando seguido de outros caracteres."""
        # Os operadores lógicos precisam ter fronteiras de palavra (\b)
        # Então não devem ser reconhecidos quando seguidos de _ ou letras/números
        entradas = {
            "E_teste": None,  # _ é parte de identificador
            "E@teste": "E",   # @ forma fronteira
            "E teste": "E"    # espaço forma fronteira
        }
        for entrada, esperado in entradas.items():
            with self.subTest(entrada=entrada):
                resultado = self.afd.match(entrada)
                if esperado is None:
                    self.assertIsNone(resultado, f"Não deveria reconhecer {entrada}")
                else:
                    self.assertIsNotNone(resultado, "Deveria reconhecer a parte válida")
                    self.assertEqual(resultado[0], esperado, 
                                  f"Deveria reconhecer apenas o operador válido {esperado}")

if __name__ == '__main__':
    unittest.main()
