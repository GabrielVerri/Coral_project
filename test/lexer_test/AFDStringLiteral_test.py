from src.lexer import AFDStringLiteral

print("=== Iniciando testes do AFD de String Literal ===")
afd_strings = AFDStringLiteral()
testes_strings = [
    ('"teste"', True, "aceito como String Literal (aspas duplas)"),
    ("'teste'", True, "aceito como String Literal (aspas simples)"),
    ('"""teste"""', True, "aceito como String Literal (aspas triplas duplas)"),
    ("'''teste'''", True, "aceito como String Literal (aspas triplas simples)"),
    ('"incompleto', False, "rejeitado (aspas duplas não fechadas)"),
    ("'incompleto", False, "rejeitado (aspas simples não fechadas)"),
    ('"""incompleto"', False, "rejeitado (aspas triplas duplas não fechadas)"),
    ("''incompleto'", False, "rejeitado (aspas triplas simples não fechadas)"),
    ("", False, "rejeitado (string vazia)")
]

for entrada, esperado, descricao in testes_strings:
    resultado = afd_strings.aceita(entrada)
    print(f"Teste {'passou' if resultado == esperado else 'falhou'}: '{entrada}' {descricao}, resultado: {resultado}")
