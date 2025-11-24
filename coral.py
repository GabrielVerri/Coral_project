#!/usr/bin/env python3
"""
Coral - Interpretador da Linguagem Coral

Este é o executável principal da linguagem Coral.
Permite executar arquivos .crl e realizar análises léxica e sintática.

Uso:
    coral.py <arquivo.crl>                    # Executa análise completa
    coral.py --lex <arquivo.crl>              # Apenas análise léxica
    coral.py --parse <arquivo.crl>            # Apenas análise sintática
    coral.py --help                           # Exibe esta ajuda
    coral.py --version                        # Exibe a versão
"""

import sys
import os
import argparse

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from lexer.lexer import LexerCoral
from parser.parser import ParserCoral, exibir_ast, ErroSintatico
from interpreter.interpreter import executar_programa
from llvm.llvm_compiler import LLVMCompiler

__version__ = "0.1.0"
__author__ = "Coral Language Team"


class CoralInterpreter:
    """Interpretador principal da linguagem Coral."""
    
    def __init__(self, arquivo):
        self.arquivo = arquivo
        self.codigo = None
        self.tokens = []
        self.ast = None
    
    def carregar_arquivo(self):
        """Carrega o código fonte do arquivo."""
        if not os.path.exists(self.arquivo):
            print(f"Erro: Arquivo '{self.arquivo}' não encontrado.")
            sys.exit(1)
        
        try:
            with open(self.arquivo, 'r', encoding='utf-8') as f:
                self.codigo = f.read()
            return True
        except Exception as e:
            print(f"Erro ao ler arquivo: {e}")
            sys.exit(1)
    
    def analise_lexica(self, exibir=True):
        """Realiza análise léxica do código."""
        try:
            lexer = LexerCoral.analisar_arquivo(self.arquivo)
            self.tokens = []
            
            if exibir:
                print(f"{'='*70}")
                print(f"Análise Léxica - Arquivo: {self.arquivo}")
                print(f"{'='*70}")
                print(f"{'TOKEN':<20} | TIPO")
                print("-" * 42)
            
            while True:
                token = lexer.getNextToken()
                self.tokens.append(token)
                
                if exibir and token.tipo != "EOF":
                    print(f"{token.lexema:<20} | {token.tipo}")
                
                if token.tipo == "EOF":
                    break
            
            if exibir:
                print(f"Análise léxica concluída: {len(self.tokens)-1} tokens encontrados.\n")
            
            return True
            
        except Exception as e:
            print(f"\nErro léxico: {e}\n")
            return False
    
    def analise_sintatica(self, exibir=True):
        """Realiza análise sintática do código."""
        if not self.tokens:
            self.analise_lexica(exibir=False)
        
        try:
            parser = ParserCoral(self.tokens)
            self.ast = parser.parse()
            
            if exibir:
                print(f"{'='*70}")
                print(f"Análise Sintática - Arquivo: {self.arquivo}")
                print(f"{'='*70}")
            if exibir:
                print(f"\nAnálise sintática concluída com sucesso!\n")
            
            return True
            
        except ErroSintatico as e:
            print(f"\n{e.formatar_mensagem()}\n")
            return False
        except Exception as e:
            print(f"\nErro inesperado: {type(e).__name__}: {e}\n")
            return False
    
    def _imprimir_ast(self, no, nivel=0):
        """Imprime a árvore AST de forma hierárquica e simples."""
        if no is None:
            return
        
        indentacao = "  " * nivel
        nome_classe = type(no).__name__
        
        # Imprime o nó atual
        print(f"{indentacao}{nome_classe}", end="")
        
        # Adiciona informações específicas do nó
        if hasattr(no, 'nome'):
            print(f"(nome={no.nome})", end="")
        elif hasattr(no, 'valor') and nome_classe == 'LiteralNode':
            valor_repr = repr(no.valor) if isinstance(no.valor, str) else no.valor
            print(f"(valor={valor_repr})", end="")
        elif hasattr(no, 'operador') and nome_classe in ['ExpressaoBinariaNode', 'ExpressaoUnariaNode']:
            op = no.operador.lexema if hasattr(no.operador, 'lexema') else no.operador
            print(f"(op={op})", end="")
        
        print()  # Nova linha
        
        # Processa nós filhos baseado no tipo
        if hasattr(no, 'declaracoes'):  # ProgramaNode
            for decl in no.declaracoes:
                self._imprimir_ast(decl, nivel + 1)
        
        elif hasattr(no, 'instrucoes'):  # BlocoNode
            for instr in no.instrucoes:
                self._imprimir_ast(instr, nivel + 1)
        
        elif nome_classe == 'AtribuicaoNode':
            print(f"{indentacao}  identificador:")
            self._imprimir_ast(no.identificador, nivel + 2)
            print(f"{indentacao}  expressao:")
            self._imprimir_ast(no.expressao, nivel + 2)
        
        elif nome_classe == 'ExpressaoBinariaNode':
            print(f"{indentacao}  esquerda:")
            self._imprimir_ast(no.esquerda, nivel + 2)
            print(f"{indentacao}  direita:")
            self._imprimir_ast(no.direita, nivel + 2)
        
        elif nome_classe == 'ExpressaoUnariaNode':
            print(f"{indentacao}  expressao:")
            self._imprimir_ast(no.expressao, nivel + 2)
        
        elif nome_classe == 'SeNode':
            print(f"{indentacao}  condicao:")
            self._imprimir_ast(no.condicao, nivel + 2)
            print(f"{indentacao}  bloco_se:")
            self._imprimir_ast(no.bloco_se, nivel + 2)
            if no.blocos_senaose:
                print(f"{indentacao}  blocos_senaose:")
                for cond, bloco in no.blocos_senaose:
                    print(f"{indentacao}    condicao:")
                    self._imprimir_ast(cond, nivel + 3)
                    print(f"{indentacao}    bloco:")
                    self._imprimir_ast(bloco, nivel + 3)
            if no.bloco_senao:
                print(f"{indentacao}  bloco_senao:")
                self._imprimir_ast(no.bloco_senao, nivel + 2)
        
        elif nome_classe == 'EnquantoNode':
            print(f"{indentacao}  condicao:")
            self._imprimir_ast(no.condicao, nivel + 2)
            print(f"{indentacao}  bloco:")
            self._imprimir_ast(no.bloco, nivel + 2)
        
        elif nome_classe == 'ParaNode':
            print(f"{indentacao}  variavel: {no.variavel}")
            print(f"{indentacao}  iteravel:")
            self._imprimir_ast(no.iteravel, nivel + 2)
            print(f"{indentacao}  bloco:")
            self._imprimir_ast(no.bloco, nivel + 2)
        
        elif nome_classe == 'FuncaoNode':
            print(f"{indentacao}  parametros: {no.parametros}")
            print(f"{indentacao}  bloco:")
            self._imprimir_ast(no.bloco, nivel + 2)
        
        elif nome_classe == 'ChamadaFuncaoNode':
            if isinstance(no.nome, str):
                print(f"{indentacao}  funcao: {no.nome}")
            else:
                print(f"{indentacao}  funcao:")
                self._imprimir_ast(no.nome, nivel + 2)
            if no.argumentos:
                print(f"{indentacao}  argumentos:")
                for arg in no.argumentos:
                    self._imprimir_ast(arg, nivel + 2)
        
        elif nome_classe == 'RetornarNode':
            if no.expressao:
                print(f"{indentacao}  expressao:")
                self._imprimir_ast(no.expressao, nivel + 2)
        
        elif nome_classe == 'ListaNode':
            if no.elementos:
                print(f"{indentacao}  elementos:")
                for elem in no.elementos:
                    self._imprimir_ast(elem, nivel + 2)
        
        elif nome_classe == 'IndexacaoNode':
            print(f"{indentacao}  objeto:")
            self._imprimir_ast(no.objeto, nivel + 2)
            print(f"{indentacao}  indice:")
            self._imprimir_ast(no.indice, nivel + 2)
        
        elif nome_classe == 'ClasseNode':
            print(f"{indentacao}  bloco:")
            self._imprimir_ast(no.bloco, nivel + 2)
        
        elif nome_classe == 'AcessoAtributoNode':
            print(f"{indentacao}  objeto:")
            self._imprimir_ast(no.objeto, nivel + 2)
            print(f"{indentacao}  atributo: {no.atributo}")
        
        elif nome_classe == 'DicionarioNode':
            if no.pares:
                print(f"{indentacao}  pares:")
                for chave, valor in no.pares:
                    print(f"{indentacao}    chave:")
                    self._imprimir_ast(chave, nivel + 3)
                    print(f"{indentacao}    valor:")
                    self._imprimir_ast(valor, nivel + 3)
    
    def executar(self, modo='completo'):
        """
        Executa o interpretador no modo especificado.
        
        Args:
            modo: 'lex' (apenas léxico), 'parse' (apenas sintático), 
                  'completo' (análise completa + execução), 'ast' (mostra AST),
                  'cat' (exibe conteúdo do arquivo), 'llvmir' (compila para LLVM IR)
        """
        self.carregar_arquivo()
        
        if modo == 'cat':
            # Exibe o conteúdo do arquivo
            print(self.codigo)
            return True
        
        if modo == 'lex':
            return self.analise_lexica()
        
        elif modo == 'parse':
            # Análise sintática: apenas valida a sintaxe
            if not self.analise_lexica(exibir=False):
                return False
            
            if not self.analise_sintatica(exibir=False):
                return False
            
            print(f"\n{'='*70}")
            print(f"✓ Sintaxe válida - {self.arquivo}")
            print(f"{'='*70}")
            print(f"\nO programa está sintaticamente correto!")
            print(f"Use --ast para ver a árvore sintática.\n")
            
            return True
        
        elif modo == 'ast':
            if not self.analise_lexica(exibir=False):
                return False
            
            if not self.analise_sintatica(exibir=True):
                return False
            
            print(f"{'='*70}")
            print(f"AST gerada com sucesso!")
            print(f"{'='*70}\n")
            
            # Imprime a árvore AST
            self._imprimir_ast(self.ast)
            print()
            
            return True
        
        elif modo == 'llvmir':
            # Modo LLVM IR: compila para LLVM
            if not self.analise_lexica(exibir=False):
                return False
            
            if not self.analise_sintatica(exibir=False):
                return False
            
            print(f"{'='*70}")
            print(f"Compilação LLVM IR")
            print(f"{'='*70}\n")
            
            try:
                compiler = LLVMCompiler()
                llvm_code = compiler.compile(self.ast)
                
                # Salva o arquivo .ll
                output_file = self.arquivo.replace('.crl', '.ll')
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(llvm_code)
                
                print(f"[OK] Codigo LLVM IR gerado: {output_file}\n")
                print(llvm_code)
                print(f"\n{'='*70}\n")
                
                return True
            except Exception as e:
                print(f"Erro durante compilação LLVM: {e}", file=sys.stderr)
                import traceback
                traceback.print_exc()
                return False
        
        elif modo == 'completo':
            # Modo completo: executa o programa e mostra apenas o output
            if not self.analise_lexica(exibir=False):
                return False
            
            if not self.analise_sintatica(exibir=False):
                return False
            
            # Executa o programa (apenas output, sem mensagens)
            try:
                from interpreter.interpreter import InterpretadorCoral
                interpretador = InterpretadorCoral()
                interpretador.interpretar(self.ast)
                return True
            except Exception as e:
                print(f"Erro durante execução: {e}", file=sys.stderr)
                return False

