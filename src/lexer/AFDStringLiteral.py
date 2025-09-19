# AFD para String Literal: ("([^"\n])*"|'([^'\n])*'|"""([^"]|("(?!"")))*"""|'''([^']|('(?!'')))*''')
class AFDStringLiteral:
    def __init__(self):
        self.transicoes = {
            'q0': {'"': 'q1', "'": 'q5', 'outro': 'q15'},
            'q1': {'"': 'q2', '\n': 'q15', 'outro': 'q3'},
            'q2': {'"': 'q9', 'outro': 'q15'},
            'q3': {'"': 'q2', '\n': 'q15', 'outro': 'q3'},
            'q5': {"'": 'q6', '\n': 'q15', 'outro': 'q7'},
            'q6': {"'": 'q10', 'outro': 'q15'},
            'q7': {"'": 'q6', '\n': 'q15', 'outro': 'q7'},
            'q9': {'"': 'q11', 'outro': 'q15'},
            'q10': {"'": 'q12', 'outro': 'q15'},
            'q11': {'"': 'q4', 'outro': 'q13'},
            'q12': {"'": 'q8', 'outro': 'q14'},
            'q13': {'"': 'q4', '\n': 'q15', 'outro': 'q13'},
            'q14': {"'": 'q8', '\n': 'q15', 'outro': 'q14'},
            'q4': {'outro': 'q15'},
            'q8': {'outro': 'q15'},
            'q15': {'"': 'q15', "'": 'q15', '\n': 'q15', 'outro': 'q15'}
        }
        self.estados_aceitacao = {'q2', 'q4', 'q6', 'q8'}  # q2: ", q4: """, q6: ', q8: '''
        self.estado_atual = 'q0'

    def transicao(self, caractere):
        classe_entrada = caractere if caractere in {'"', "'", '\n'} else 'outro'
        self.estado_atual = self.transicoes[self.estado_atual].get(classe_entrada, 'q15')

    def aceita(self, entrada):
        self.estado_atual = 'q0'
        for caractere in entrada:
            self.transicao(caractere)
        return self.estado_atual in self.estados_aceitacao