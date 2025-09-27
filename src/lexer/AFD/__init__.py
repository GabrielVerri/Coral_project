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
    (AFDComentariosLinha, "Comentários de linha"),          # 1. Comentários (padrão claro, ignora o resto)
    (AFDStringLiteral, "Strings literais"),                 # 2. Strings (padrão delimitado, evita conflitos)
    (AFDIdentificadores, "Identificadores e palavras reservadas"),  # 3. Identificadores (deve vir cedo para rejeitar inválidos)
    (AFDSimbolos, "Símbolos/pontuação"),                    # 4. Símbolos (caracteres simples como '(', ')', evita conflitos com operadores)
    (AFDOperadoresAritmeticosRelacionais, "Operadores aritméticos/relacionais"),  # 5. Operadores compostos (ex.: ==, <=)
    (AFDOperadoresLogicos, "Operadores lógicos"),           # 6. Operadores lógicos (ex.: E, OU, NAO)
    (AFDOperadoresBooleanos, "Operadores booleanos"),       # 7. Operadores booleanos (ex.: VERDADE, FALSO)
    (AFDDecimal, "Números (inteiros e decimais)")           # 8. Números (deve vir por último para evitar consumir partes de identificadores)
]

def get_afds():
    """Retorna uma lista de instâncias de AFDs na ordem correta de prioridade"""
    return [afd() for afd, _ in _afds]
