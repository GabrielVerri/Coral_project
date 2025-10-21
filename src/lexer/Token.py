class Token:
    """Representa um token reconhecido pelo analisador léxico."""
    
    def __init__(self, lexema, tipo, linha, coluna, posicao):
        self.lexema = lexema
        self.tipo = tipo
        self.linha = linha
        self.coluna = coluna
        self.posicao = posicao
    
    def __repr__(self):
        return f"Token({self.lexema!r}, {self.tipo}, L{self.linha}:C{self.coluna})"
    
    def __str__(self):
        return f"{self.lexema} ({self.tipo})"
