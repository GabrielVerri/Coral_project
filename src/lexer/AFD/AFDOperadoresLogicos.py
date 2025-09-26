# AFD para Operadores Lógicos: \b(E|OU|NAO)\b
class AFDOperadoresLogicos:
    def __init__(self):
        self.transicoes = {
            'q0': {'E': 'q1', 'O': 'q2', 'N': 'q4', 'outro': 'q7'},
            'q1': {'outro': 'q7'},  # E aceito
            'q2': {'U': 'q3', 'outro': 'q7'},
            'q3': {'outro': 'q7'},  # OU aceito
            'q4': {'A': 'q5', 'outro': 'q7'},
            'q5': {'O': 'q6', 'outro': 'q7'},
            'q6': {'outro': 'q7'},  # NAO aceito
            'q7': {'outro': 'q7'}  # Estado de erro
        }
        self.estados_aceitacao = {'q1', 'q3', 'q6'}  # E, OU e NAO
        self.estado_atual = 'q0'
        
    def eh_parte_identificador(self, c):
        """Retorna True se c pode fazer parte de um identificador."""
        return c.isalnum() or c == '_'
        
    def match(self, entrada):
        """Tenta reconhecer um operador lógico no início da string de entrada.
        
        Reconhece os operadores E, OU e NAO que estejam entre fronteiras de palavra (\b).
        Uma fronteira de palavra ocorre em:
        - Início/fim da string
        - Entre letra e não-letra
        - Entre caractere de identificador e não-identificador"""
        if not entrada:
            return None
            
        self.estado_atual = 'q0'
        palavra = ""
        i = 0
        
        # Processa caractere por caractere usando o AFD
        while i < len(entrada):
            c = entrada[i]
            
            # Processa transição
            if c in self.transicoes[self.estado_atual]:
                self.estado_atual = self.transicoes[self.estado_atual][c]
            else:
                self.estado_atual = self.transicoes[self.estado_atual]['outro']
            palavra += c
            i += 1
            
            # Verifica estados de aceitação
            if (self.estado_atual == 'q1' and len(palavra) == 1) or \
               (self.estado_atual == 'q3' and len(palavra) == 2) or \
               (self.estado_atual == 'q6' and len(palavra) == 3):
                # Se estivermos no fim da entrada, aceita
                if i >= len(entrada):
                    return (palavra, i, "OPERADOR_LOGICO")
                # Se o próximo caractere NÃO pode fazer parte de identificador, aceita
                if not self.eh_parte_identificador(entrada[i]):
                    return (palavra, i, "OPERADOR_LOGICO")
                # Se pode fazer parte de identificador, rejeita (pode ser VERDADE, E1, etc)
                return None
                
        return None