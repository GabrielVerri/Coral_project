"""
Testes para geração de LLVM IR a partir da AST.
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.lexer.lexer import LexerCoral
from src.parser.parser import ParserCoral
from src.parser.ast_nodes import *
from src.llvm.llvm_compiler import LLVMCompiler


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


class TestLLVMIRBasico:
    """Testes básicos para geração de LLVM IR."""
    
    def parse(self, codigo):
        """Helper para fazer lex + parse."""
        tokens = tokenizar_codigo(codigo)
        
        parser = ParserCoral(tokens)
        return parser.parse()
    
    def compile(self, codigo):
        """Helper para compilar para LLVM IR."""
        ast = self.parse(codigo)
        compiler = LLVMCompiler()
        return compiler.compile(ast)
    
    def test_declaracao_variavel_inteira(self):
        """Testa geração de IR para declaração de variável inteira."""
        ir = self.compile("x = 42")
        assert "alloca i32" in ir
        assert "store i32 42" in ir
    
    def test_operacao_aritmetica_soma(self):
        """Testa geração de IR para soma."""
        ir = self.compile("resultado = 10 + 20")
        assert "add" in ir
        assert "i32" in ir
    
    def test_operacao_aritmetica_multiplicacao(self):
        """Testa geração de IR para multiplicação."""
        ir = self.compile("produto = 5 * 6")
        assert "mul" in ir
        assert "i32" in ir


class TestLLVMIRControleFluxo:
    """Testes para geração de IR de estruturas de controle."""
    
    def parse(self, codigo):
        """Helper para fazer lex + parse."""
        tokens = tokenizar_codigo(codigo)
        
        parser = ParserCoral(tokens)
        return parser.parse()
    
    def compile(self, codigo):
        """Helper para compilar para LLVM IR."""
        ast = self.parse(codigo)
        compiler = LLVMCompiler()
        return compiler.compile(ast)
    
    def test_estrutura_se(self):
        """Testa geração de IR para SE."""
        codigo = """
x = 0
SE x > 0:
    y = 1
SENAO:
    y = 0
"""
        ir = self.compile(codigo)
        assert "br i1" in ir or "br label" in ir
        assert "icmp" in ir
    
    def test_laco_enquanto(self):
        """Testa geração de IR para ENQUANTO."""
        codigo = """
x = 0
ENQUANTO x < 10:
    x = x + 1
"""
        ir = self.compile(codigo)
        assert "br label" in ir
        assert "icmp" in ir


class TestLLVMIRFuncoes:
    """Testes para geração de IR de funções."""
    
    def parse(self, codigo):
        """Helper para fazer lex + parse."""
        tokens = tokenizar_codigo(codigo)
        
        parser = ParserCoral(tokens)
        return parser.parse()
    
    def compile(self, codigo):
        """Helper para compilar para LLVM IR."""
        ast = self.parse(codigo)
        compiler = LLVMCompiler()
        return compiler.compile(ast)
    
    def test_funcao_simples(self):
        """Testa declaração de função simples sem parâmetros."""
        codigo = """
FUNCAO saudacao():
    ESCREVA("Ola")
"""
        ir = self.compile(codigo)
        assert "define i32 @saudacao()" in ir
        assert "ret i32 0" in ir
    
    def test_funcao_com_parametros(self):
        """Testa função com parâmetros."""
        codigo = """
FUNCAO somar(a: INTEIRO, b: INTEIRO):
    resultado = a + b
    RETORNAR resultado
"""
        ir = self.compile(codigo)
        assert "define i32 @somar(i32 %a, i32 %b)" in ir
        assert "add" in ir
        assert "ret i32" in ir
    
    def test_funcao_com_retorno(self):
        """Testa função com RETORNAR."""
        codigo = """
FUNCAO dobro(x: INTEIRO) -> INTEIRO:
    RETORNAR x * 2
