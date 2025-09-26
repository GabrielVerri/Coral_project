import unittest
from src.lexer.AFD.AFDDecimal import AFDDecimal

class TestAFDDecimal(unittest.TestCase):
    """Testes unitários para o AFD de números decimais."""
    
    def setUp(self):
        """Inicializa um AFD novo para cada teste."""
        self.afd = AFDDecimal()
    
    def test_decimal_simples(self):
        """Testa reconhecimento de número decimal simples."""
        entrada = "123.456"
        resultado = self.afd.match(entrada)
        self.assertIsNotNone(resultado, "Deveria reconhecer um decimal válido")
        self.assertEqual(resultado[2], "DECIMAL", "Tipo do token deveria ser DECIMAL")
        self.assertEqual(resultado[0], "123.456", "Lexema deveria ser o número completo")
        
    def test_decimal_zero(self):
        """Testa reconhecimento de zero decimal."""
        entrada = "0.0"
        resultado = self.afd.match(entrada)
        self.assertIsNotNone(resultado, "Deveria reconhecer zero decimal")
        self.assertEqual(resultado[2], "DECIMAL", "Tipo do token deveria ser DECIMAL")
        
    def test_decimal_muitas_casas(self):
        """Testa reconhecimento de decimal com muitas casas."""
        entrada = "3.14159265359"
        resultado = self.afd.match(entrada)
        self.assertIsNotNone(resultado, "Deveria reconhecer decimal com muitas casas")
        self.assertEqual(resultado[2], "DECIMAL", "Tipo do token deveria ser DECIMAL")
        
    def test_inteiro(self):
        """Testa reconhecimento de número inteiro."""
        entrada = "42"
        resultado = self.afd.match(entrada)
        self.assertIsNotNone(resultado, "Deveria reconhecer um inteiro")
        self.assertEqual(resultado[2], "INTEIRO", "Tipo do token deveria ser INTEIRO")
        
    def test_rejeita_ponto_inicial(self):
        """Testa rejeição de número começando com ponto."""
        entrada = ".5"
        resultado = self.afd.match(entrada)
        self.assertIsNone(resultado, "Não deveria reconhecer número começando com ponto")
        
    def test_rejeita_ponto_sem_decimal(self):
        """Testa rejeição de número terminando em ponto."""
        entrada = "123."
        resultado = self.afd.match(entrada)
        self.assertIsNone(resultado, "Não deveria reconhecer número terminando em ponto")
        
    def test_rejeita_multiplos_pontos(self):
        """Testa rejeição de número com múltiplos pontos."""
        entrada = "1.2.3"
        resultado = self.afd.match(entrada)
        self.assertIsNotNone(resultado, "Deveria reconhecer até o primeiro número decimal válido")
        self.assertEqual(resultado[0], "1.2", "Deveria parar no primeiro decimal válido")
        
    def test_rejeita_nao_numero(self):
        """Testa rejeição de entrada que não é número."""
        entrada = "abc"
        resultado = self.afd.match(entrada)
        self.assertIsNone(resultado, "Não deveria reconhecer texto")
        
    def test_rejeita_vazio(self):
        """Testa rejeição de string vazia."""
        entrada = ""
        resultado = self.afd.match(entrada)
        self.assertIsNone(resultado, "Não deveria reconhecer string vazia")
        
    def test_decimal_com_lixo_depois(self):
        """Testa reconhecimento de decimal seguido de caracteres inválidos."""
        entrada = "123.456abc"
        resultado = self.afd.match(entrada)
        self.assertIsNotNone(resultado, "Deveria reconhecer a parte decimal válida")
        self.assertEqual(resultado[0], "123.456", "Deveria extrair apenas o número decimal")
        self.assertEqual(resultado[1], 7, "Deveria consumir 7 caracteres")

if __name__ == '__main__':
    unittest.main()