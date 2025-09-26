# AFD para Operadores Aritméticos e Relacionais
class AFDOperadoresAritmeticosRelacionais:
    def match(self, entrada):
        # testa lexemas em ordem de tamanho (maior primeiro para não confundir == com =)
        operadores = [
            # Operadores Relacionais
            ("==", "OPERADOR_RELACIONAL"),
            ("!=", "OPERADOR_RELACIONAL"),
            ("<=", "OPERADOR_RELACIONAL"),
            (">=", "OPERADOR_RELACIONAL"),
            ("<", "OPERADOR_RELACIONAL"),
            (">", "OPERADOR_RELACIONAL"),
            # Operadores de Atribuição Composta
            ("+=", "OPERADOR_ATRIBUICAO"),
            ("-=", "OPERADOR_ATRIBUICAO"),
            ("*=", "OPERADOR_ATRIBUICAO"),
            ("/=", "OPERADOR_ATRIBUICAO"),
            ("%=", "OPERADOR_ATRIBUICAO"),
            ("++", "OPERADOR_ATRIBUICAO"),
            ("--", "OPERADOR_ATRIBUICAO"),
            # Operadores Aritméticos
            ("*", "OPERADOR_ARITMETICO"),
            ("/", "OPERADOR_ARITMETICO"),
            ("%", "OPERADOR_ARITMETICO"),
            ("+", "OPERADOR_ARITMETICO"),
            ("-", "OPERADOR_ARITMETICO"),
            # Atribuição Simples
            ("=", "OPERADOR_ATRIBUICAO"),
        ]

        # Tenta encontrar o maior operador válido no início da entrada
        for op, tipo in operadores:
            if entrada.startswith(op):
                # Se a entrada é exatamente o operador, aceita
                if len(entrada) == len(op):
                    return (op, len(op), tipo)
                # Se tem mais caracteres depois, verifica se não formam outro operador
                prox = entrada[len(op)]
                if prox not in "=<>!+-*/%":
                    return (op, len(op), tipo)
        return None
