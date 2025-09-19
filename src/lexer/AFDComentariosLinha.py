# AFD para Comentários em Linha: \#.*
class AFDComentariosLinha:
    def __init__(self):
        self.transicoes = {
            'q0': {'#': 'q1', 'outro': 'q2'},
            'q1': {'outro': 'q1'},
            'q2': {'outro': 'q2', '#': 'q2'}
        }
        self.estados_aceitacao = {'q1'}
        self.estado_atual = 'q0'

    def transicao(self, caractere):
        classe_entrada = caractere if caractere == '#' else 'outro'
        self.estado_atual = self.transicoes[self.estado_atual].get(classe_entrada, 'q2')

    def aceita(self, entrada):
        self.estado_atual = 'q0'
        for caractere in entrada:
            self.transicao(caractere)
        return self.estado_atual in self.estados_aceitacao
