import sys
import os

src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, src_dir)

from lexer.AFD import get_afd
from lexer.Token import Token
from lexer.Buffer import BufferLeitura

class AnalisadorLexico:
    """Analisador léxico/Tokenizador para a linguagem Coral."""
    
    def __init__(self, codigo_fonte):
        self.buffer_leitura = BufferLeitura(codigo_fonte)
        
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

        self.afd = get_afd()
    
    def _reconhecer_proximo_token(self):
        """Reconhece e retorna o próximo token do código fonte."""
        while not self.buffer_leitura.fim_arquivo():
            caractere = self.buffer_leitura.caractere_atual()
            
            if caractere.isspace():
                self.buffer_leitura.avancar(1)
                continue
            
            pos_info = self.buffer_leitura.get_posicao_info()
            resultado = self.afd.match(self.buffer_leitura.resto_codigo())
            
            if resultado:
                lexema, tamanho, tipo = resultado
                
                # Reclassifica palavras reservadas
                if tipo == "IDENTIFICADOR" and lexema in self.palavras_reservadas:
                    tipo = "PALAVRA_RESERVADA"
                
                token = Token(lexema, tipo, pos_info['linha'], pos_info['coluna'], pos_info['posicao'])
                self.buffer_leitura.avancar(tamanho)
                return token
            else:
                raise ValueError(
                    f"Token inválido na linha {pos_info['linha']}, coluna {pos_info['coluna']}: '{caractere}'"
                )
        
        return None
    
    def getNextToken(self):
        """Retorna o próximo token para o analisador sintático."""
        token = self._reconhecer_proximo_token()
        
        # Pula comentários
        while token and token.tipo in ("COMENTARIO_LINHA", "COMENTARIO_BLOCO"):
            token = self._reconhecer_proximo_token()
        
        # Retorna EOF se acabou
        if token is None:
            pos_info = self.buffer_leitura.get_posicao_info()
            token = Token("", "EOF", pos_info['linha'], pos_info['coluna'], pos_info['posicao'])
        
        return token
    
    def peekNextToken(self):
        """Espia o próximo token sem consumi-lo (lookahead)."""
        pos_salva = self.buffer_leitura.posicao
        linha_salva = self.buffer_leitura.linha
        coluna_salva = self.buffer_leitura.coluna
        
        token = self.getNextToken()
        
        self.buffer_leitura.posicao = pos_salva
        self.buffer_leitura.linha = linha_salva
        self.buffer_leitura.coluna = coluna_salva
        
        return token

class LexerCoral:
    """Interface principal do analisador léxico da linguagem Coral."""
    
    @staticmethod
    def analisar_arquivo(nome_arquivo):
        """Analisa um arquivo Coral retornando o analisador léxico."""
        try:
            with open(nome_arquivo, "r", encoding="utf-8") as f:
                codigo_fonte = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo {nome_arquivo} não encontrado.")
        
        return AnalisadorLexico(codigo_fonte)
    
    @staticmethod
    def analisar_string(codigo_fonte):
        """Analisa uma string de código Coral retornando o analisador léxico."""
        return AnalisadorLexico(codigo_fonte)

def main():
    """Função principal para execução via linha de comando."""
    if len(sys.argv) != 2:
        print("Uso: python lexer.py <arquivo.coral>")
        sys.exit(1)

    nome_arquivo = sys.argv[1]
    
    try:
        lexer = LexerCoral.analisar_arquivo(nome_arquivo)
        
        print(f"{'TOKEN':20} | {'TIPO'}")
        print("-" * 40)
        
        while True:
            token = lexer.getNextToken()
            if token.tipo == "EOF":
                break
            print(f"{token.lexema:20} | {token.tipo}")
    
    except FileNotFoundError as e:
        print(f"Erro: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Erro léxico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()