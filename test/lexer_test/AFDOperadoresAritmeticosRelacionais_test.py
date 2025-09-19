from src.lexer import AFDOperadoresAritmeticosRelacionais

print("=== Iniciando testes do AFD de Operadores Aritméticos e Relacionais ===")
afd_operadores_aritmeticos = AFDOperadoresAritmeticosRelacionais()
testes_operadores_aritmeticos = [
    ("+", True, "aceito como Operador Aritmético"),
    ("**", True, "aceito como Operador Aritmético"),
    ("==", True, "aceito como Operador Relacional"),
    ("+=", True, "aceito como Operador Aritmético"),
    ("abc", False, "rejeitado (não é operador válido)"),
    ("", False, "rejeitado (string vazia)")
]

for entrada, esperado, descricao in testes_operadores_aritmeticos:
    resultado = afd_operadores_aritmeticos.aceita(entrada)
    print(f"Teste {'passou' if resultado == esperado else 'falhou'}: '{entrada}' {descricao}, resultado: {resultado}")