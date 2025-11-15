from src.lexer.AFD import get_afd

afd = get_afd()
texto = '"""Ola Mundo"""'
result = afd.match(texto)
print(f"Entrada: {repr(texto)}")
print(f"Resultado: {result}")
