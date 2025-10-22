import unittest
from src.lexer.AFD.AFDStringLiteral import AFDStringLiteral

class TestAFDStringLiteral(unittest.TestCase):
    """Testes unitários para o AFD de strings literais."""
    
    def setUp(self):
        """Inicializa um AFD novo para cada teste."""
        self.afd = AFDStringLiteral()
    
    def test_string_aspas_duplas(self):
        """Testa reconhecimento de string com aspas duplas."""
        entrada = '"teste"'
        resultado = self.afd.match(entrada)
        self.assertIsNotNone(resultado, "Deveria reconhecer string com aspas duplas")
        self.assertEqual(resultado[2], "STRING", "Tipo do token deveria ser STRING")
        self.assertEqual(resultado[0], '"teste"', "Lexema deveria incluir as aspas")
    
    def test_string_aspas_simples(self):
        """Testa reconhecimento de string com aspas simples."""
        entrada = "'teste'"
        resultado = self.afd.match(entrada)
        self.assertIsNotNone(resultado, "Deveria reconhecer string com aspas simples")
        self.assertEqual(resultado[2], "STRING", "Tipo do token deveria ser STRING")
        
    def test_string_vazia(self):
        """Testa reconhecimento de string vazia."""
        entradas = ['""', "''"]
        for entrada in entradas:
            with self.subTest(entrada=entrada):
                resultado = self.afd.match(entrada)
                self.assertIsNotNone(resultado, f"Deveria reconhecer string vazia {entrada}")
                self.assertEqual(resultado[2], "STRING", "Tipo do token deveria ser STRING")
    
    def test_string_com_espacos(self):
        """Testa reconhecimento de string com espaços."""
        entrada = '"texto com espacos"'
        resultado = self.afd.match(entrada)
        self.assertIsNotNone(resultado, "Deveria reconhecer string com espaços")
        self.assertEqual(resultado[2], "STRING", "Tipo do token deveria ser STRING")
    
    def test_string_com_caracteres_especiais(self):
        """Testa reconhecimento de string com caracteres especiais."""
        entrada = '"teste!@#$%^&*()"'
        resultado = self.afd.match(entrada)
        self.assertIsNotNone(resultado, "Deveria reconhecer string com caracteres especiais")
        self.assertEqual(resultado[2], "STRING", "Tipo do token deveria ser STRING")
    
    def test_string_com_numeros(self):
        """Testa reconhecimento de string com números."""
        entrada = '"123456"'
        resultado = self.afd.match(entrada)
        self.assertIsNotNone(resultado, "Deveria reconhecer string com números")
        self.assertEqual(resultado[2], "STRING", "Tipo do token deveria ser STRING")
    
    def test_rejeita_string_nao_fechada(self):
        """Testa rejeição de strings não fechadas (sem aspas de fechamento)."""
        # Strings que realmente não têm fechamento
        entradas = ['"teste', "'teste"]
        for entrada in entradas:
            with self.subTest(entrada=entrada):
                resultado = self.afd.match(entrada)
                self.assertIsNone(resultado, f"Não deveria reconhecer string não fechada {entrada}")
    
    def test_string_com_texto_depois(self):
        """Testa que string válida seguida de texto reconhece apenas a string."""
        # O AFD deve reconhecer a string válida e parar
        casos = [
            ('"teste"texto', ('"teste"', 7, 'STRING')),
            ("'teste'texto", ("'teste'", 7, 'STRING'))
        ]
        for entrada, esperado in casos:
            with self.subTest(entrada=entrada):
                resultado = self.afd.match(entrada)
                self.assertEqual(resultado, esperado)
    
    def test_rejeita_string_sem_aspas(self):
        """Testa rejeição de texto sem aspas."""
        entrada = "teste"
        resultado = self.afd.match(entrada)
        self.assertIsNone(resultado, "Não deveria reconhecer texto sem aspas")
    
    def test_string_com_aspas_internas(self):
        """Testa reconhecimento de string com aspas dentro."""
        entrada = '"Texto com \\"aspas\\" dentro"'
        resultado = self.afd.match(entrada)
        self.assertIsNotNone(resultado, "Deveria reconhecer string com aspas escapadas")
        self.assertEqual(resultado[2], "STRING", "Tipo do token deveria ser STRING")

if __name__ == '__main__':
    unittest.main()
