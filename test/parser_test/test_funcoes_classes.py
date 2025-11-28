"""
Testes para parsing de funções e classes.
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.lexer.lexer import LexerCoral
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


class TestFuncoes:
    """Testes para declaração e chamada de funções."""
    
    def parse(self, codigo):
        """Helper para fazer lex + parse."""
        tokens = tokenizar_codigo(codigo)
        parser = ParserCoral(tokens)
        return parser.parse()
    
    def test_funcao_sem_parametros(self):
        """Testa declaração de função sem parâmetros."""
        codigo = """
FUNCAO ola():
    ESCREVA("Ola!")
"""
        ast = self.parse(codigo)
        assert len(ast.declaracoes) == 1
        funcao = ast.declaracoes[0]
        assert isinstance(funcao, FuncaoNode)
        assert funcao.nome == 'ola'
        assert len(funcao.parametros) == 0
    
    def test_funcao_com_parametros(self):
        """Testa declaração de função com parâmetros."""
        codigo = """
FUNCAO somar(a, b):
    RETORNAR a + b
"""
        ast = self.parse(codigo)
        funcao = ast.declaracoes[0]
        assert len(funcao.parametros) == 2
        assert funcao.parametros[0].nome == 'a'
        assert funcao.parametros[1].nome == 'b'
    
    def test_funcao_com_tipos(self):
        """Testa declaração de função com anotações de tipo."""
        codigo = """
FUNCAO somar(a: INTEIRO, b: INTEIRO) -> INTEIRO:
    RETORNAR a + b
"""
        ast = self.parse(codigo)
        funcao = ast.declaracoes[0]
        assert funcao.parametros[0].tipo_anotacao == 'INTEIRO'
        assert funcao.parametros[1].tipo_anotacao == 'INTEIRO'
        assert funcao.tipo_retorno == 'INTEIRO'
    
    def test_funcao_com_retorno(self):
        """Testa função com RETORNAR."""
        codigo = """
FUNCAO dobro(x):
    RETORNAR x * 2
"""
        ast = self.parse(codigo)
        funcao = ast.declaracoes[0]
        retorno = funcao.bloco.declaracoes[0]
        assert isinstance(retorno, RetornarNode)
        assert retorno.expressao is not None
    
    def test_funcao_sem_retorno(self):
        """Testa função sem RETORNAR (procedimento)."""
        codigo = """
FUNCAO imprimir(mensagem):
    ESCREVA(mensagem)
"""
        ast = self.parse(codigo)
        funcao = ast.declaracoes[0]
        assert isinstance(funcao, FuncaoNode)
        # Não deve ter RetornarNode no bloco
        assert not any(isinstance(cmd, RetornarNode) for cmd in funcao.bloco.declaracoes)
    
    def test_chamada_funcao_sem_args(self):
        """Testa chamada de função sem argumentos."""
        codigo = """
resultado = calcular()
"""
        ast = self.parse(codigo)
        atrib = ast.declaracoes[0]
        assert isinstance(atrib.expressao, ChamadaFuncaoNode)
        assert len(atrib.expressao.argumentos) == 0
    
    def test_chamada_funcao_com_args(self):
        """Testa chamada de função com argumentos."""
        codigo = """
soma = somar(10, 20)
"""
        ast = self.parse(codigo)
        atrib = ast.declaracoes[0]
        chamada = atrib.expressao
        assert isinstance(chamada, ChamadaFuncaoNode)
        assert len(chamada.argumentos) == 2
    
    def test_funcao_aninhada(self):
        """Testa função declarada dentro de outra."""
        codigo = """
FUNCAO externa():
    FUNCAO interna():
        ESCREVA("Interna")
    interna()
"""
        ast = self.parse(codigo)
        funcao_externa = ast.declaracoes[0]
        funcao_interna = funcao_externa.bloco.declaracoes[0]
        assert isinstance(funcao_interna, FuncaoNode)


class TestClasses:
    """Testes para declaração e uso de classes."""
    
    def parse(self, codigo):
        """Helper para fazer lex + parse."""
        tokens = tokenizar_codigo(codigo)
        parser = ParserCoral(tokens)
        return parser.parse()
    
    def test_classe_simples(self):
        """Testa declaração de classe simples."""
        codigo = """
CLASSE Pessoa:
    PASSAR
"""
        ast = self.parse(codigo)
        assert len(ast.declaracoes) == 1
        classe = ast.declaracoes[0]
        assert isinstance(classe, ClasseNode)
        assert classe.nome == 'Pessoa'
    
    def test_classe_com_construtor(self):
        """Testa classe com __construtor__."""
        codigo = """
CLASSE Pessoa:
    FUNCAO __construtor__(self, nome, idade):
        self.nome = nome
        self.idade = idade
"""
        ast = self.parse(codigo)
        classe = ast.declaracoes[0]
        construtor = classe.bloco.declaracoes[0]
        assert isinstance(construtor, FuncaoNode)
        assert construtor.nome == '__construtor__'
        assert construtor.parametros[0].nome == 'self'
    
    def test_classe_com_metodos(self):
        """Testa classe com métodos."""
        codigo = """
