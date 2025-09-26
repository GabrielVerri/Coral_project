# AFD para String Literal: ("([^"\n])*"|'([^'\n])*'|"""([^"]|("(?!"")))*"""|'''([^']|('(?!'')))*''')
class AFDStringLiteral:
    def __init__(self):
        self.estado_atual = 'q0'
        
    def next_char_is_alnum(self, entrada, pos):
        return pos < len(entrada) and entrada[pos].isalnum()
        
    def find_string_end(self, entrada, inicio, delimitador):
        i = inicio
        escaped = False
        
        while i < len(entrada):
            c = entrada[i]
            
            if escaped:
                escaped = False
            elif c == '\\':
                escaped = True
            elif c == '\n':
                return -1  # String não pode conter quebra de linha
            elif c == delimitador:
                # Verifica se o próximo caractere não é alfanumérico
                if not self.next_char_is_alnum(entrada, i + 1):
                    return i
                return -1
                
            i += 1
            
        return -1  # String não foi fechada
        
    def match(self, entrada):
        if not entrada:
            return None
            
        # String começa com aspas duplas
        if entrada.startswith('"'):
            # Tenta encontrar o fim da string
            pos = self.find_string_end(entrada, 1, '"')
            if pos >= 0:
                return (entrada[:pos+1], pos+1, 'STRING')
                
        # String começa com aspas simples
        elif entrada.startswith("'"):
            # Tenta encontrar o fim da string
            pos = self.find_string_end(entrada, 1, "'")
            if pos >= 0:
                return (entrada[:pos+1], pos+1, 'STRING')
                
        return None