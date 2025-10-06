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

class Scanner:
    """Scanner/Tokenizador para a linguagem Coral."""
    
    def __init__(self, source):
        """
        Inicializa o scanner com o código fonte.
        
        Args:
            source (str): Código fonte em Coral para tokenizar
        """
        self.source = source
        self.pos = 0
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

    def _eh_alfanumerico_ou_underscore(self, char):
        """Verifica se o caractere é alfanumérico ou underscore."""
        return char.isalnum() or char == '_'
    
    def tokenize(self):
        """
        Realiza a tokenização do código fonte.
        
        Returns:
            list: Lista de tuplas (lexema, tipo_token)
            
        Raises:
            ValueError: Quando encontra token inválido
        """
        tokens = []
        
        while self.pos < len(self.source):
            char = self.source[self.pos]
            
            # Ignora espaços em branco e quebras de linha
            if char.isspace():
                self._avancar(1)
                continue
            
            # Tenta reconhecer token com cada AFD
            resultado = None
            for afd in self.afds:
                resultado = afd.match(self.source[self.pos:])
                if resultado:
                    lexema, tamanho, tipo = resultado
                    
                    # Validação especial: número seguido de letra/underscore = erro
                    if tipo in ("INTEIRO", "DECIMAL"):
                        proxima_pos = self.pos + tamanho
                        if proxima_pos < len(self.source):
                            proximo_char = self.source[proxima_pos]
                            if self._eh_alfanumerico_ou_underscore(proximo_char):
                                # Encontra onde termina a sequência inválida
                                fim_seq = proxima_pos
                                while (fim_seq < len(self.source) and 
                                       self._eh_alfanumerico_ou_underscore(self.source[fim_seq])):
                                    fim_seq += 1
                                sequencia_invalida = self.source[self.pos:fim_seq]
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
                    f"Token inválido na linha {self.linha}, coluna {self.coluna}: '{char}'"
                )
        
        return tokens
    
    def _avancar(self, n):
        """Avança n posições no código fonte, atualizando linha e coluna."""
        for _ in range(n):
            if self.pos < len(self.source):
                if self.source[self.pos] == "\n":
                    self.linha += 1
                    self.coluna = 1
                else:
                    self.coluna += 1
                self.pos += 1

class CoralLexer:
    """Interface principal do analisador léxico da linguagem Coral."""
    
    @staticmethod
    def analyze_file(filename):
        """
        Analisa um arquivo Coral e retorna os tokens.
        
        Args:
            filename (str): Caminho para o arquivo .coral
            
        Returns:
            list: Lista de tokens (lexema, tipo)
            
        Raises:
            FileNotFoundError: Se o arquivo não existir
            ValueError: Se houver erro léxico
        """
        try:
            with open(filename, "r", encoding="utf-8") as f:
                source = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo {filename} não encontrado.")
        
        scanner = Scanner(source)
        return scanner.tokenize()
    
    @staticmethod
    def analyze_string(source):
        """
        Analisa uma string de código Coral e retorna os tokens.
        
        Args:
            source (str): Código fonte em Coral
            
        Returns:
            list: Lista de tokens (lexema, tipo)
            
        Raises:
            ValueError: Se houver erro léxico
        """
        scanner = Scanner(source)
        return scanner.tokenize()

def main():
    """Função principal para execução via linha de comando."""
    if len(sys.argv) != 2:
        print("Uso: python lexer.py <arquivo.coral>")
        sys.exit(1)

    filename = sys.argv[1]
    
    try:
        tokens = CoralLexer.analyze_file(filename)
        
        # Exibe tabela de tokens
        print(f"{'TOKEN':20} | {'TIPO'}")
        print("-" * 40)
        for token, tipo in tokens:
            print(f"{token:20} | {tipo}")
            
        print(f"\nTotal de tokens encontrados: {len(tokens)}")
        
    except FileNotFoundError as e:
        print(f"Erro: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Erro léxico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()