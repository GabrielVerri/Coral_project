# Scanner.py - COM PEQUENA CORREÇÃO
try:
    from .AFD import get_afds
except ImportError:
    from AFD import get_afds

class Scanner:
    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.linha = 1
        self.coluna = 1
        # palavras reservadas da linguagem
        self.palavras_reservadas = {
            'SE', 'SENAO', 'SENAOSE', 'ENQUANTO', 'PARA', 'DENTRODE',
            'E', 'OU', 'NAO', 'VERDADE', 'FALSO',
            'INTEIRO', 'DECIMAL', 'TEXTO', 'BOOLEANO',
            'DEF', 'CLASSE', 'RETORNAR',
            'QUEBRA', 'CONTINUA', 'PASSAR',
            'GLOBAL', 'NAOLOCAL', 'IMPORTAR', 'DE', 'COMO',
            'TENTE', 'EXCETO', 'FINALMENTE', 'LANCAR', 'AFIRMA',
            'ESPERA', 'VAZIO', 'EIGUAL', 'LAMBDA', 'COM', 'DELETAR',
            'ASSINCRONO', 'ENVIAR'
        }
        # obter lista de AFDs na ordem de prioridade
        self.afds = get_afds()

    def _eh_alfanumerico_ou_underscore(self, char):
        """Verifica se o caractere é alfanumérico ou underscore"""
        return char.isalnum() or char == '_'
    
    def tokenize(self):
        tokens = []
        while self.pos < len(self.source):
            char = self.source[self.pos]
            # ignora espaços e quebras de linha
            if char.isspace():
                self._avancar(1)
                continue
            
            # tenta reconhecer com cada AFD
            resultado = None
            for afd in self.afds:
                resultado = afd.match(self.source[self.pos:])
                if resultado:
                    lexema, tamanho, tipo = resultado
                    
                    # NOVA VERIFICAÇÃO: Se é número seguido de letra/underscore = erro
                    if tipo in ("INTEIRO", "DECIMAL"):
                        proxima_pos = self.pos + tamanho
                        if proxima_pos < len(self.source):
                            proximo_char = self.source[proxima_pos]
                            if self._eh_alfanumerico_ou_underscore(proximo_char):
                                # Número grudado com letra = token inválido
                                # Encontra onde termina essa sequência inválida
                                fim_seq = proxima_pos
                                while (fim_seq < len(self.source) and 
                                       self._eh_alfanumerico_ou_underscore(self.source[fim_seq])):
                                    fim_seq += 1
                                sequencia_invalida = self.source[self.pos:fim_seq]
                                raise ValueError(
                                    f"Token inválido na linha {self.linha}, coluna {self.coluna}: "
                                    f"'{sequencia_invalida}' - números não podem ser seguidos por letras"
                                )
                    
                    # se for identificador, checa se é palavra reservada
                    if tipo == "IDENTIFICADOR":
                        # verifica se é palavra reservada
                        if lexema in self.palavras_reservadas:
                            tipo = "PALAVRA_RESERVADA"
                    
                    # comentários são ignorados (não entram na tabela)
                    if tipo not in ("COMENTARIO_LINHA", "COMENTARIO_BLOCO"):
                        tokens.append((lexema, tipo))
                    self._avancar(tamanho)
                    break
            
            # se nenhum AFD reconheceu, erro
            if not resultado:
                raise ValueError(
                    f"Token inválido na linha {self.linha}, coluna {self.coluna}: '{char}'"
                )
        return tokens
    
    def _avancar(self, n):
        for _ in range(n):
            if self.pos < len(self.source):
                if self.source[self.pos] == "\n":
                    self.linha += 1
                    self.coluna = 1
                else:
                    self.coluna += 1
                self.pos += 1