CLASSE Calculadora:
    FUNCAO somar(self, a, b):
        RETORNAR a + b
    
    FUNCAO subtrair(self, a, b):
        RETORNAR a - b
"""
        ast = self.parse(codigo)
        classe = ast.declaracoes[0]
        assert len(classe.bloco.declaracoes) == 2
        assert all(isinstance(m, FuncaoNode) for m in classe.bloco.declaracoes)
    
    def test_acesso_atributo(self):
        """Testa acesso a atributo (self.atributo)."""
        codigo = """
CLASSE Pessoa:
    FUNCAO obter_nome(self):
        RETORNAR self.nome
"""
        ast = self.parse(codigo)
        classe = ast.declaracoes[0]
        metodo = classe.bloco.declaracoes[0]
        retorno = metodo.bloco.declaracoes[0]
        assert isinstance(retorno.expressao, AcessoAtributoNode)
        assert retorno.expressao.atributo == 'nome'
    
    def test_chamada_metodo(self):
        """Testa chamada de método (objeto.metodo())."""
        codigo = """
resultado = pessoa.obter_nome()
"""
        ast = self.parse(codigo)
        atrib = ast.declaracoes[0]
        chamada = atrib.expressao
        assert isinstance(chamada, ChamadaFuncaoNode)
        assert isinstance(chamada.nome, AcessoAtributoNode)
    
    def test_instanciacao_classe(self):
        """Testa instanciação de classe."""
        codigo = """
p = Pessoa("Ian", 21)
"""
        ast = self.parse(codigo)
        atrib = ast.declaracoes[0]
        assert isinstance(atrib.expressao, ChamadaFuncaoNode)
        assert len(atrib.expressao.argumentos) == 2


class TestIndexacao:
    """Testes para indexação de listas."""
    
    def parse(self, codigo):
        """Helper para fazer lex + parse."""
        tokens = tokenizar_codigo(codigo)
        parser = ParserCoral(tokens)
        return parser.parse()
    
    def test_acesso_indice_simples(self):
        """Testa acesso por índice simples."""
        codigo = """
primeiro = lista[0]
"""
        ast = self.parse(codigo)
        atrib = ast.declaracoes[0]
        assert isinstance(atrib.expressao, IndexacaoNode)
        assert isinstance(atrib.expressao.indice, LiteralNode)
    
    def test_acesso_indice_variavel(self):
        """Testa acesso por índice com variável."""
        codigo = """
elemento = lista[i]
"""
        ast = self.parse(codigo)
        atrib = ast.declaracoes[0]
        assert isinstance(atrib.expressao, IndexacaoNode)
        assert isinstance(atrib.expressao.indice, IdentificadorNode)
    
    def test_indexacao_encadeada(self):
        """Testa indexação encadeada (matriz[i][j])."""
        codigo = """
valor = matriz[0][1]
"""
        ast = self.parse(codigo)
        atrib = ast.declaracoes[0]
        # matriz[0] é um IndexacaoNode
        # matriz[0][1] é outro IndexacaoNode cujo objeto é matriz[0]
        assert isinstance(atrib.expressao, IndexacaoNode)
        assert isinstance(atrib.expressao.objeto, IndexacaoNode)
    
    def test_atribuicao_indice(self):
        """Testa atribuição em índice."""
        codigo = """
lista[0] = 10
"""
        ast = self.parse(codigo)
        atrib = ast.declaracoes[0]
        assert isinstance(atrib.identificador, IndexacaoNode)
    
    def test_operador_composto_indice(self):
        """Testa operador composto com índice."""
        codigo = """
valores[0] += 5
"""
        ast = self.parse(codigo)
        atrib = ast.declaracoes[0]
        assert isinstance(atrib.identificador, IndexacaoNode)
        assert atrib.operador == '+='


class TestOperadoresCompostos:
    """Testes para operadores compostos (+=, -=, etc)."""
    
    def parse(self, codigo):
        """Helper para fazer lex + parse."""
        tokens = tokenizar_codigo(codigo)
        parser = ParserCoral(tokens)
        return parser.parse()
    
    def test_mais_igual(self):
        """Testa operador +=."""
        ast = self.parse("x += 5")
        atrib = ast.declaracoes[0]
        assert atrib.operador == '+='
    
    def test_menos_igual(self):
        """Testa operador -=."""
        ast = self.parse("x -= 3")
        atrib = ast.declaracoes[0]
        assert atrib.operador == '-='
    
    def test_vezes_igual(self):
        """Testa operador *=."""
        ast = self.parse("x *= 2")
        atrib = ast.declaracoes[0]
        assert atrib.operador == '*='
    
    def test_dividir_igual(self):
        """Testa operador /=."""
        ast = self.parse("x /= 4")
        atrib = ast.declaracoes[0]
        assert atrib.operador == '/='
    
    def test_modulo_igual(self):
        """Testa operador %=."""
        ast = self.parse("x %= 10")
        atrib = ast.declaracoes[0]
        assert atrib.operador == '%='
