import unittest
from src.lexer.AFN.AFNCoralUnificado import AFNCoralUnificado
from src.lexer.afn_to_afd import ConversorAFNparaAFD
from src.lexer.AFD.AFDUnificado import AFDUnificado

class TestAFNAFDUnificado(unittest.TestCase):
    def setUp(self):
        # Inicializa AFN
        self.afn = AFNCoralUnificado()
        # Converte para AFD
        conversor = ConversorAFNparaAFD(self.afn)
        conversor.construir_subconjuntos()
        # Cria AFD unificado
        self.afd = AFDUnificado(conversor)
    
    def test_identificadores(self):
        """Testa reconhecimento de identificadores."""
        casos = [
            ("variavel", ("variavel", 8, "IDENTIFICADOR")),
            ("_teste", ("_teste", 6, "IDENTIFICADOR")),
            ("x123", ("x123", 4, "IDENTIFICADOR")),
            ("ABC_DEF", ("ABC_DEF", 7, "IDENTIFICADOR"))
        ]
        for entrada, esperado in casos:
            with self.subTest(entrada=entrada):
                resultado = self.afd.match(entrada)
                self.assertEqual(resultado, esperado)
    
    def test_strings(self):
        """Testa reconhecimento de strings."""
        casos = [
            ('"texto"', ('"texto"', 7, "STRING")),
            ("'texto'", ("'texto'", 7, "STRING")),
            ('"""texto\nmultilinhas"""', ('"""texto\nmultilinhas"""', 23, "STRING_MULTILINE"))
        ]
        for entrada, esperado in casos:
            with self.subTest(entrada=entrada):
                resultado = self.afd.match(entrada)
                self.assertEqual(resultado, esperado)
    
    def test_numeros(self):
        """Testa reconhecimento de números."""
        casos = [
            ("123", ("123", 3, "INTEIRO")),
            ("3.14", ("3.14", 4, "DECIMAL")),
            ("0.5", ("0.5", 3, "DECIMAL")),
            ("42.", None)  # Número inválido
        ]
        for entrada, esperado in casos:
            with self.subTest(entrada=entrada):
                resultado = self.afd.match(entrada)
                self.assertEqual(resultado, esperado)
    
    def test_operadores_aritmeticos(self):
        """Testa reconhecimento de operadores aritméticos."""
        casos = [
            ("+", ("+", 1, "OPERADOR_ARITMETICO")),
            ("-", ("-", 1, "OPERADOR_ARITMETICO")),
            ("*", ("*", 1, "OPERADOR_ARITMETICO")),
            ("/", ("/", 1, "OPERADOR_ARITMETICO")),
            ("%", ("%", 1, "OPERADOR_ARITMETICO"))
        ]
        for entrada, esperado in casos:
            with self.subTest(entrada=entrada):
                resultado = self.afd.match(entrada)
                self.assertEqual(resultado, esperado)
    
    def test_operadores_compostos(self):
        """Testa reconhecimento de operadores compostos."""
        casos = [
            ("+=", ("+=", 2, "OPERADOR_ATRIBUICAO")),
            ("-=", ("-=", 2, "OPERADOR_ATRIBUICAO")),
            ("*=", ("*=", 2, "OPERADOR_ATRIBUICAO")),
            ("/=", ("/=", 2, "OPERADOR_ATRIBUICAO")),
            ("++", ("++", 2, "OPERADOR_ATRIBUICAO")),
            ("--", ("--", 2, "OPERADOR_ATRIBUICAO"))
        ]
        for entrada, esperado in casos:
            with self.subTest(entrada=entrada):
                resultado = self.afd.match(entrada)
                self.assertEqual(resultado, esperado)
    
    def test_operadores_relacionais(self):
        """Testa reconhecimento de operadores relacionais."""
        casos = [
            ("==", ("==", 2, "OPERADOR_RELACIONAL")),
            ("!=", ("!=", 2, "OPERADOR_RELACIONAL")),
            ("<=", ("<=", 2, "OPERADOR_RELACIONAL")),
            (">=", (">=", 2, "OPERADOR_RELACIONAL")),
            ("<", ("<", 1, "OPERADOR_RELACIONAL")),
            (">", (">", 1, "OPERADOR_RELACIONAL"))
        ]
        for entrada, esperado in casos:
            with self.subTest(entrada=entrada):
                resultado = self.afd.match(entrada)
                self.assertEqual(resultado, esperado)
    
    def test_operadores_logicos(self):
        """Testa reconhecimento de operadores lógicos."""
        casos = [
            ("E", ("E", 1, "OPERADOR_LOGICO")),
            ("OU", ("OU", 2, "OPERADOR_LOGICO")),
            ("NAO", ("NAO", 3, "OPERADOR_LOGICO"))
        ]
        for entrada, esperado in casos:
            with self.subTest(entrada=entrada):
                resultado = self.afd.match(entrada)
                self.assertEqual(resultado, esperado)
    
    def test_operadores_booleanos(self):
        """Testa reconhecimento de operadores booleanos."""
        casos = [
            ("VERDADE", ("VERDADE", 7, "BOOLEANO")),
            ("FALSO", ("FALSO", 5, "BOOLEANO"))
        ]
        for entrada, esperado in casos:
            with self.subTest(entrada=entrada):
                resultado = self.afd.match(entrada)
                self.assertEqual(resultado, esperado)
    
    def test_comentarios(self):
        """Testa reconhecimento de comentários."""
        casos = [
            ("# comentário\n", ("# comentário\n", 13, "COMENTARIO_LINHA")),
            ("#\n", ("#\n", 2, "COMENTARIO_LINHA")),
            ("# teste", ("# teste", 7, "COMENTARIO_LINHA"))
        ]
        for entrada, esperado in casos:
            with self.subTest(entrada=entrada):
                resultado = self.afd.match(entrada)
                self.assertEqual(resultado, esperado)
    
    def test_delimitadores(self):
        """Testa reconhecimento de delimitadores."""
        casos = [
            ("(", ("(", 1, "DELIMITADOR")),
            (")", (")", 1, "DELIMITADOR")),
            ("{", ("{", 1, "DELIMITADOR")),
            ("}", ("}", 1, "DELIMITADOR")),
            (",", (",", 1, "DELIMITADOR"))
        ]
        for entrada, esperado in casos:
            with self.subTest(entrada=entrada):
                resultado = self.afd.match(entrada)
                self.assertEqual(resultado, esperado)
    
    def test_entradas_invalidas(self):
        """Testa rejeição de entradas inválidas."""
        casos = [
            "@",  # Caractere inválido
            "&",  # Operador não suportado
            "123abc",  # Número seguido de letra
            ".5",  # Número começando com ponto
        ]
        for entrada in casos:
            with self.subTest(entrada=entrada):
                resultado = self.afd.match(entrada)
                self.assertIsNone(resultado)
    
    def test_identificadores_similares_palavras_reservadas(self):
        """Testa que identificadores similares a palavras reservadas são aceitos."""
        casos = [
            ("VERDADES", ("VERDADES", 8, "IDENTIFICADOR")),
            ("EE", ("EE", 2, "IDENTIFICADOR")),
            ("FALSOO", ("FALSOO", 6, "IDENTIFICADOR")),
            ("NAO_NAO", ("NAO_NAO", 7, "IDENTIFICADOR"))
        ]
        for entrada, esperado in casos:
            with self.subTest(entrada=entrada):
                resultado = self.afd.match(entrada)
                self.assertEqual(resultado, esperado)

if __name__ == '__main__':
    unittest.main()