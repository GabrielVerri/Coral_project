"""
Pacote de AFDs do lexer. Usa o AFD unificado criado a partir da conversão AFN->AFD.
"""

from ..AFN import AFNCoralUnificado
from ..afn_to_afd import ConversorAFNparaAFD
from .AFDUnificado import AFDUnificado

__all__ = [
    "AFDUnificado",
    "get_afd"
]

def get_afd():
    """Retorna o AFD unificado."""
    afn = AFNCoralUnificado()
    conversor = ConversorAFNparaAFD(afn)
    afd_unificado = AFDUnificado(conversor)
    
    return afd_unificado
