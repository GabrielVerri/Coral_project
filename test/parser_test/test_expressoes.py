"""
Testes para parsing de expressões aritméticas, lógicas e booleanas.
"""
import pytest
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.lexer.lexer import LexerCoral, AnalisadorLexico
from src.parser.parser import ParserCoral, ErroSintatico
from src.parser.ast_nodes import *


def tokenizar_codigo(codigo):
    """Helper global para tokenizar código."""
    analisador = LexerCoral.analisar_string(codigo)
    tokens = []
    while True:
        token = analisador.getNextToken()
        tokens.append(token)
        if token.tipo == "EOF":
            break
    return tokens


class TestExpressoesAritmeticas:
    """Testes para expressões aritméticas."""
    
    def parse(self, codigo):
        """Helper para fazer lex + parse."""
        tokens = tokenizar_codigo(codigo)
        parser = ParserCoral(tokens)
        return parser.parse()
    
    def test_soma_simples(self):
        """Testa parsing de soma simples."""
        ast = self.parse("x = 5 + 3")
        assert isinstance(ast, ProgramaNode)
        assert len(ast.declaracoes) == 1
        atrib = ast.declaracoes[0]
        assert isinstance(atrib, AtribuicaoNode)
        assert isinstance(atrib.expressao, ExpressaoBinariaNode)
        assert atrib.expressao.operador.lexema == '+'
    
    def test_subtracao(self):
        """Testa parsing de subtração."""
        ast = self.parse("resultado = 10 - 4")
        atrib = ast.declaracoes[0]
        assert atrib.expressao.operador.lexema == '-'
    
    def test_multiplicacao(self):
        """Testa parsing de multiplicação."""
        ast = self.parse("produto = 6 * 7")
        atrib = ast.declaracoes[0]
        assert atrib.expressao.operador.lexema == '*'
    
    def test_divisao(self):
        """Testa parsing de divisão."""
        ast = self.parse("quociente = 20 / 5")
        atrib = ast.declaracoes[0]
        assert atrib.expressao.operador.lexema == '/'
    
    def test_modulo(self):
        """Testa parsing de módulo."""
        ast = self.parse("resto = 17 % 5")
        atrib = ast.declaracoes[0]
        assert atrib.expressao.operador.lexema == '%'
    
    def test_exponenciacao(self):
        """Testa parsing de exponenciação."""
        ast = self.parse("potencia = 2 ** 8")
        atrib = ast.declaracoes[0]
        assert atrib.expressao.operador.lexema == '**'
    
    def test_precedencia_multiplicacao_soma(self):
        """Testa precedência: multiplicação antes de soma."""
        ast = self.parse("x = 2 + 3 * 4")
        atrib = ast.declaracoes[0]
        # Deve ser: 2 + (3 * 4)
        assert isinstance(atrib.expressao, ExpressaoBinariaNode)
        assert atrib.expressao.operador.lexema == '+'
        assert isinstance(atrib.expressao.direita, ExpressaoBinariaNode)
        assert atrib.expressao.direita.operador.lexema == '*'
    
    def test_parenteses(self):
        """Testa uso de parênteses para forçar precedência."""
        ast = self.parse("x = (2 + 3) * 4")
        atrib = ast.declaracoes[0]
        # Deve ser: (2 + 3) * 4
        assert isinstance(atrib.expressao, ExpressaoBinariaNode)
        assert atrib.expressao.operador.lexema == '*'
        assert isinstance(atrib.expressao.esquerda, ExpressaoBinariaNode)
        assert atrib.expressao.esquerda.operador.lexema == '+'
    
    def test_expressao_unaria_negativa(self):
        """Testa expressão unária com menos."""
        ast = self.parse("x = -5")
        atrib = ast.declaracoes[0]
        assert isinstance(atrib.expressao, ExpressaoUnariaNode)
        assert atrib.expressao.operador.lexema == '-'


