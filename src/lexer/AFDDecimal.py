# AFD para Decimal: [0-9]+(\.[0-9]+)?
class AFDDecimal:
    def __init__(self):
        self.transicoes = {
            'q0': {'numero': 'q1', 'outro': 'q4'},
            'q1': {'numero': 'q1', '.': 'q2', 'outro': 'q4'},
            'q2': {'numero': 'q3', 'outro': 'q4'},
            'q3': {'numero': 'q3', 'outro': 'q4'},
            'q4': {'numero': 'q4', '.': 'q4', 'outro': 'q4'}
        }
        self.estados_aceitacao = {'q1', 'q3'}  # q1 para inteiros, q3 para decimais
        self.estado_atual = 'q0'

    def transicao(self, caractere):
        classe_entrada = 'numero' if caractere.isdigit() else ('.' if caractere == '.' else 'outro')
        self.estado_atual = self.transicoes[self.estado_atual].get(classe_entrada, 'q4')

    def aceita(self, entrada):
        self.estado_atual = 'q0'
        for caractere in entrada:
            self.transicao(caractere)
        return self.estado_atual in self.estados_aceitacao