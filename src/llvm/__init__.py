"""
Módulo de compilação LLVM IR para Coral.

Este módulo converte a AST de Coral para código LLVM IR,
permitindo compilação nativa de programas Coral.
"""

from .llvm_compiler import LLVMCompiler

__all__ = ['LLVMCompiler']
