class AFDDelimitadores:
    """Reconhece símbolos de pontuação simples: () {} ; ,"""
    def __init__(self):
        # lista de símbolos reconhecidos
        self.delimitadores = {'(', ')', '{', '}', ','}

    def match(self, entrada):
        if not entrada:
            return None
        c = entrada[0]
        if c in self.delimitadores:
            return (c, 1, "DELIMITADOR")
        return None
