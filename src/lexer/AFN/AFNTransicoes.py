class AFNTransicoes:
    """Gerencia transições do AFN para conversão em AFD."""
    
    def __init__(self, estados, estado_inicial):
        self.estados = estados
        self.estado_inicial = estado_inicial
        self.tabela_transicoes = {}
        self._construir_tabela_transicoes()
    
    def _construir_tabela_transicoes(self):
        """Constrói a tabela de transições do AFN."""
        for estado_id, estado in self.estados.items():
            self.tabela_transicoes[estado_id] = {}
            
            # Adiciona transições normais
            for simbolo, estados_destino in estado.transicoes.items():
                self.tabela_transicoes[estado_id][simbolo] = estados_destino
            
            # Adiciona epsilon transições
            if estado.epsilon_transicoes:
                self.tabela_transicoes[estado_id]['ε'] = estado.epsilon_transicoes
    
    def get_transicoes(self, estado_id, simbolo=None):
        """Retorna as transições possíveis para um estado e símbolo."""
        if estado_id not in self.tabela_transicoes:
            return set()
            
        if simbolo is None:
            return self.tabela_transicoes[estado_id]
            
        return self.tabela_transicoes[estado_id].get(simbolo, set())
    
    def get_simbolos(self):
        """Retorna o conjunto de todos os símbolos do alfabeto (exceto ε)."""
        simbolos = set()
        for transicoes in self.tabela_transicoes.values():
            simbolos.update(transicoes.keys())
        simbolos.discard('ε')
        return simbolos
    
    def get_epsilon_transicoes(self, estado_id):
        """Retorna as epsilon transições de um estado."""
        return self.get_transicoes(estado_id, 'ε')
    
    def get_estados_aceitacao(self):
        """Retorna o conjunto de estados de aceitação e seus tipos de token."""
        estados_aceitacao = {}
        for estado_id, estado in self.estados.items():
            if estado.aceitacao:
                estados_aceitacao[estado_id] = estado.tipo_token
        return estados_aceitacao