class AFDIdentificadores:
    def __init__(self):
        self.estados_aceitacao = {'q1'}
    
    def match(self, entrada):
        # Verifica se entrada não está vazia
        if not entrada:
            return None
        
        # CORREÇÃO: Verifica o primeiro caractere ANTES de processar
        primeiro_char = entrada[0]
        if not (primeiro_char.isalpha() or primeiro_char == '_'):
            return None  # Rejeita imediatamente se não começar com letra/underscore
        
        # Resto do código original (sem alterações)
        estado = 'q0'
        lexema = ""
        i = 0
        
        for caractere in entrada:
            if estado == 'q0':
                if caractere.isalpha() or caractere == '_':
                    estado = 'q1'
                    lexema += caractere
                    i += 1
                else:
                    return None
            elif estado == 'q1':
                if caractere.isalnum() or caractere == '_':
                    lexema += caractere
                    i += 1
                else:
                    break
        
        # Se terminou em estado de aceitação
        if estado in self.estados_aceitacao:
            return lexema, i, "IDENTIFICADOR"
        return None