class TestExpressoesLogicas:
    """Testes para expressões lógicas e relacionais."""
    
    def parse(self, codigo):
        """Helper para fazer lex + parse."""
        tokens = tokenizar_codigo(codigo)
        parser = ParserCoral(tokens)
        return parser.parse()
    
    def test_comparacao_igualdade(self):
        """Testa comparação de igualdade."""
        ast = self.parse("resultado = x == 10")
        atrib = ast.declaracoes[0]
        assert atrib.expressao.operador.lexema == '=='
    
    def test_comparacao_diferenca(self):
        """Testa comparação de diferença."""
        ast = self.parse("diferente = a != b")
        atrib = ast.declaracoes[0]
        assert atrib.expressao.operador.lexema == '!='
    
    def test_menor_que(self):
        """Testa operador menor que."""
        ast = self.parse("menor = x < 5")
        atrib = ast.declaracoes[0]
        assert atrib.expressao.operador.lexema == '<'
    
    def test_maior_que(self):
        """Testa operador maior que."""
        ast = self.parse("maior = x > 10")
        atrib = ast.declaracoes[0]
        assert atrib.expressao.operador.lexema == '>'
    
    def test_menor_igual(self):
        """Testa operador menor ou igual."""
        ast = self.parse("valido = idade <= 18")
        atrib = ast.declaracoes[0]
        assert atrib.expressao.operador.lexema == '<='
    
    def test_maior_igual(self):
        """Testa operador maior ou igual."""
        ast = self.parse("aprovado = nota >= 7")
        atrib = ast.declaracoes[0]
        assert atrib.expressao.operador.lexema == '>='
    
    def test_operador_e(self):
        """Testa operador lógico E."""
        ast = self.parse("aprovado = nota >= 7 E presenca >= 75")
        atrib = ast.declaracoes[0]
        assert isinstance(atrib.expressao, ExpressaoBinariaNode)
        assert atrib.expressao.operador.lexema == 'E'
    
    def test_operador_ou(self):
        """Testa operador lógico OU."""
        ast = self.parse("especial = vip OU admin")
        atrib = ast.declaracoes[0]
        assert atrib.expressao.operador.lexema == 'OU'
    
    def test_operador_nao(self):
        """Testa operador lógico NAO."""
        ast = self.parse("invalido = NAO ativo")
        atrib = ast.declaracoes[0]
        assert isinstance(atrib.expressao, ExpressaoUnariaNode)
        assert atrib.expressao.operador.lexema == 'NAO'
    
    def test_expressao_logica_complexa(self):
        """Testa combinação de operadores lógicos."""
        ast = self.parse("aprovado = (nota >= 7 E presenca >= 75) OU recuperacao")
        atrib = ast.declaracoes[0]
        assert isinstance(atrib.expressao, ExpressaoBinariaNode)
        assert atrib.expressao.operador.lexema == 'OU'


class TestLiterais:
    """Testes para literais (números, strings, booleanos)."""
    
    def parse(self, codigo):
        """Helper para fazer lex + parse."""
        tokens = tokenizar_codigo(codigo)
        parser = ParserCoral(tokens)
        return parser.parse()
    
    def test_literal_inteiro(self):
        """Testa parsing de literal inteiro."""
        ast = self.parse("x = 42")
        atrib = ast.declaracoes[0]
        assert isinstance(atrib.expressao, LiteralNode)
        assert atrib.expressao.tipo == 'INTEIRO'
    
    def test_literal_decimal(self):
        """Testa parsing de literal decimal."""
        ast = self.parse("pi = 3.14")
        atrib = ast.declaracoes[0]
        assert isinstance(atrib.expressao, LiteralNode)
        assert atrib.expressao.tipo == 'DECIMAL'
    
    def test_literal_string(self):
        """Testa parsing de string literal."""
        ast = self.parse('nome = "Coral"')
        atrib = ast.declaracoes[0]
        assert isinstance(atrib.expressao, LiteralNode)
        assert atrib.expressao.tipo == 'STRING'
    
    def test_literal_booleano_verdadeiro(self):
        """Testa parsing de booleano VERDADE."""
        ast = self.parse("ativo = VERDADE")
        atrib = ast.declaracoes[0]
        assert isinstance(atrib.expressao, LiteralNode)
        assert atrib.expressao.tipo == 'BOOLEANO'
    
    def test_literal_booleano_falso(self):
        """Testa parsing de booleano FALSO."""
        ast = self.parse("inativo = FALSO")
        atrib = ast.declaracoes[0]
        assert isinstance(atrib.expressao, LiteralNode)
        assert atrib.expressao.tipo == 'BOOLEANO'
    
    def test_fstring_simples(self):
        """Testa parsing de f-string."""
        ast = self.parse('mensagem = f"Ola {nome}"')
        atrib = ast.declaracoes[0]
        assert isinstance(atrib.expressao, LiteralNode)
        assert atrib.expressao.formatada == True
    
    def test_lista_vazia(self):
        """Testa parsing de lista vazia."""
        ast = self.parse("lista = []")
        atrib = ast.declaracoes[0]
        assert isinstance(atrib.expressao, ListaNode)
        assert len(atrib.expressao.elementos) == 0
    
    def test_lista_com_elementos(self):
        """Testa parsing de lista com elementos."""
        ast = self.parse("numeros = [1, 2, 3, 4, 5]")
        atrib = ast.declaracoes[0]
        assert isinstance(atrib.expressao, ListaNode)
        assert len(atrib.expressao.elementos) == 5
