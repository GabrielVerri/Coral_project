import sys
import os

# Adiciona o diretório src ao path do Python para imports
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, src_dir)

from lexer.AFN import AFNTransicoes, AFNCoralUnificado

class ConversorAFNparaAFD:
    """Converte AFN em AFD usando algoritmo de construção de subconjuntos."""
    
    def __init__(self, afn):
        self.afn = afn
        self.afn_transicoes = AFNTransicoes(afn.estados, afn.estado_inicial)
        self.afd_estados = {}
        self.afd_transicoes = {}
        self.afd_estados_aceitacao = {}
    
    def _novo_nome_estado(self, conjunto_estados):
        return 'S' + '_'.join(sorted(conjunto_estados))
    
    def _eh_estado_aceitacao(self, conjunto_estados):
        estados_aceitacao = self.afn_transicoes.get_estados_aceitacao()
        for estado in conjunto_estados:
            if estado in estados_aceitacao:
                return estados_aceitacao[estado]
        return None
    
    def construir_subconjuntos(self):
        estado_inicial = 'Sq0'
        estados_nao_processados = [estado_inicial]
        
        self.afd_estados[estado_inicial] = frozenset(self.afn.epsilon_fecho(self.afn.estado_inicial.id))
        
        tipo_token = self._eh_estado_aceitacao(self.afd_estados[estado_inicial])
        if tipo_token:
            self.afd_estados_aceitacao[estado_inicial] = tipo_token
        while estados_nao_processados:
            estado_atual = estados_nao_processados.pop()
            estados_afn = self.afd_estados[estado_atual]
            
            # Para cada símbolo possível
            for simbolo in self.afn_transicoes.get_simbolos():
                # Conjunto de estados alcançáveis
                estados_destino = set()
                
                # Para cada estado AFN no estado atual do AFD
                for estado in estados_afn:
                    # Adiciona estados alcançáveis com o símbolo atual
                    novos_estados = self.afn.mover({estado}, simbolo)
                    for novo_estado in novos_estados:
                        # Adiciona o ε-fecho de cada novo estado
                        estados_destino.update(self.afn.epsilon_fecho(novo_estado))
                
                if estados_destino:
                    # Cria novo nome para o estado de destino
                    estado_destino = self._novo_nome_estado(estados_destino)
                    
                    # Adiciona transição
                    if estado_atual not in self.afd_transicoes:
                        self.afd_transicoes[estado_atual] = {}
                    self.afd_transicoes[estado_atual][simbolo] = estado_destino
                    
                    # Se é um novo estado, adiciona à lista de não processados
                    if estado_destino not in self.afd_estados:
                        self.afd_estados[estado_destino] = frozenset(estados_destino)
                        estados_nao_processados.append(estado_destino)
                        
                        # Verifica se é estado de aceitação
                        tipo_token = self._eh_estado_aceitacao(estados_destino)
                        if tipo_token:
                            self.afd_estados_aceitacao[estado_destino] = tipo_token
    
    def get_tabela_transicoes_afd(self):
        """Retorna a tabela de transições do AFD resultante."""
        return self.afd_transicoes
    
    def get_estados_aceitacao_afd(self):
        """Retorna os estados de aceitação do AFD resultante."""
        return self.afd_estados_aceitacao

if __name__ == "__main__":
    afn = AFNCoralUnificado()
    
    conversor = ConversorAFNparaAFD(afn)
    conversor.construir_subconjuntos()