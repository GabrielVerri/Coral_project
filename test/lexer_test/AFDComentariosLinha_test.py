import unittest
from src.lexer.AFD.AFDComentariosLinha import AFDComentariosLinha

class TestAFDComentariosLinha(unittest.TestCase):
    """Testes unitários para o AFD de comentários em linha."""
    
    def setUp(self):
        """Inicializa um AFD novo para cada teste."""
        self.afd = AFDComentariosLinha()
    
    def test_comentario_simples(self):
        """Testa reconhecimento de comentário simples."""
        entrada = "#teste"
        resultado = self.afd.match(entrada)
        self.assertIsNotNone(resultado, "Deveria reconhecer um comentário válido")
        self.assertEqual(resultado[2], "COMENTARIO_LINHA", "Tipo do token deveria ser COMENTARIO_LINHA")
        
    def test_comentario_vazio(self):
        """Testa reconhecimento de comentário sem conteúdo."""
        entrada = "#"
        resultado = self.afd.match(entrada)
        self.assertIsNotNone(resultado, "Deveria reconhecer um comentário vazio")
        self.assertEqual(resultado[2], "COMENTARIO_LINHA", "Tipo do token deveria ser COMENTARIO_LINHA")
        
    def test_nao_comentario(self):
        """Testa rejeição de string que não é comentário."""
        entrada = "abc"
        resultado = self.afd.match(entrada)
        self.assertIsNone(resultado, "Não deveria reconhecer texto sem #")
        
    def test_string_vazia(self):
        """Testa rejeição de string vazia."""
        entrada = ""
        resultado = self.afd.match(entrada)
        self.assertIsNone(resultado, "Não deveria reconhecer string vazia")
        
    def test_comentario_com_espacos(self):
        """Testa reconhecimento de comentário com espaços."""
        entrada = "# teste com espaços"
        resultado = self.afd.match(entrada)
        self.assertIsNotNone(resultado, "Deveria reconhecer comentário com espaços")
        self.assertEqual(resultado[2], "COMENTARIO_LINHA", "Tipo do token deveria ser COMENTARIO_LINHA")

if __name__ == '__main__':
    unittest.main()