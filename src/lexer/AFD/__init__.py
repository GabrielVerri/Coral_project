"""
Pacote de AFDs do lexer. Usa o AFD unificado criado a partir da conversão AFN->AFD.
"""

from ..AFN import AFNCoralUnificado
from ..conversores import ConversorAFNparaAFD
from .AFDUnificado import AFDUnificado

__all__ = [
    "AFDUnificado",
    "get_afds"
]

def get_afds():
    """Retorna uma lista com o AFD unificado"""
    # Cria o AFN
    afn = AFNCoralUnificado()
    
    # Cria o conversor
    conversor = ConversorAFNparaAFD(afn)
    
    # Cria o AFD unificado
    afd_unificado = AFDUnificado(conversor)
    
    return [afd_unificado]
