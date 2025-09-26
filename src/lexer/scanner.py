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
            'SE', 'ENTAO', 'SENAO', 'FIM', 'ESCREVA', 'VERDADE', 'FALSO',
            'INTEIRO', 'DECIMAL', 'TEXTO', 'BOOLEANO', 'E', 'OU', 'NAO'
        }

        # obter lista de AFDs na ordem de prioridade
        self.afds = get_afds()

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
                    # se for identificador, checa se é palavra reservada
                    if tipo == "IDENTIFICADOR":
                        # verifica se é palavra reservada
                        if lexema in self.palavras_reservadas:
                            tipo = "PALAVRA_RESERVADA"
                        # verifica se é um comando (seguido por parênteses)
                        elif self.pos + tamanho < len(self.source) and self.source[self.pos + tamanho].strip() == '(':
                            # se for um comando mas não for palavra reservada, é erro
                            raise ValueError(
                                f"Token inválido na linha {self.linha}, coluna {self.coluna}: '{lexema}'"
                            )
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
            if self.source[self.pos] == "\n":
                self.linha += 1
                self.coluna = 1
            else:
                self.coluna += 1
            self.pos += 1
