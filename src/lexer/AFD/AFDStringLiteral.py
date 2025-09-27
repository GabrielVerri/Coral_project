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

        # String tripla com aspas duplas
        if entrada.startswith('"""'):
            pos = self.find_string_end(entrada, 3, '"""', multiline=True)
            if pos >= 0:
                return (entrada[:pos+3], pos+3, 'STRING_MULTILINE')

        # String tripla com aspas simples
        elif entrada.startswith("'''"):
            pos = self.find_string_end(entrada, 3, "'''", multiline=True)
            if pos >= 0:
                return (entrada[:pos+3], pos+3, 'STRING_MULTILINE')

        # String normal com aspas duplas
        elif entrada.startswith('"'):
            pos = self.find_string_end(entrada, 1, '"', multiline=False)
            if pos >= 0:
                return (entrada[:pos+1], pos+1, 'STRING')

        # String normal com aspas simples
        elif entrada.startswith("'"):
            pos = self.find_string_end(entrada, 1, "'", multiline=False)
            if pos >= 0:
                return (entrada[:pos+1], pos+1, 'STRING')

        return None
