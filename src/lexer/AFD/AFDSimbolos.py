class AFDSimbolos:
    """Reconhece símbolos de pontuação simples: () {} ; ,"""
    def __init__(self):
        # lista de símbolos reconhecidos
        self.simbolos = {'(', ')', '{', '}', ','}

    def match(self, entrada):
        if not entrada:
            return None
        c = entrada[0]
        if c in self.simbolos:
            return (c, 1, "SIMBOLO")
        return None