def exibir_logo():
    logo = r"""
   ______                 __
  / ____/___  _________ _/ /
 / /   / __ \/ ___/ __ `/ / 
/ /___/ /_/ / /  / /_/ / /  
\____/\____/_/   \__,_/_/   
                             
    """
    print(logo)

def main():
    """Função principal do interpretador."""
    parser = argparse.ArgumentParser(
        prog='coral',
        description='Interpretador da Linguagem Coral',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  coral programa.crl              # Executa o programa
  coral --lex programa.crl        # Apenas análise léxica
  coral --parse programa.crl      # Valida sintaxe
  coral --ast programa.crl        # Exibe a AST
  coral --llvmir programa.crl     # Compila para LLVM IR
  coral --cat programa.crl        # Exibe o conteúdo do arquivo
  coral --logo                    # Exibe o logo do Coral
  coral --version                 # Exibe a versão
  
Para mais informações, visite: https://github.com/GabrielVerri/Coral_project
        """
    )
    
    parser.add_argument(
        'arquivo',
        nargs='?',
        help='Arquivo .crl para executar'
    )
    
    parser.add_argument(
        '--lex',
        action='store_true',
        help='Executar apenas análise léxica'
    )
    
    parser.add_argument(
        '--parse',
        action='store_true',
        help='Validar sintaxe do programa'
    )
    
    parser.add_argument(
        '--ast',
        action='store_true',
        help='Exibir a Árvore Sintática Abstrata (AST)'
    )
    
    parser.add_argument(
        '--cat',
        action='store_true',
        help='Exibir o conteúdo do arquivo'
    )
    
    parser.add_argument(
        '--llvmir',
        action='store_true',
        help='Compilar para LLVM IR'
    )
    
    parser.add_argument(
        '--logo',
        action='store_true',
        help='Exibir o logo do Coral'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version=f'Coral v{__version__}'
    )
    
    args = parser.parse_args()
    
    if args.logo:
        exibir_logo()
        sys.exit(0)
    
    # Verifica se arquivo foi fornecido
    if not args.arquivo:
        parser.print_help()
        sys.exit(1)
    
    # Verifica extensão do arquivo
    if not args.arquivo.endswith('.crl'):
        print(f"Aviso: Arquivo '{args.arquivo}' não possui extensão .crl")
        resposta = input("Deseja continuar? (s/n): ")
        if resposta.lower() != 's':
            sys.exit(0)
    
    # Determina o modo de execução
    if args.lex:
        modo = 'lex'
    elif args.parse:
        modo = 'parse'
    elif args.ast:
        modo = 'ast'
    elif args.cat:
        modo = 'cat'
    elif args.llvmir:
        modo = 'llvmir'
    else:
        modo = 'completo'
    
    # Executa o interpretador
    interpretador = CoralInterpreter(args.arquivo)
    sucesso = interpretador.executar(modo)
    
    sys.exit(0 if sucesso else 1)


if __name__ == "__main__":
    main()
