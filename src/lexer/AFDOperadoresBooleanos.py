# AFD para Operadores Booleanos: \b(VERDADE|FALSO)\b
class AFDOperadoresBooleanos:
    def __init__(self):
        self.transicoes = {
            'q0': {'V': 'q1', 'F': 'q6', 'outro': 'q12'},
            'q1': {'E': 'q2', 'outro': 'q12'},
            'q2': {'R': 'q3', 'outro': 'q12'},
            'q3': {'D': 'q4', 'outro': 'q12'},
            'q4': {'A': 'q5', 'outro': 'q12'},
            'q5': {'outro': 'q11'},
            'q6': {'A': 'q7', 'outro': 'q12'},
            'q7': {'L': 'q8', 'outro': 'q12'},
            'q8': {'S': 'q9', 'outro': 'q12'},
            'q9': {'O': 'q10', 'outro': 'q12'},
            'q10': {'outro': 'q11'},
            'q11': {'V': 'q12', 'F': 'q12', 'outro': 'q12'},
            'q12': {'V': 'q12', 'F': 'q12', 'outro': 'q12'}
        }
        self.estados_aceitacao = {'q5', 'q10'}
        self.estado_atual = 'q0'

    def transicao(self, caractere):
        classe_entrada = caractere if caractere in {'V', 'E', 'R', 'D', 'A', 'F', 'L', 'S', 'O'} else 'outro'
        self.estado_atual = self.transicoes[self.estado_atual].get(classe_entrada, 'q12')

    def aceita(self, entrada):
        self.estado_atual = 'q0'
        for caractere in entrada:
            self.transicao(caractere)
        return self.estado_atual in self.estados_aceitacao