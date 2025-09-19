# AFD para Operadores Lógicos: \b(E|OU|NAO)\b
class AFDOperadoresLogicos:
    def __init__(self):
        self.transicoes = {
            'q0': {'E': 'q1', 'O': 'q2', 'N': 'q3', 'outro': 'q10'},
            'q1': {'outro': 'q4'},
            'q2': {'U': 'q5', 'outro': 'q10'},
            'q3': {'A': 'q6', 'outro': 'q10'},
            'q4': {'E': 'q10', 'O': 'q10', 'N': 'q10', 'U': 'q10', 'A': 'q10', 'outro': 'q10'},
            'q5': {'outro': 'q7'},
            'q6': {'O': 'q8', 'outro': 'q10'},
            'q7': {'E': 'q10', 'O': 'q10', 'N': 'q10', 'U': 'q10', 'A': 'q10', 'outro': 'q10'},
            'q8': {'outro': 'q9'},
            'q9': {'E': 'q10', 'O': 'q10', 'N': 'q10', 'U': 'q10', 'A': 'q10', 'outro': 'q10'},
            'q10': {'E': 'q10', 'O': 'q10', 'N': 'q10', 'U': 'q10', 'A': 'q10', 'outro': 'q10'}
        }
        self.estados_aceitacao = {'q4', 'q7', 'q9'}
        self.estado_atual = 'q0'

    def transicao(self, caractere):
        classe_entrada = caractere if caractere in {'E', 'O', 'N', 'U', 'A'} else 'outro'
        self.estado_atual = self.transicoes[self.estado_atual].get(classe_entrada, 'q10')

    def aceita(self, entrada):
        self.estado_atual = 'q0'
        for caractere in entrada:
            self.transicao(caractere)
        return self.estado_atual in self.estados_aceitacao