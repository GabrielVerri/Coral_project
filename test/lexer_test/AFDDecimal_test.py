from src.lexer import AFDDecimal

print("=== Iniciando testes do AFD de Decimal ===")
afd_decimal = AFDDecimal()
testes_decimal = [
    ("123.456", True, "aceito como Decimal"),
    ("0.0", True, "aceito como Decimal"),
    ("42", True, "aceito como Inteiro"),
    (".5", False, "rejeitado (não começa com dígito)"),
    ("123.", False, "rejeitado (ponto sem parte decimal)"),
    ("abc", False, "rejeitado (não é número)"),
    ("", False, "rejeitado (string vazia)")
]

for entrada, esperado, descricao in testes_decimal:
    resultado = afd_decimal.aceita(entrada)
    print(f"Teste {'passou' if resultado == esperado else 'falhou'}: '{entrada}' {descricao}, resultado: {resultado}")