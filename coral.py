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
                print(f"{'='*70}\n")
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
                print(f"\nAnálise léxica concluída: {len(self.tokens)-1} tokens encontrados.\n")
            
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
                print(f"{'='*70}\n")
            if exibir:
                print(f"\nAnálise sintática concluída com sucesso!\n")
            
            return True
            
        except ErroSintatico as e:
            print(f"\n{e.formatar_mensagem()}\n")
            return False
        except Exception as e:
            print(f"\nErro inesperado: {type(e).__name__}: {e}\n")
            return False
    
    def executar(self, modo='completo'):
        """
        Executa o interpretador no modo especificado.
        
        Args:
            modo: 'lex' (apenas léxico), 'parse' (apenas sintático), 
                  'completo' (análise completa + execução), 'ast' (mostra AST),
                  'cat' (exibe conteúdo do arquivo)
        """
        self.carregar_arquivo()
        
        if modo == 'cat':
            # Exibe o conteúdo do arquivo
            print(self.codigo)
            return True
        
        if modo == 'lex':
            return self.analise_lexica()
        
        elif modo == 'parse':
            return self.analise_sintatica()
        
        elif modo == 'ast':
            # Modo especial: mostra a AST sem executar
            print(f"\n{'='*70}")
            print(f"Coral Language 🐍 Interpreter")
            print(f"{'='*70}\n")
            
            if not self.analise_lexica(exibir=False):
                return False
            
            if not self.analise_sintatica(exibir=True):
                return False
            
            print(f"{'='*70}")
            print(f"AST gerada com sucesso!")
            print(f"{'='*70}\n")
            
            return True
        
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
  coral --parse programa.crl      # Apenas análise sintática
  coral --ast programa.crl        # Exibe a AST
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
        help='Executar apenas análise sintática'
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
    else:
        modo = 'completo'
    
    # Executa o interpretador
    interpretador = CoralInterpreter(args.arquivo)
    sucesso = interpretador.executar(modo)
    
    sys.exit(0 if sucesso else 1)


if __name__ == "__main__":
    main()
