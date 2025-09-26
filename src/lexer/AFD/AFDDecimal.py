# AFD para números: [0-9]+(\.[0-9]+)?
class AFDDecimal:
    def __init__(self):
        self.transicoes = {
            'q0': {'numero': 'q1', 'outro': 'q4'},    # início -> dígito
            'q1': {'numero': 'q1', '.': 'q2', 'outro': 'q4'},  # sequência de dígitos (inteiro)
            'q2': {'numero': 'q3', 'outro': 'q4'},    # ponto decimal -> precisa dígito
            'q3': {'numero': 'q3', 'outro': 'q4'},    # sequência após ponto (decimal)
            'q4': {'numero': 'q4', '.': 'q4', 'outro': 'q4'}  # estado de rejeição
        }
        self.estados_aceitacao = {'q1', 'q3'}  # q1: inteiro, q3: decimal
        self.estado_atual = 'q0'

    def transicao(self, caractere):
        classe_entrada = 'numero' if caractere.isdigit() else ('.' if caractere == '.' else 'outro')
        self.estado_atual = self.transicoes[self.estado_atual].get(classe_entrada, 'q4')

    def match(self, entrada):
        # percorre a entrada e registra a última posição onde o AFD estava em estado de aceitação
        self.estado_atual = 'q0'
        last_accept_pos = 0
        last_accept_state = None
        i = 0

        for caractere in entrada:
            prev_state = self.estado_atual
            self.transicao(caractere)
            i += 1
            
            # registra posição e estado se chegou em estado de aceitação
            if self.estado_atual in self.estados_aceitacao:
                last_accept_pos = i
                last_accept_state = self.estado_atual

            # se entrou em rejeição e não tem aceitação anterior, falha
            if self.estado_atual == 'q4' and last_accept_pos == 0:
                return None

        # Não aceita se terminou lendo um ponto
        if self.estado_atual == 'q2':
            return None
            
        if last_accept_pos > 0:
            lexema = entrada[:last_accept_pos]
            # decide tipo baseado no estado de aceitação
            tipo = "DECIMAL" if last_accept_state == 'q3' else "INTEIRO"
            return (lexema, last_accept_pos, tipo)

        return None