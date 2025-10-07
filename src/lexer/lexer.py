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
        self.codigo_fonte = codigo_fonte
        self.posicao = 0
        self.linha = 1
        self.coluna = 1
        
        # Palavras reservadas da linguagem Coral
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
        
        # Obtém lista de AFDs na ordem de prioridade
        self.afds = get_afds()

    def _eh_alfanumerico_ou_underscore(self, caractere):
        """Verifica se o caractere é alfanumérico ou underscore."""
        return caractere.isalnum() or caractere == '_'
    
    def tokenizar(self):
        """
        Realiza a tokenização do código fonte.
        
        Returns:
            list: Lista de tuplas (lexema, tipo_token)
            
        Raises:
            ValueError: Quando encontra token inválido
        """
        tokens = []
        
        while self.posicao < len(self.codigo_fonte):
            caractere = self.codigo_fonte[self.posicao]
            
            # Ignora espaços em branco e quebras de linha
            if caractere.isspace():
                self._avancar(1)
                continue
            
            # Tenta reconhecer token com cada AFD
            resultado = None
            for afd in self.afds:
                resultado = afd.match(self.codigo_fonte[self.posicao:])
                if resultado:
                    lexema, tamanho, tipo = resultado
                    
                    # Validação especial: número seguido de letra/underscore = erro
                    if tipo in ("INTEIRO", "DECIMAL"):
                        proxima_posicao = self.posicao + tamanho
                        if proxima_posicao < len(self.codigo_fonte):
                            proximo_caractere = self.codigo_fonte[proxima_posicao]
                            if self._eh_alfanumerico_ou_underscore(proximo_caractere):
                                # Encontra onde termina a sequência inválida
                                fim_sequencia = proxima_posicao
                                while (fim_sequencia < len(self.codigo_fonte) and 
                                       self._eh_alfanumerico_ou_underscore(self.codigo_fonte[fim_sequencia])):
                                    fim_sequencia += 1
                                sequencia_invalida = self.codigo_fonte[self.posicao:fim_sequencia]
                                raise ValueError(
                                    f"Token inválido na linha {self.linha}, coluna {self.coluna}: "
                                    f"'{sequencia_invalida}' - números não podem ser seguidos por letras"
                                )
                    
                    # Classifica identificadores vs palavras reservadas
                    if tipo == "IDENTIFICADOR":
                        if lexema in self.palavras_reservadas:
                            tipo = "PALAVRA_RESERVADA"
                    
                    # Comentários são processados mas não incluídos na saída
                    if tipo not in ("COMENTARIO_LINHA", "COMENTARIO_BLOCO"):
                        tokens.append((lexema, tipo))
                    
                    self._avancar(tamanho)
                    break
            
            # Se nenhum AFD reconheceu o token
            if not resultado:
                raise ValueError(
                    f"Token inválido na linha {self.linha}, coluna {self.coluna}: '{caractere}'"
                )
        
        return tokens
    
    def _avancar(self, quantidade):
        """Avança quantidade de posições no código fonte, atualizando linha e coluna."""
        for _ in range(quantidade):
            if self.posicao < len(self.codigo_fonte):
                if self.codigo_fonte[self.posicao] == "\n":
                    self.linha += 1
                    self.coluna = 1
                else:
                    self.coluna += 1
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
    """Função principal para execução via linha de comando."""
    if len(sys.argv) != 2:
        print("Uso: python lexer.py <arquivo.coral>")
        sys.exit(1)

    nome_arquivo = sys.argv[1]
    
    try:
        tokens = LexerCoral.analisar_arquivo(nome_arquivo)
        
        # Exibe tabela de tokens
        print(f"{'TOKEN':20} | {'TIPO'}")
        print("-" * 40)
        for token, tipo in tokens:
            print(f"{token:20} | {tipo}")
                    
    except FileNotFoundError as e:
        print(f"Erro: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Erro léxico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()