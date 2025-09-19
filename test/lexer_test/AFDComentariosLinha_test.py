from src.lexer import AFDComentariosLinha

print("=== Iniciando testes do AFD de Comentários em Linha ===")
afd_comentarios = AFDComentariosLinha()
testes_comentarios = [
    ("#teste", True, "aceito como Comentário em Linha"),
    ("#", True, "aceito como Comentário em Linha"),
    ("abc", False, "rejeitado (não começa com #)"),
    ("", False, "rejeitado (string vazia)")
]

for entrada, esperado, descricao in testes_comentarios:
    resultado = afd_comentarios.aceita(entrada)
    print(f"Teste {'passou' if resultado == esperado else 'falhou'}: '{entrada}' {descricao}, resultado: {resultado}")