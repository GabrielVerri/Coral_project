"""
Script para testar o Parser com arquivos .crl de exemplo.

Este script carrega e analisa todos os arquivos .crl do diretório
exemplos/parser/, exibindo a AST gerada para cada um.
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.lexer import AnalisadorLexico
from src.parser import ParserCoral, ErroSintatico


def exibir_ast(node, indent=0, max_depth=5):
    """
    Exibe a AST de forma hierárquica e legível.
    
    Args:
        node: Nó da AST
        indent: Nível de indentação
        max_depth: Profundidade máxima para evitar recursão excessiva
    """
    if indent > max_depth:
        print("  " * indent + "...")
        return
    
    prefix = "  " * indent
    print(f"{prefix}{node}")
    
    # Exibe filhos dependendo do tipo de nó
    if hasattr(node, 'declaracoes') and node.declaracoes:
        for decl in node.declaracoes[:10]:  # Limita a 10 declarações
            exibir_ast(decl, indent + 1, max_depth)
        if len(node.declaracoes) > 10:
            print("  " * (indent + 1) + f"... e mais {len(node.declaracoes) - 10} declarações")
    
    elif hasattr(node, 'esquerda') and hasattr(node, 'direita'):
        if node.esquerda:
            exibir_ast(node.esquerda, indent + 1, max_depth)
        if node.direita:
            exibir_ast(node.direita, indent + 1, max_depth)
    
    elif hasattr(node, 'expressao') and node.expressao:
        exibir_ast(node.expressao, indent + 1, max_depth)
    
    elif hasattr(node, 'condicao') and hasattr(node, 'bloco_se'):
        print(f"{prefix}  Condição:")
        exibir_ast(node.condicao, indent + 2, max_depth)
        print(f"{prefix}  Bloco SE:")
        exibir_ast(node.bloco_se, indent + 2, max_depth)
        if hasattr(node, 'bloco_senao') and node.bloco_senao:
            print(f"{prefix}  Bloco SENAO:")
            exibir_ast(node.bloco_senao, indent + 2, max_depth)
    
    elif hasattr(node, 'bloco') and node.bloco:
        if hasattr(node, 'parametros'):  # Função
            print(f"{prefix}  Parâmetros: {len(node.parametros)}")
        exibir_ast(node.bloco, indent + 1, max_depth)


def analisar_arquivo(caminho_arquivo):
    """
    Analisa um arquivo .crl e exibe a AST gerada.
    
    Args:
        caminho_arquivo: Caminho para o arquivo .crl
    """
    print(f"\n{'='*70}")
    print(f"Arquivo: {os.path.basename(caminho_arquivo)}")
    print(f"{'='*70}")
    
    try:
        # Lê o conteúdo do arquivo
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
        
        print(f"\nCódigo fonte:")
        print("-" * 70)
        print(codigo)
        print("-" * 70)
        
        # Análise léxica
        print(f"\n[1/2] Análise Léxica...")
        lexer = AnalisadorLexico(codigo)
        tokens = lexer.analisar()
        print(f"✓ {len(tokens)} tokens gerados")
        
        # Análise sintática
        print(f"\n[2/2] Análise Sintática...")
        parser = ParserCoral(tokens)
        ast = parser.parse()
        print(f"✓ AST construída com sucesso!")
        
        # Exibe a AST
        print(f"\nÁrvore Sintática Abstrata (AST):")
        print("-" * 70)
        exibir_ast(ast)
        print("-" * 70)
        
        print(f"\n✅ Análise concluída com sucesso!\n")
        return True
        
    except ErroSintatico as e:
        print(f"\n❌ Erro Sintático:")
        print(f"   {e.formatar_mensagem()}\n")
        return False
        
    except Exception as e:
        print(f"\n❌ Erro inesperado: {type(e).__name__}")
        print(f"   {e}\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Função principal que executa todos os testes."""
    # Diretório com os exemplos
    diretorio_exemplos = Path(__file__).parent
    
    # Lista todos os arquivos .crl
    arquivos_crl = sorted(diretorio_exemplos.glob("*.crl"))
    
    if not arquivos_crl:
        print("⚠️  Nenhum arquivo .crl encontrado no diretório exemplos/parser/")
        return
    
    print(f"\n{'#'*70}")
    print(f"# Parser Coral - Teste com Arquivos .crl")
    print(f"{'#'*70}")
    print(f"\nEncontrados {len(arquivos_crl)} arquivos para análise:\n")
    
    for i, arquivo in enumerate(arquivos_crl, 1):
        print(f"  {i}. {arquivo.name}")
    
    # Analisa cada arquivo
    resultados = []
    for arquivo in arquivos_crl:
        sucesso = analisar_arquivo(arquivo)
        resultados.append((arquivo.name, sucesso))
    
    # Resumo final
    print(f"\n{'='*70}")
    print(f"RESUMO DOS TESTES")
    print(f"{'='*70}\n")
    
    sucessos = sum(1 for _, s in resultados if s)
    falhas = len(resultados) - sucessos
    
    for nome, sucesso in resultados:
        status = "✅ SUCESSO" if sucesso else "❌ FALHOU"
        print(f"  {status}: {nome}")
    
    print(f"\n{'='*70}")
    print(f"Total: {len(resultados)} arquivos")
    print(f"Sucessos: {sucessos}")
    print(f"Falhas: {falhas}")
    print(f"{'='*70}\n")
    
    if falhas == 0:
        print("🎉 Todos os testes passaram com sucesso!")
    else:
        print(f"⚠️  {falhas} teste(s) falharam.")
    
    return falhas == 0


if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1)
