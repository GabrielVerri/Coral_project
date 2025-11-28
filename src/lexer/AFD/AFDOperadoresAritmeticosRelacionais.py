# AFD para Operadores Aritméticos e Relacionais
class AFDOperadoresAritmeticosRelacionais:
    def match(self, entrada):
        # testa lexemas em ordem de tamanho (maior primeiro para não confundir == com =)
        operadores = [
            # Operadores Relacionais (2 caracteres primeiro)
            ("==", "OPERADOR_RELACIONAL"),
            ("!=", "OPERADOR_RELACIONAL"),
            ("<=", "OPERADOR_RELACIONAL"),
            (">=", "OPERADOR_RELACIONAL"),
            # Operador de Exponenciação (2 caracteres)
            ("**", "OPERADOR_ARITMETICO"),
            # Operadores de Atribuição Composta (2 caracteres)
            ("+=", "OPERADOR_ATRIBUICAO"),
            ("-=", "OPERADOR_ATRIBUICAO"),
            ("*=", "OPERADOR_ATRIBUICAO"),
            ("/=", "OPERADOR_ATRIBUICAO"),
            ("%=", "OPERADOR_ATRIBUICAO"),
            ("++", "OPERADOR_ATRIBUICAO"),
            ("--", "OPERADOR_ATRIBUICAO"),
            # Operadores Relacionais (1 caractere)
            ("<", "OPERADOR_RELACIONAL"),
            (">", "OPERADOR_RELACIONAL"),
            # Operadores Aritméticos (1 caractere)
            ("*", "OPERADOR_ARITMETICO"),
            ("/", "OPERADOR_ARITMETICO"),
            ("%", "OPERADOR_ARITMETICO"),
            ("+", "OPERADOR_ARITMETICO"),
            ("-", "OPERADOR_ARITMETICO"),
            # Atribuição Simples (1 caractere)
            ("=", "OPERADOR_ATRIBUICAO"),
        ]

        # Tenta encontrar o maior operador válido no início da entrada
        for op, tipo in operadores:
            if entrada.startswith(op):
                return (op, len(op), tipo)
        return None
