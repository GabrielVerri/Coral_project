"""
Pacote AFN (Autômatos Finitos Não-Determinísticos) para análise léxica.
"""

from .AFNCoralUnificado import AFNCoralUnificado
from .AFNTransicoes import AFNTransicoes

__all__ = [
    "AFNCoralUnificado",
    "AFNTransicoes"
]