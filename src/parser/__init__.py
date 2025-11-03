"""
Parser (Analisador Sintático) para a linguagem Coral.

Este módulo implementa um parser descendente preditivo LL(1) baseado
nos conjuntos FIRST e FOLLOW calculados na gramática formal.

Componentes principais:
- ParserCoral: Analisador sintático principal
- ErroSintatico: Exceção para erros de sintaxe
- ast_nodes: Classes de nós da AST
- FirstFollowSets: Conjuntos FIRST e FOLLOW para decisões de parsing
"""

from .parser import ParserCoral, ErroSintatico
from .ast_nodes import *
from .first_follow import FirstFollowSets

__all__ = ['ParserCoral', 'ErroSintatico', 'FirstFollowSets']
