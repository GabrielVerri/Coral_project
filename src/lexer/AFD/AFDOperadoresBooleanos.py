# AFD para Operadores Booleanos: \b(VERDADE|FALSO)\b
class AFDOperadoresBooleanos:
    def __init__(self):
        self.estado_atual = 'q0'
        
    def match(self, entrada):
        if not entrada:
            return None
            
        # Tenta reconhecer VERDADE
        if entrada.startswith("VERDADE"):
            # Se for exatamente VERDADE ou qualquer coisa depois
            if len(entrada) == 7:
                return ("VERDADE", 7, "BOOLEANO")
            # Se o próximo caractere não continua uma palavra
            elif not entrada[7].isalpha():
                return ("VERDADE", 7, "BOOLEANO")
            return None
            
        # Tenta reconhecer FALSO
        elif entrada.startswith("FALSO"):
            # Se for exatamente FALSO ou qualquer coisa depois
            if len(entrada) == 5:
                return ("FALSO", 5, "BOOLEANO")
            # Se o próximo caractere não continua uma palavra
            elif not entrada[5].isalpha():
                return ("FALSO", 5, "BOOLEANO")
            return None
            
        return None