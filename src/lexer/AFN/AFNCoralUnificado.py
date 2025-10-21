class Estado:
    """Representa um estado do AFN."""
    
    def __init__(self, id_estado, aceitacao=False, tipo_token=None):
        self.id = id_estado
        self.aceitacao = aceitacao
        self.tipo_token = tipo_token
        self.transicoes = {}
        self.epsilon_transicoes = set()
    
    def adicionar_transicao(self, simbolo, estado_destino):
        if simbolo not in self.transicoes:
            self.transicoes[simbolo] = set()
        self.transicoes[simbolo].add(estado_destino)
    
    def adicionar_epsilon_transicao(self, estado_destino):
        self.epsilon_transicoes.add(estado_destino)

class AFNCoralUnificado:
    """AFN unificado que reconhece todos os tokens da linguagem Coral."""
    
    def __init__(self):
        self.estados = {}
        self.estado_inicial = None
        self.construir_afn()
    
    def criar_estado(self, id_estado, aceitacao=False, tipo_token=None):
        estado = Estado(id_estado, aceitacao, tipo_token)
        self.estados[id_estado] = estado
        return estado
    
    def epsilon_fecho(self, estados_iniciais):
        if isinstance(estados_iniciais, str):
            estados_iniciais = {estados_iniciais}
            
        fecho = set(estados_iniciais)
        pilha = list(estados_iniciais)
        
        while pilha:
            estado_atual = pilha.pop()
            estado = self.estados[estado_atual]
            
            for estado_destino in estado.epsilon_transicoes:
                if estado_destino not in fecho:
                    fecho.add(estado_destino)
                    pilha.append(estado_destino)
                    
        return fecho
    
    def mover(self, estados_atuais, simbolo):
        estados_destino = set()
        
        for estado_id in estados_atuais:
            estado = self.estados[estado_id]
            if simbolo in estado.transicoes:
                estados_destino.update(estado.transicoes[simbolo])
                
        return estados_destino
    
    def construir_afn(self):
        self.estado_inicial = self.criar_estado('q0')
        
        # Comentários
        qC0 = self.criar_estado('qC0')
        qC1 = self.criar_estado('qC1', aceitacao=True, tipo_token='COMENTARIO_LINHA')
        qC2 = self.criar_estado('qC2')
        
        self.estado_inicial.adicionar_epsilon_transicao('qC0')
        qC0.adicionar_transicao('#', 'qC1')
        qC0.adicionar_transicao('outro', 'qC2')
        qC1.adicionar_transicao('outro', 'qC1')
        qC2.adicionar_transicao('outro', 'qC2')
        qC2.adicionar_transicao('#', 'qC2')
        
        # Strings
        qS0 = self.criar_estado('qS0')
        qS1 = self.criar_estado('qS1')
        qS2 = self.criar_estado('qS2', aceitacao=True, tipo_token='STRING')
        qS3 = self.criar_estado('qS3')
        qS4 = self.criar_estado('qS4', aceitacao=True, tipo_token='STRING')
        qS5 = self.criar_estado('qS5')
        qS6 = self.criar_estado('qS6', aceitacao=True, tipo_token='STRING_MULTILINE')
        qS7 = self.criar_estado('qS7')
        qS8 = self.criar_estado('qS8', aceitacao=True, tipo_token='STRING_MULTILINE')
        
        self.estado_inicial.adicionar_epsilon_transicao('qS0')
        qS0.adicionar_transicao('"', 'qS1')
        qS0.adicionar_transicao("'", 'qS3')
        qS1.adicionar_transicao('outro', 'qS1')
        qS1.adicionar_transicao('"', 'qS2')
        qS3.adicionar_transicao('outro', 'qS3')
        qS3.adicionar_transicao("'", 'qS4')
        qS0.adicionar_transicao('"""', 'qS5')
        qS0.adicionar_transicao("'''", 'qS7')
        qS5.adicionar_transicao('qualquer', 'qS5')
        qS5.adicionar_transicao('"""', 'qS6')
        qS7.adicionar_transicao('qualquer', 'qS7')
        qS7.adicionar_transicao("'''", 'qS8')
        
        # Identificadores
        qI0 = self.criar_estado('qI0')
        qI1 = self.criar_estado('qI1', aceitacao=True, tipo_token='IDENTIFICADOR')
        qI2 = self.criar_estado('qI2')
        
        self.estado_inicial.adicionar_epsilon_transicao('qI0')
        qI0.adicionar_transicao('letra', 'qI1')
        qI0.adicionar_transicao('outro', 'qI2')
        qI1.adicionar_transicao('letra_digito', 'qI1')
        qI2.adicionar_transicao('outro', 'qI2')
        
        # Delimitadores
        qSim0 = self.criar_estado('qSim0')
        qSim1 = self.criar_estado('qSim1', aceitacao=True, tipo_token='DELIMITADOR')
        
        self.estado_inicial.adicionar_epsilon_transicao('qSim0')
        qSim0.adicionar_transicao('(', 'qSim1')
        qSim0.adicionar_transicao(')', 'qSim1')
        qSim0.adicionar_transicao('{', 'qSim1')
        qSim0.adicionar_transicao('}', 'qSim1')
        qSim0.adicionar_transicao(',', 'qSim1')
        
        # Operadores
        qOA0 = self.criar_estado('qOA0')
        qOA1 = self.criar_estado('qOA1', aceitacao=True, tipo_token='OPERADOR_ATRIBUICAO')
        qOA2 = self.criar_estado('qOA2', aceitacao=True, tipo_token='OPERADOR_RELACIONAL')
        qOA3 = self.criar_estado('qOA3')
        qOA4 = self.criar_estado('qOA4', aceitacao=True, tipo_token='OPERADOR_RELACIONAL')
        qOA5 = self.criar_estado('qOA5', aceitacao=True, tipo_token='OPERADOR_RELACIONAL')
        qOA6 = self.criar_estado('qOA6', aceitacao=True, tipo_token='OPERADOR_RELACIONAL')
        qOA7 = self.criar_estado('qOA7', aceitacao=True, tipo_token='OPERADOR_RELACIONAL')
        qOA8 = self.criar_estado('qOA8', aceitacao=True, tipo_token='OPERADOR_RELACIONAL')
        qOA9 = self.criar_estado('qOA9', aceitacao=True, tipo_token='OPERADOR_ARITMETICO')
        qOA10 = self.criar_estado('qOA10', aceitacao=True, tipo_token='OPERADOR_ATRIBUICAO')
        qOA11 = self.criar_estado('qOA11', aceitacao=True, tipo_token='OPERADOR_ATRIBUICAO')
        qOA12 = self.criar_estado('qOA12', aceitacao=True, tipo_token='OPERADOR_ARITMETICO')
        qOA13 = self.criar_estado('qOA13', aceitacao=True, tipo_token='OPERADOR_ATRIBUICAO')
        qOA14 = self.criar_estado('qOA14', aceitacao=True, tipo_token='OPERADOR_ATRIBUICAO')
        qOA15 = self.criar_estado('qOA15', aceitacao=True, tipo_token='OPERADOR_ARITMETICO')
        qOA16 = self.criar_estado('qOA16', aceitacao=True, tipo_token='OPERADOR_ATRIBUICAO')
        qOA17 = self.criar_estado('qOA17', aceitacao=True, tipo_token='OPERADOR_ARITMETICO')
        qOA18 = self.criar_estado('qOA18', aceitacao=True, tipo_token='OPERADOR_ATRIBUICAO')
        qOA19 = self.criar_estado('qOA19', aceitacao=True, tipo_token='OPERADOR_ARITMETICO')
        qOA20 = self.criar_estado('qOA20', aceitacao=True, tipo_token='OPERADOR_ATRIBUICAO')
        
        self.estado_inicial.adicionar_epsilon_transicao('qOA0')
        qOA0.adicionar_transicao('=', 'qOA1')
        qOA1.adicionar_transicao('=', 'qOA2')
        qOA0.adicionar_transicao('!', 'qOA3')
        qOA3.adicionar_transicao('=', 'qOA4')
        qOA0.adicionar_transicao('<', 'qOA5')
        qOA5.adicionar_transicao('=', 'qOA6')
        qOA0.adicionar_transicao('>', 'qOA7')
        qOA7.adicionar_transicao('=', 'qOA8')
        qOA0.adicionar_transicao('+', 'qOA9')
        qOA9.adicionar_transicao('+', 'qOA10')
        qOA9.adicionar_transicao('=', 'qOA11')
        qOA0.adicionar_transicao('-', 'qOA12')
        qOA12.adicionar_transicao('-', 'qOA13')
        qOA12.adicionar_transicao('=', 'qOA14')
        qOA0.adicionar_transicao('*', 'qOA15')
        qOA15.adicionar_transicao('=', 'qOA16')
        qOA0.adicionar_transicao('/', 'qOA17')
        qOA17.adicionar_transicao('=', 'qOA18')
        
        qOA0.adicionar_transicao('%', 'qOA19')
        qOA19.adicionar_transicao('=', 'qOA20')
        
        # 6. Operadores Lógicos
        qOL0 = self.criar_estado('qOL0')
        qOL1 = self.criar_estado('qOL1', aceitacao=True, tipo_token='OPERADOR_LOGICO')  # E
        qOL2 = self.criar_estado('qOL2')  # O
        qOL3 = self.criar_estado('qOL3', aceitacao=True, tipo_token='OPERADOR_LOGICO')  # OU
        qOL4 = self.criar_estado('qOL4')  # N
        qOL5 = self.criar_estado('qOL5')  # NA
        qOL6 = self.criar_estado('qOL6', aceitacao=True, tipo_token='OPERADOR_LOGICO')  # NAO
        qOL7 = self.criar_estado('qOL7')  # estado de erro
        
        self.estado_inicial.adicionar_epsilon_transicao('qOL0')
        
        qOL0.adicionar_transicao('E', 'qOL1')
        qOL0.adicionar_transicao('O', 'qOL2')
        qOL0.adicionar_transicao('N', 'qOL4')
        qOL0.adicionar_transicao('outro', 'qOL7')
        
        qOL2.adicionar_transicao('U', 'qOL3')
        qOL2.adicionar_transicao('outro', 'qOL7')
        
        qOL4.adicionar_transicao('A', 'qOL5')
        qOL4.adicionar_transicao('outro', 'qOL7')
        
        qOL5.adicionar_transicao('O', 'qOL6')
        qOL5.adicionar_transicao('outro', 'qOL7')
        
        qOL7.adicionar_transicao('outro', 'qOL7')
        
        # 7. Operadores Booleanos
        qOB0 = self.criar_estado('qOB0')
        qOB1 = self.criar_estado('qOB1')  # V
        qOB2 = self.criar_estado('qOB2')  # VE
        qOB3 = self.criar_estado('qOB3')  # VER
        qOB4 = self.criar_estado('qOB4')  # VERD
        qOB5 = self.criar_estado('qOB5')  # VERDA
        qOB6 = self.criar_estado('qOB6')  # VERDAD
        qOB7 = self.criar_estado('qOB7', aceitacao=True, tipo_token='BOOLEANO')  # VERDADE
        
        qOB8 = self.criar_estado('qOB8')  # F
        qOB9 = self.criar_estado('qOB9')  # FA
        qOB10 = self.criar_estado('qOB10')  # FAL
        qOB11 = self.criar_estado('qOB11')  # FALS
        qOB12 = self.criar_estado('qOB12', aceitacao=True, tipo_token='BOOLEANO')  # FALSO
        
        self.estado_inicial.adicionar_epsilon_transicao('qOB0')
        
        qOB0.adicionar_transicao('V', 'qOB1')
        qOB1.adicionar_transicao('E', 'qOB2')
        qOB2.adicionar_transicao('R', 'qOB3')
        qOB3.adicionar_transicao('D', 'qOB4')
        qOB4.adicionar_transicao('A', 'qOB5')
        qOB5.adicionar_transicao('D', 'qOB6')
        qOB6.adicionar_transicao('E', 'qOB7')
        
        qOB0.adicionar_transicao('F', 'qOB8')
        qOB8.adicionar_transicao('A', 'qOB9')
        qOB9.adicionar_transicao('L', 'qOB10')
        qOB10.adicionar_transicao('S', 'qOB11')
        qOB11.adicionar_transicao('O', 'qOB12')
        
        # 8. Decimais
        qD0 = self.criar_estado('qD0')
        qD1 = self.criar_estado('qD1', aceitacao=True, tipo_token='INTEIRO')
        qD2 = self.criar_estado('qD2')
        qD3 = self.criar_estado('qD3', aceitacao=True, tipo_token='DECIMAL')
        qD4 = self.criar_estado('qD4')  # estado de erro
        
        self.estado_inicial.adicionar_epsilon_transicao('qD0')
        
        qD0.adicionar_transicao('digito', 'qD1')
        qD0.adicionar_transicao('outro', 'qD4')
        
        qD1.adicionar_transicao('digito', 'qD1')
        qD1.adicionar_transicao('.', 'qD2')
        qD1.adicionar_transicao('outro', 'qD4')
        
        qD2.adicionar_transicao('digito', 'qD3')
        qD2.adicionar_transicao('outro', 'qD4')
        
        qD3.adicionar_transicao('digito', 'qD3')
        qD3.adicionar_transicao('outro', 'qD4')
        
        qD4.adicionar_transicao('outro', 'qD4')
    
    def match(self, entrada):
        """Tenta reconhecer um token no início da string de entrada."""
        if not entrada:
            return None
            
        # Conjunto inicial de estados (epsilon-fecho do estado inicial)
        estados_atuais = self.epsilon_fecho(self.estado_inicial.id)
        
        # Para cada caractere da entrada
        for i, char in enumerate(entrada):
            # Move para próximos estados possíveis
            prox_estados = self.mover(estados_atuais, char)
            if not prox_estados:
                # Tenta com 'outro' se nenhuma transição específica existir
                prox_estados = self.mover(estados_atuais, 'outro')
            
            # Calcula epsilon-fecho dos próximos estados
            estados_atuais = self.epsilon_fecho(prox_estados)
            
            if not estados_atuais:
                break
        
        # Verifica se algum estado atual é de aceitação
        for estado_id in estados_atuais:
            estado = self.estados[estado_id]
            if estado.aceitacao:
                return (entrada[:i+1], i+1, estado.tipo_token)
        
        return None