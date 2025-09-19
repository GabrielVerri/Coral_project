# AFD para Identificadores: [a-zA-Z_][a-zA-Z0-9_]*
class AFDIdentificadores:
    def __init__(self):
        self.transicoes = {
            'q0': {'letra': 'q1', 'numero': 'q2', 'outro': 'q2'},
            'q1': {'letra': 'q1', 'numero': 'q1', 'outro': 'q2'},
            'q2': {'letra': 'q2', 'numero': 'q2', 'outro': 'q2'}
        }
        self.estados_aceitacao = {'q1'}
        self.estado_atual = 'q0'

    def transicao(self, caractere):
        classe_entrada = self.obter_classe_entrada(caractere)
        self.estado_atual = self.transicoes[self.estado_atual].get(classe_entrada, 'q2')

    def obter_classe_entrada(self, caractere):
        if caractere.isalpha() or caractere == '_':
            return 'letra'
        elif caractere.isdigit():
            return 'numero'
        else:
            return 'outro'

    def aceita(self, entrada):
        self.estado_atual = 'q0'
        for caractere in entrada:
            self.transicao(caractere)
        return self.estado_atual in self.estados_aceitacao