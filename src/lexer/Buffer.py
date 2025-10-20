class BufferLeitura:
    """Gerencia leitura do código fonte com controle de posição."""
    
    def __init__(self, codigo_fonte):
        self.codigo_fonte = codigo_fonte
        self.posicao = 0
        self.linha = 1
        self.coluna = 1
        self.tamanho = len(codigo_fonte)
    
    def caractere_atual(self):
        """Retorna o caractere na posição atual."""
        if self.posicao < self.tamanho:
            return self.codigo_fonte[self.posicao]
        return None
    
    def resto_codigo(self):
        """Retorna o restante do código a partir da posição atual."""
        return self.codigo_fonte[self.posicao:]
    
    def fim_arquivo(self):
        """Verifica se chegou ao fim do arquivo."""
        return self.posicao >= self.tamanho
    
    def get_posicao_info(self):
        """Retorna informações da posição atual."""
        return {
            'posicao': self.posicao,
            'linha': self.linha,
            'coluna': self.coluna
        }
    
    def avancar(self, quantidade=1):
        """Avança o buffer atualizando linha e coluna."""
        for _ in range(quantidade):
            if self.posicao < self.tamanho:
                if self.codigo_fonte[self.posicao] == '\n':
                    self.linha += 1
                    self.coluna = 1
                else:
                    self.coluna += 1
                self.posicao += 1


class BufferTokens:
    """Armazena tokens reconhecidos durante a análise léxica."""
    
    def __init__(self):
        self.tokens = []
    
    def adicionar(self, token):
        """Adiciona um token ao buffer."""
        self.tokens.append(token)
    
    def obter_todos(self):
        """Retorna lista de todos os tokens."""
        return self.tokens
    
    def obter_tuplas(self):
        """Retorna lista de tuplas (lexema, tipo) para compatibilidade."""
        return [token.to_tuple() for token in self.tokens]
    
    def limpar(self):
        """Limpa o buffer de tokens."""
        self.tokens = []
    
    def __len__(self):
        return len(self.tokens)
    
    def __iter__(self):
        return iter(self.tokens)
    
    def __getitem__(self, index):
        return self.tokens[index]
