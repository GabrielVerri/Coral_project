from src.lexer import AFDOperadoresBooleanos

print("=== Iniciando testes do AFD de Operadores Booleanos ===")
afd_operadores_booleanos = AFDOperadoresBooleanos()
testes_operadores_booleanos = [
    ("VERDADE", True, "aceito como Operador Booleano"),
    ("FALSO", True, "aceito como Operador Booleano"),
    ("VERDADEIRO", False, "rejeitado (não é operador booleano válido)"),
    ("FAL", False, "rejeitado (não é operador booleano completo)"),
    ("", False, "rejeitado (string vazia)")
]

for entrada, esperado, descricao in testes_operadores_booleanos:
    resultado = afd_operadores_booleanos.aceita(entrada)
    print(f"Teste {'passou' if resultado == esperado else 'falhou'}: '{entrada}' {descricao}, resultado: {resultado}")