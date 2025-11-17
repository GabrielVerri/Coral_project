class AFDStringLiteral:
    def __init__(self):
        self.estado_atual = 'q0'

    def next_char_is_alnum(self, entrada, pos):
        return pos < len(entrada) and entrada[pos].isalnum()

    def find_string_end(self, entrada, inicio, delimitador, multiline=False):
        i = inicio
        escaped = False

        while i < len(entrada):
            c = entrada[i]

            if escaped:
                escaped = False
            elif c == '\\':
                escaped = True
            elif c == '\n' and not multiline:
                return -1  # não pode quebra de linha em string normal
            elif entrada.startswith(delimitador, i):
                return i + len(delimitador) - 1
            i += 1

        return -1  # String não foi fechada

    def match(self, entrada):
        if not entrada:
            return None

        # Verifica se começa com 'f' (f-string)
        prefixo_f = entrada.startswith('f')
        inicio = 1 if prefixo_f else 0
        entrada_sem_prefixo = entrada[inicio:]

        # String tripla com aspas duplas
        if entrada_sem_prefixo.startswith('"""'):
            pos = self.find_string_end(entrada, inicio + 3, '"""', multiline=True)
            if pos >= 0:
                return (entrada[:pos+3], pos+3, 'STRING_MULTILINE')

        # String tripla com aspas simples
        elif entrada_sem_prefixo.startswith("'''"):
            pos = self.find_string_end(entrada, inicio + 3, "'''", multiline=True)
            if pos >= 0:
                return (entrada[:pos+3], pos+3, 'STRING_MULTILINE')

        # String normal com aspas duplas
        elif entrada_sem_prefixo.startswith('"'):
            pos = self.find_string_end(entrada, inicio + 1, '"', multiline=False)
            if pos >= 0:
                return (entrada[:pos+1], pos+1, 'STRING')

        # String normal com aspas simples
        elif entrada_sem_prefixo.startswith("'"):
            pos = self.find_string_end(entrada, inicio + 1, "'", multiline=False)
            if pos >= 0:
                return (entrada[:pos+1], pos+1, 'STRING')

        return None