"""
        ir = self.compile(codigo)
        assert "define i32 @dobro(i32 %x)" in ir
        assert "mul" in ir
        assert "ret i32" in ir
    
    def test_chamada_funcao(self):
        """Testa chamada de função definida pelo usuário."""
        codigo = """
FUNCAO soma(a: INTEIRO, b: INTEIRO) -> INTEIRO:
    RETORNAR a + b

resultado = soma(10, 20)
"""
        ir = self.compile(codigo)
        assert "define i32 @soma(i32 %a, i32 %b)" in ir
        assert "call i32 @soma(i32 10, i32 20)" in ir
    
    def test_funcao_sem_retorno_explicito(self):
        """Testa função sem RETORNAR (retorno padrão)."""
        codigo = """
FUNCAO imprimir(n: INTEIRO):
    ESCREVA(n)
"""
        ir = self.compile(codigo)
        assert "define i32 @imprimir(i32 %n)" in ir
        assert "ret i32 0" in ir


# Teste funcional que pode rodar agora: verifica se AST está correta para futura geração de IR
class TestASTParaLLVMIR:
    """Testes que verificam se a AST tem informações necessárias para gerar LLVM IR."""
    
    def parse(self, codigo):
        """Helper para fazer lex + parse."""
        tokens = tokenizar_codigo(codigo)
        parser = ParserCoral(tokens)
        return parser.parse()
    
    def test_ast_contem_tipos(self):
        """Verifica se AST contém informações de tipo em parâmetros de função."""
        codigo = """
FUNCAO calcular(x: INTEIRO, y: DECIMAL) -> TEXTO:
    RETORNAR "ok"
"""
        ast = self.parse(codigo)
        funcao = ast.declaracoes[0]
        # Verifica se temos informação de tipo nos parâmetros
        assert isinstance(funcao, FuncaoNode)
        assert funcao.parametros[0].tipo_anotacao == 'INTEIRO'
        assert funcao.parametros[1].tipo_anotacao == 'DECIMAL'
        assert funcao.tipo_retorno == 'TEXTO'
    
    def test_ast_funcao_tem_tipos_parametros(self):
        """Verifica se função na AST tem tipos de parâmetros."""
        codigo = """
FUNCAO teste(a: INTEIRO, b: DECIMAL) -> TEXTO:
    RETORNAR "ok"
"""
        ast = self.parse(codigo)
        funcao = ast.declaracoes[0]
        assert isinstance(funcao, FuncaoNode)
        assert len(funcao.parametros) == 2
        # Cada parâmetro deve ter tipo_anotacao
        assert funcao.parametros[0].tipo_anotacao == 'INTEIRO'
        assert funcao.parametros[1].tipo_anotacao == 'DECIMAL'
        assert funcao.tipo_retorno == 'TEXTO'
    
    def test_ast_expressao_tem_operadores(self):
        """Verifica se expressões mantêm operadores."""
        ast = self.parse("x = 10 + 20 * 3")
        atrib = ast.declaracoes[0]
        expr = atrib.expressao
        assert isinstance(expr, ExpressaoBinariaNode)
        assert hasattr(expr, 'operador')
        assert expr.operador.lexema in ['+', '-', '*', '/', '%', '**']
    
    def test_ast_estrutura_se_completa(self):
        """Verifica se estrutura SE tem todas as partes necessárias."""
        codigo = """
SE x > 0:
    y = 1
SENAO:
    y = -1
"""
        ast = self.parse(codigo)
        se = ast.declaracoes[0]
        assert isinstance(se, SeNode)
        assert se.condicao is not None
        assert se.bloco_se is not None
        assert se.bloco_senao is not None
    
    def test_ast_laco_para_tem_iteravel(self):
        """Verifica se laço PARA mantém informação do iterável."""
        codigo = """
PARA i DENTRODE INTERVALO(10):
    ESCREVA(i)
"""
        ast = self.parse(codigo)
        para = ast.declaracoes[0]
        assert isinstance(para, ParaNode)
        assert hasattr(para, 'iteravel')
        assert hasattr(para, 'variavel')
        assert hasattr(para, 'bloco')
