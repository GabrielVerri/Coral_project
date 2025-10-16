"""
Lexer para a linguagem Coral - Analisador Léxico completo.
Implementa tokenização utilizando AFDs para reconhecimento de padrões.
"""

import sys
import os

# Adiciona o diretório src ao path do Python para imports
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, src_dir)

# Importa os AFDs necessários
from lexer.AFD import get_afds

class AnalisadorLexico:
    """Analisador léxico/Tokenizador para a linguagem Coral."""
    
    def __init__(self, codigo_fonte):
        """
        Inicializa o analisador léxico com o código fonte.
        
        Args:
            codigo_fonte (str): Código fonte em Coral para tokenizar
        """
        self.codigo_fonte = codigo_fonte  # O código que será analisado
        
        self.posicao = 0    # Índice atual no código fonte (qual caractere estamos lendo)
        self.linha = 1      # Linha atual (para reportar erros com precisão)
        self.coluna = 1     # Coluna atual (para reportar erros com precisão)
        
        # DICIONÁRIO DE PALAVRAS RESERVADAS DA LINGUAGEM CORAL
        self.palavras_reservadas = {
            'SE', 'SENAO', 'SENAOSE', 'ENQUANTO', 'PARA', 'DENTRODE',
            'E', 'OU', 'NAO', 'VERDADE', 'FALSO',
            'INTEIRO', 'DECIMAL', 'TEXTO', 'BOOLEANO',
            'DEF', 'CLASSE', 'RETORNAR',
            'QUEBRA', 'CONTINUA', 'PASSAR',
            'GLOBAL', 'NAOLOCAL', 'IMPORTAR', 'DE', 'COMO',
            'TENTE', 'EXCETO', 'FINALMENTE', 'LANCAR', 'AFIRMA',
            'ESPERA', 'VAZIO', 'EIGUAL', 'LAMBDA', 'COM', 'DELETAR',
            'ASSINCRONO', 'ENVIAR'
        }

        self.afds = get_afds()  # Obtém a lista de AFDs que farão o reconhecimento de padrões


    
    def tokenizar(self):
        """
        Realiza a tokenização do código fonte.
        
        Returns:
            list: Lista de tuplas (lexema, tipo_token)
            
        Raises:
            ValueError: Quando encontra token inválido
        """
        tokens = []
        
        # LOOP PRINCIPAL: Percorre todo o código fonte caractere por caractere
        while self.posicao < len(self.codigo_fonte):
            caractere = self.codigo_fonte[self.posicao]  # Caractere atual
            
            # Pula espaços, tabs, quebras de linha
            if caractere.isspace():
                self._avancar(1)  # Move ponteiro e atualiza linha/coluna
                continue          # Volta para o início do loop
            
            # TENTATIVA DE MATCH COM O AFD UNIFICADO
            # Como temos apenas 1 AFD unificado, não precisamos de loop
            afd_unificado = self.afds[0]  # Acessa diretamente o único AFD
            
            # TENTATIVA DE MATCH: 
            # - Passa o resto do código (da posição atual até o fim)
            # - Retorna None se não reconhecer, ou (lexema, tamanho, tipo) se reconhecer
            resultado = afd_unificado.match(self.codigo_fonte[self.posicao:])
            
            if resultado:  # AFD reconheceu um token
                    lexema, tamanho, tipo = resultado
                    # lexema: o texto do token
                    # tamanho: quantos caracteres o token ocupa 
                    # tipo: categoria do token (ex: "PALAVRA_RESERVADA", "INTEIRO")
                    
                    # Validação removida - AFD já garante tokens válidos
                    
                    # Reclassifica identificadores como palavras reservadas
                    if tipo == "IDENTIFICADOR":
                        if lexema in self.palavras_reservadas:
                            tipo = "PALAVRA_RESERVADA"  # Muda o tipo do token
                    

                    # Comentários são reconhecidos mas não incluídos na saída final
                    if tipo not in ("COMENTARIO_LINHA", "COMENTARIO_BLOCO"):
                        tokens.append((lexema, tipo))  # Adiciona token válido à lista
                    
                    # Move o ponteiro pela quantidade de caracteres que o token ocupou
                    self._avancar(tamanho)
            else:
                # FASE 6: TRATAMENTO DE ERRO - AFD NÃO RECONHECEU
                # Se chegou aqui, o AFD não conseguiu fazer match com o caractere atual
                # Isso significa que temos um caractere/sequência inválida na linguagem
                raise ValueError(
                    f"Token inválido na linha {self.linha}, coluna {self.coluna}: '{caractere}'"
                )
        
        # RETORNO: Lista completa de todos os tokens reconhecidos
        return tokens
    
    def _avancar(self, quantidade):
        """
        Avança o ponteiro no código fonte e mantém controle de linha/coluna.
        """
        # AVANÇA CARACTERE POR CARACTERE
        for _ in range(quantidade):
            # Verifica se ainda há caracteres para processar
            if self.posicao < len(self.codigo_fonte):
                # CONTROLE DE LINHA E COLUNA PARA RELATÓRIO DE ERROS
                if self.codigo_fonte[self.posicao] == "\n":
                    # Encontrou quebra de linha: vai para próxima linha, volta coluna para 1
                    self.linha += 1
                    self.coluna = 1
                else:
                    # Caractere normal: apenas avança a coluna
                    self.coluna += 1
                
                # AVANÇA O PONTEIRO PRINCIPAL
                self.posicao += 1

class LexerCoral:
    """Interface principal do analisador léxico da linguagem Coral."""
    
    @staticmethod
    def analisar_arquivo(nome_arquivo):
        """
        Analisa um arquivo Coral e retorna os tokens.
        
        Args:
            nome_arquivo (str): Caminho para o arquivo .coral
            
        Returns:
            list: Lista de tokens (lexema, tipo)
            
        Raises:
            FileNotFoundError: Se o arquivo não existir
            ValueError: Se houver erro léxico
        """
        try:
            with open(nome_arquivo, "r", encoding="utf-8") as f:
                codigo_fonte = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo {nome_arquivo} não encontrado.")
        
        analisador = AnalisadorLexico(codigo_fonte)
        return analisador.tokenizar()
    
    @staticmethod
    def analisar_string(codigo_fonte):
        """
        Analisa uma string de código Coral e retorna os tokens.
        
        Args:
            codigo_fonte (str): Código fonte em Coral
            
        Returns:
            list: Lista de tokens (lexema, tipo)
            
        Raises:
            ValueError: Se houver erro léxico
        """
        analisador = AnalisadorLexico(codigo_fonte)
        return analisador.tokenizar()

def main():
    """
    Função principal para execução via linha de comando.
    
    FLUXO COMPLETO:
    1. Valida argumentos da linha de comando
    2. Lê arquivo fonte
    3. Executa análise léxica (tokenização)
    4. Exibe resultados ou erros
    """
    # VALIDAÇÃO DE ARGUMENTOS
    if len(sys.argv) != 2:
        print("Uso: python lexer.py <arquivo.coral>")
        sys.exit(1)

    nome_arquivo = sys.argv[1]
    
    try:
        # ANÁLISE LÉXICA
        tokens = LexerCoral.analisar_arquivo(nome_arquivo)
        
        # EXIBIÇÃO DOS RESULTADOS
        # Formata e exibe todos os tokens encontrados em formato tabular
        print(f"{'TOKEN':20} | {'TIPO'}")
        print("-" * 40)
        for token, tipo in tokens:
            print(f"{token:20} | {tipo}")
    
    # TRATAMENTO DE ERROS
    except FileNotFoundError as e:
        print(f"Erro: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Erro léxico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()