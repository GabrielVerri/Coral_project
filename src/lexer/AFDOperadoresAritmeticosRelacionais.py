# AFD para Operadores Aritméticos e Relacionais
class AFDOperadoresAritmeticosRelacionais:
    def __init__(self):
        self.transicoes = {
            'q0': {'+': 'q1', '-': 'q2', '*': 'q3', '/': 'q4', '%': 'q5', '=': 'q6', '!': 'q7', '<': 'q8', '>': 'q9', 'outro': 'q15'},
            'q1': {'+': 'q10', '=': 'q11', 'outro': 'q14'},
            'q2': {'-': 'q12', '=': 'q13', 'outro': 'q14'},
            'q3': {'*': 'q16', '=': 'q17', 'outro': 'q14'},
            'q4': {'=': 'q18', 'outro': 'q14'},
            'q5': {'=': 'q19', 'outro': 'q14'},
            'q6': {'=': 'q20', 'outro': 'q14'},
            'q7': {'=': 'q21', 'outro': 'q14'},
            'q8': {'=': 'q22', 'outro': 'q14'},
            'q9': {'=': 'q23', 'outro': 'q14'},
            'q10': {'outro': 'q14'},
            'q11': {'outro': 'q14'},
            'q12': {'outro': 'q14'},
            'q13': {'outro': 'q14'},
            'q14': {'+': 'q15', '-': 'q15', '*': 'q15', '/': 'q15', '%': 'q15', '=': 'q15', '!': 'q15', '<': 'q15', '>': 'q15', 'outro': 'q15'},
            'q16': {'=': 'q24', 'outro': 'q14'},
            'q17': {'outro': 'q14'},
            'q18': {'outro': 'q14'},
            'q19': {'outro': 'q14'},
            'q20': {'outro': 'q14'},
            'q21': {'outro': 'q14'},
            'q22': {'outro': 'q14'},
            'q23': {'outro': 'q14'},
            'q24': {'outro': 'q14'},
            'q15': {'+': 'q15', '-': 'q15', '*': 'q15', '/': 'q15', '%': 'q15', '=': 'q15', '!': 'q15', '<': 'q15', '>': 'q15', 'outro': 'q15'}
        }
        self.estados_aceitacao = {'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 'q11', 'q12', 'q13', 'q16', 'q17', 'q18', 'q19', 'q20', 'q21', 'q22', 'q23', 'q24'}
        self.estado_atual = 'q0'

    def transicao(self, caractere):
        classe_entrada = caractere if caractere in {'+', '-', '*', '/', '%', '=', '!', '<', '>'} else 'outro'
        self.estado_atual = self.transicoes[self.estado_atual].get(classe_entrada, 'q15')

    def aceita(self, entrada):
        self.estado_atual = 'q0'
        for caractere in entrada:
            self.transicao(caractere)
        return self.estado_atual in self.estados_aceitacao