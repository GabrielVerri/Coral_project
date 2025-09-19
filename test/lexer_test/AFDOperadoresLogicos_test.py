from src.lexer import AFDOperadoresLogicos

print("=== Iniciando testes do AFD de Operadores Lógicos ===")
afd_operadores_logicos = AFDOperadoresLogicos()
testes_operadores_logicos = [
    ("E", True, "aceito como Operador Lógico"),
    ("OU", True, "aceito como Operador Lógico"),
    ("NAO", True, "aceito como Operador Lógico"),
    ("E1", False, "rejeitado (não é operador lógico válido)"),
    ("O", False, "rejeitado (não é operador lógico completo)"),
    ("", False, "rejeitado (string vazia)")
]

for entrada, esperado, descricao in testes_operadores_logicos:
    resultado = afd_operadores_logicos.aceita(entrada)
    print(f"Teste {'passou' if resultado == esperado else 'falhou'}: '{entrada}' {descricao}, resultado: {resultado}")
