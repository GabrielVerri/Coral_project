"""
Testes para parsing de estruturas de controle (SE, PARA, ENQUANTO).
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


class TestEstruturaCondicional:
    """Testes para estrutura SE-SENAO."""
    
    def parse(self, codigo):
        """Helper para fazer lex + parse."""
        tokens = tokenizar_codigo(codigo)
        parser = ParserCoral(tokens)
        return parser.parse()
    
    def test_se_simples(self):
        """Testa SE simples sem SENAO."""
        codigo = """
SE x > 0:
    ESCREVA("Positivo")
"""
        ast = self.parse(codigo)
        assert len(ast.declaracoes) == 1
        se = ast.declaracoes[0]
        assert isinstance(se, SeNode)
        assert se.condicao is not None
        assert len(se.bloco_se.declaracoes) > 0
        assert se.bloco_senao is None
    
    def test_se_senao(self):
        """Testa SE com SENAO."""
        codigo = """
SE idade >= 18:
    ESCREVA("Maior de idade")
SENAO:
    ESCREVA("Menor de idade")
"""
        ast = self.parse(codigo)
        se = ast.declaracoes[0]
        assert isinstance(se, SeNode)
        assert len(se.bloco_se.declaracoes) > 0
        assert len(se.bloco_senao.declaracoes) > 0
    
    def test_se_senao_se(self):
        """Testa SE com múltiplos SENAO SE."""
        codigo = """
SE nota >= 9:
    ESCREVA("A")
SENAOSE nota >= 7:
    ESCREVA("B")
SENAOSE nota >= 5:
    ESCREVA("C")
SENAO:
    ESCREVA("D")
"""
        ast = self.parse(codigo)
        se = ast.declaracoes[0]
        assert isinstance(se, SeNode)
        assert len(se.blocos_senaose) == 2
        assert se.bloco_senao is not None
    
    def test_se_aninhado(self):
        """Testa SE aninhado."""
        codigo = """
SE x > 0:
    SE x < 10:
        ESCREVA("Entre 0 e 10")
"""
        ast = self.parse(codigo)
        se_externo = ast.declaracoes[0]
        assert isinstance(se_externo, SeNode)
        se_interno = se_externo.bloco_se.declaracoes[0]
        assert isinstance(se_interno, SeNode)


class TestLacosPARA:
    """Testes para laço PARA."""
    
    def parse(self, codigo):
        """Helper para fazer lex + parse."""
        tokens = tokenizar_codigo(codigo)
        parser = ParserCoral(tokens)
        return parser.parse()
    
    def test_para_lista(self):
        """Testa PARA iterando sobre lista."""
        codigo = """
PARA item DENTRODE lista:
    ESCREVA(item)
"""
        ast = self.parse(codigo)
        assert len(ast.declaracoes) == 1
        para = ast.declaracoes[0]
        assert isinstance(para, ParaNode)
        assert para.variavel.nome == 'item'
        assert isinstance(para.iteravel, IdentificadorNode)
    
    def test_para_intervalo(self):
        """Testa PARA com INTERVALO."""
        codigo = """
PARA i DENTRODE INTERVALO(10):
    ESCREVA(i)
"""
        ast = self.parse(codigo)
        para = ast.declaracoes[0]
        assert isinstance(para, ParaNode)
        assert isinstance(para.iteravel, ChamadaFuncaoNode)
        assert para.iteravel.nome == 'INTERVALO'
    
    def test_para_intervalo_inicio_fim(self):
        """Testa PARA com INTERVALO(inicio, fim)."""
        codigo = """
PARA i DENTRODE INTERVALO(1, 11):
    ESCREVA(i)
"""
        ast = self.parse(codigo)
        para = ast.declaracoes[0]
        chamada = para.iteravel
        assert len(chamada.argumentos) == 2
    
    def test_para_com_quebra(self):
        """Testa PARA com QUEBRA."""
        codigo = """
PARA i DENTRODE INTERVALO(10):
    SE i == 5:
        QUEBRA
