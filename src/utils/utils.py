"""
Utilitários e constantes compartilhadas da linguagem Coral.

Este módulo centraliza definições utilizadas por múltiplos componentes
do compilador, como palavras reservadas, operadores e mapeamentos de tipos.

Uso:
    from src.utils import PALAVRAS_RESERVADAS, OPERADORES_LOGICOS
    
    # Verificar se é palavra reservada
    if lexema in PALAVRAS_RESERVADAS:
        ...
    
    # Exibir tabelas de referência
    from src.utils import exibir_tabelas
    exibir_tabelas()
"""

# ===== PALAVRAS RESERVADAS =====

PALAVRAS_RESERVADAS = {
    # Estruturas de controle
    'SE', 'SENAO', 'SENAOSE', 'ENQUANTO', 'PARA', 'DENTRODE',
    # Controle de fluxo
    'QUEBRA', 'CONTINUA', 'PASSAR', 'RETORNAR',
    # Definições
    'FUNCAO', 'CLASSE',
    # Literais e tipos
    'VAZIO',
}

# ===== OPERADORES =====

OPERADORES_LOGICOS = {'E', 'OU', 'NAO'}

OPERADORES_BOOLEANOS = {'VERDADE', 'FALSO'}

OPERADORES_ARITMETICOS = {'+', '-', '*', '/', '%', '**'}

OPERADORES_RELACIONAIS = {'==', '!=', '<', '>', '<=', '>='}

OPERADORES_ATRIBUICAO = {'=', '+=', '-=', '*=', '/=', '%='}

DELIMITADORES = {'(', ')', '[', ']', '{', '}', ':', ','}

# ===== MAPEAMENTOS DE TIPOS =====

TIPO_MAP = {
    'ID': 'IDENTIFICADOR',
    'STRING': 'STRING',
    'BOOLEANO': 'BOOLEANO',
    'NEWLINE': 'NEWLINE',
    'INDENTA': 'INDENTA',
    'DEDENTA': 'DEDENTA',
    'EOF': 'EOF'
}

# ===== TABELA DE PALAVRAS RESERVADAS (para exibição) =====

TABELA_PALAVRAS_RESERVADAS = """
╔═══════════════════════════════════════════════════════════════════╗
║                      PALAVRAS RESERVADAS                          ║
╠═══════════════════════════════════════════════════════════════════╣
║ Estruturas de Controle:                                           ║
║   SE, SENAO, SENAOSE, ENQUANTO, PARA, DENTRODE                    ║
║                                                                   ║
║ Controle de Fluxo:                                                ║
║   QUEBRA, CONTINUA, PASSAR, RETORNAR                              ║
║                                                                   ║
║ Definições:                                                       ║
║   FUNCAO, CLASSE                                                  ║
║                                                                   ║
║ Literais e Tipos:                                                 ║
║   VAZIO, VERDADE, FALSO                                           ║
╚═══════════════════════════════════════════════════════════════════╝
"""

# ===== TABELA DE OPERADORES (para exibição) =====

TABELA_OPERADORES = """
╔═══════════════════════════════════════════════════════════════════╗
║                           OPERADORES                              ║
╠═══════════════════════════════════════════════════════════════════╣
║ Lógicos:                                                          ║
║   E, OU, NAO                                                      ║
║                                                                   ║
║ Aritméticos:                                                      ║
║   +, -, *, /, %, **                                               ║
║                                                                   ║
║ Relacionais:                                                      ║
║   ==, !=, <, >, <=, >=                                            ║
║                                                                   ║
║ Atribuição:                                                       ║
║   =, +=, -=, *=, /=, %=                                           ║
╚═══════════════════════════════════════════════════════════════════╝
"""


def exibir_tabelas():
    """Exibe as tabelas de palavras reservadas e operadores."""
    print(TABELA_PALAVRAS_RESERVADAS)
    print(TABELA_OPERADORES)


def eh_palavra_reservada(lexema):
    """
    Verifica se um lexema é uma palavra reservada.
    
    Args:
        lexema: String a verificar
        
    Returns:
        bool: True se for palavra reservada, False caso contrário
    """
    return lexema in PALAVRAS_RESERVADAS


def eh_operador_logico(lexema):
    """
    Verifica se um lexema é um operador lógico.
    
    Args:
        lexema: String a verificar
        
    Returns:
        bool: True se for operador lógico, False caso contrário
    """
    return lexema in OPERADORES_LOGICOS


def eh_operador_booleano(lexema):
    """
    Verifica se um lexema é um operador booleano.
    
    Args:
        lexema: String a verificar
        
    Returns:
        bool: True se for operador booleano, False caso contrário
    """
    return lexema in OPERADORES_BOOLEANOS


if __name__ == "__main__":
    # Exibe tabelas quando executado diretamente
    exibir_tabelas()
