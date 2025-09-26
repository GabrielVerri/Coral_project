"""
Pacote de AFDs do lexer. Define a ordem e prioridade dos autômatos.
"""

from .AFDComentariosLinha import AFDComentariosLinha
from .AFDStringLiteral import AFDStringLiteral
from .AFDSimbolos import AFDSimbolos
from .AFDDecimal import AFDDecimal
from .AFDOperadoresAritmeticosRelacionais import AFDOperadoresAritmeticosRelacionais
from .AFDOperadoresLogicos import AFDOperadoresLogicos
from .AFDOperadoresBooleanos import AFDOperadoresBooleanos
from .AFDIdentificadores import AFDIdentificadores

__all__ = [
    "AFDIdentificadores",
    "AFDDecimal",
    "AFDComentariosLinha",
    "AFDOperadoresBooleanos",
    "AFDOperadoresAritmeticosRelacionais",
    "AFDOperadoresLogicos",
    "AFDStringLiteral",
    "AFDSimbolos",
    "get_afds"
]

# Lista de AFDs na ordem de prioridade que serão usados pelo scanner
_afds = [
    (AFDComentariosLinha, "Comentários de linha"),
    (AFDStringLiteral, "Strings literais"), 
    (AFDSimbolos, "Símbolos/pontuação"),
    (AFDDecimal, "Números (inteiros e decimais)"),
    (AFDOperadoresAritmeticosRelacionais, "Operadores aritméticos/relacionais"),
    (AFDOperadoresLogicos, "Operadores lógicos"),
    (AFDOperadoresBooleanos, "Operadores booleanos"),
    (AFDIdentificadores, "Identificadores e palavras reservadas")
]

def get_afds():
    """Retorna uma lista de instâncias de AFDs na ordem correta de prioridade"""
    return [afd() for afd, _ in _afds]