"""
        ast = self.parse(codigo)
        para = ast.declaracoes[0]
        se = para.bloco.declaracoes[0]
        quebra = se.bloco_se.declaracoes[0]
        assert isinstance(quebra, QuebraNode)
    
    def test_para_com_continua(self):
        """Testa PARA com CONTINUA."""
        codigo = """
PARA i DENTRODE INTERVALO(10):
    SE i % 2 == 0:
        CONTINUA
    ESCREVA(i)
"""
        ast = self.parse(codigo)
        para = ast.declaracoes[0]
        se = para.bloco.declaracoes[0]
        continua = se.bloco_se.declaracoes[0]
        assert isinstance(continua, ContinuaNode)


class TestLacosENQUANTO:
    """Testes para laço ENQUANTO."""
    
    def parse(self, codigo):
        """Helper para fazer lex + parse."""
        tokens = tokenizar_codigo(codigo)
        parser = ParserCoral(tokens)
        return parser.parse()
    
    def test_enquanto_simples(self):
        """Testa ENQUANTO simples."""
        codigo = """
ENQUANTO x < 10:
    x = x + 1
"""
        ast = self.parse(codigo)
        assert len(ast.declaracoes) == 1
        enquanto = ast.declaracoes[0]
        assert isinstance(enquanto, EnquantoNode)
        assert enquanto.condicao is not None
        assert len(enquanto.bloco.declaracoes) > 0
    
    def test_enquanto_com_quebra(self):
        """Testa ENQUANTO com QUEBRA."""
        codigo = """
ENQUANTO VERDADEIRO:
    SE condicao:
        QUEBRA
"""
        ast = self.parse(codigo)
        enquanto = ast.declaracoes[0]
        se = enquanto.bloco.declaracoes[0]
        quebra = se.bloco_se.declaracoes[0]
        assert isinstance(quebra, QuebraNode)
    
    def test_enquanto_aninhado(self):
        """Testa ENQUANTO aninhado."""
        codigo = """
ENQUANTO x < 10:
    ENQUANTO y < 5:
        y = y + 1
    x = x + 1
"""
        ast = self.parse(codigo)
        enquanto_externo = ast.declaracoes[0]
        enquanto_interno = enquanto_externo.bloco.declaracoes[0]
        assert isinstance(enquanto_externo, EnquantoNode)
        assert isinstance(enquanto_interno, EnquantoNode)


class TestErrosSintaticos:
    """Testes para validação de erros sintáticos."""
    
    def parse(self, codigo):
        """Helper para fazer lex + parse."""
        tokens = tokenizar_codigo(codigo)
        parser = ParserCoral(tokens)
        return parser.parse()
        return parser.parse()
    
    def test_string_sem_aspas(self):
        """Testa erro de string sem aspas."""
        codigo = "texto = Ola Mundo"
        with pytest.raises(ErroSintatico) as exc_info:
            self.parse(codigo)
        assert "String sem aspas" in str(exc_info.value)
    
    def test_falta_dois_pontos_se(self):
        """Testa erro de falta de dois-pontos no SE."""
        codigo = """
SE x > 0
    ESCREVA("Positivo")
"""
        with pytest.raises(ErroSintatico):
            self.parse(codigo)
    
    def test_falta_dois_pontos_para(self):
        """Testa erro de falta de dois-pontos no PARA."""
        codigo = """
PARA i DENTRODE INTERVALO(10)
    ESCREVA(i)
"""
        with pytest.raises(ErroSintatico):
            self.parse(codigo)
    
    def test_quebra_fora_laco(self):
        """Testa QUEBRA fora de laço."""
        codigo = """
x = 5
QUEBRA
"""
        with pytest.raises(ErroSintatico) as exc_info:
            self.parse(codigo)
        assert "QUEBRA" in str(exc_info.value)
    
    def test_continua_fora_laco(self):
        """Testa CONTINUA fora de laço."""
        codigo = """
x = 10
CONTINUA
"""
        with pytest.raises(ErroSintatico) as exc_info:
            self.parse(codigo)
        assert "CONTINUA" in str(exc_info.value)
