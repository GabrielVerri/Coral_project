from src.lexer import AFDIdentificadores

print("=== Iniciando testes do AFD de Identificadores ===")
afd_identificadores = AFDIdentificadores()
testes_identificadores = [
    ("variavel", True, "aceito como Identificador"),
    ("x_123", True, "aceito como Identificador"),
    ("123abc", False, "rejeitado (não começa com letra ou _)"),
    ("", False, "rejeitado (string vazia)")
]

for entrada, esperado, descricao in testes_identificadores:
    resultado = afd_identificadores.aceita(entrada)
    print(f"Teste {'passou' if resultado == esperado else 'falhou'}: '{entrada}' {descricao}, resultado: {resultado}")