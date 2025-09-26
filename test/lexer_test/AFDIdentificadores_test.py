import unittest
from src.lexer.AFD.AFDIdentificadores import AFDIdentificadores

class TestAFDIdentificadores(unittest.TestCase):
    """Testes unitários para o AFD de identificadores."""
    
    def setUp(self):
        """Inicializa um AFD novo para cada teste."""
        self.afd = AFDIdentificadores()
    
    def test_identificador_simples(self):
        """Testa reconhecimento de identificador simples."""
        entrada = "variavel"
        resultado = self.afd.match(entrada)
        self.assertIsNotNone(resultado, "Deveria reconhecer um identificador válido")
        self.assertEqual(resultado[2], "IDENTIFICADOR", "Tipo do token deveria ser IDENTIFICADOR")
        self.assertEqual(resultado[0], "variavel", "Lexema deveria ser o identificador completo")
        
    def test_identificador_com_underscore(self):
        """Testa reconhecimento de identificador com underscore."""
        entrada = "x_123"
        resultado = self.afd.match(entrada)
        self.assertIsNotNone(resultado, "Deveria reconhecer identificador com underscore")
        self.assertEqual(resultado[2], "IDENTIFICADOR", "Tipo do token deveria ser IDENTIFICADOR")
        
    def test_identificador_so_underscore(self):
        """Testa reconhecimento de identificador que é só underscore."""
        entrada = "_"
        resultado = self.afd.match(entrada)
        self.assertIsNotNone(resultado, "Deveria reconhecer underscore como identificador")
        self.assertEqual(resultado[2], "IDENTIFICADOR", "Tipo do token deveria ser IDENTIFICADOR")
        
    def test_identificador_com_numeros(self):
        """Testa reconhecimento de identificador com números."""
        entrada = "var123"
        resultado = self.afd.match(entrada)
        self.assertIsNotNone(resultado, "Deveria reconhecer identificador com números")
        self.assertEqual(resultado[2], "IDENTIFICADOR", "Tipo do token deveria ser IDENTIFICADOR")
        
    def test_rejeita_comeca_numero(self):
        """Testa rejeição de identificador começando com número."""
        entrada = "123abc"
        resultado = self.afd.match(entrada)
        self.assertIsNone(resultado, "Não deveria reconhecer identificador começando com número")
        
    def test_rejeita_vazio(self):
        """Testa rejeição de string vazia."""
        entrada = ""
        resultado = self.afd.match(entrada)
        self.assertIsNone(resultado, "Não deveria reconhecer string vazia")
        
    def test_identificador_maiusculo(self):
        """Testa reconhecimento de identificador em maiúsculo."""
        entrada = "NOME"
        resultado = self.afd.match(entrada)
        self.assertIsNotNone(resultado, "Deveria reconhecer identificador em maiúsculo")
        self.assertEqual(resultado[2], "IDENTIFICADOR", "Tipo do token deveria ser IDENTIFICADOR")
        
    def test_identificador_misto(self):
        """Testa reconhecimento de identificador com maiúsculas e minúsculas."""
        entrada = "Nome_Completo_123"
        resultado = self.afd.match(entrada)
        self.assertIsNotNone(resultado, "Deveria reconhecer identificador misto")
        self.assertEqual(resultado[2], "IDENTIFICADOR", "Tipo do token deveria ser IDENTIFICADOR")
        
    def test_identificador_com_caractere_invalido(self):
        """Testa reconhecimento parcial de identificador com caractere inválido."""
        entrada = "nome@sobrenome"
        resultado = self.afd.match(entrada)
        self.assertIsNotNone(resultado, "Deveria reconhecer a parte válida do identificador")
        self.assertEqual(resultado[0], "nome", "Deveria parar no caractere inválido")
        
    def test_identificador_com_espaco(self):
        """Testa reconhecimento parcial de identificador com espaço."""
        entrada = "nome sobrenome"
        resultado = self.afd.match(entrada)
        self.assertIsNotNone(resultado, "Deveria reconhecer a parte válida do identificador")
        self.assertEqual(resultado[0], "nome", "Deveria parar no espaço")

if __name__ == '__main__':
    unittest.main()