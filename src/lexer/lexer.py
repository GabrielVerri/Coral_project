import sys
import os

src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, src_dir)

from lexer.AFD import get_afd
from lexer.Token import Token
from lexer.Buffer import BufferLeitura

class AnalisadorLexico:
    """Analisador léxico/Tokenizador para a linguagem Coral com suporte a INDENTA/DEDENTA."""
    
    def __init__(self, codigo_fonte):
        self.buffer_leitura = BufferLeitura(codigo_fonte)
        
        self.palavras_reservadas = {
            'SE', 'SENAO', 'SENAOSE', 'ENQUANTO', 'PARA', 'DENTRODE',
            'INTEIRO', 'DECIMAL', 'TEXTO', 'BOOLEANO',
            'DEF', 'FUNCAO', 'CLASSE', 'RETORNAR',
            'QUEBRA', 'CONTINUA', 'PASSAR',
            'GLOBAL', 'NAOLOCAL', 'IMPORTAR', 'DE', 'COMO',
            'TENTE', 'EXCETO', 'FINALMENTE', 'LANCAR', 'AFIRMA',
            'ESPERA', 'VAZIO', 'EIGUAL', 'LAMBDA', 'COM', 'DELETAR',
            'ASSINCRONO', 'ENVIAR'
        }

        self.afd = get_afd()
        
        # Sistema de rastreamento de indentação
        self.pilha_indentacao = [0]
        self.tokens_pendentes = []
        self.inicio_linha = True
        self.nivel_parenteses = 0
    
    def _processar_indentacao(self, pos_info):
        """Processa a indentação no início de uma linha."""
        # Conta espaços/tabs no início da linha
        nivel_indentacao = 0
        while not self.buffer_leitura.fim_arquivo():
            char = self.buffer_leitura.caractere_atual()
            if char == ' ':
                nivel_indentacao += 1
                self.buffer_leitura.avancar(1)
            elif char == '\t':
                nivel_indentacao += 4  # Tab conta como 4 espaços
                self.buffer_leitura.avancar(1)
            else:
                break
        
        # Se a linha está vazia ou é comentário, ignora indentação
        if self.buffer_leitura.fim_arquivo():
            return
        
        char_atual = self.buffer_leitura.caractere_atual()
        if char_atual == '\n' or char_atual == '\r':
            return  # Linha vazia
        
        # Verifica se é comentário
        resto = self.buffer_leitura.resto_codigo()
        if resto.startswith('#'):
            return  # Linha de comentário
        
        # Compara com o nível de indentação atual
        nivel_atual = self.pilha_indentacao[-1]
        
        if nivel_indentacao > nivel_atual:
            self.pilha_indentacao.append(nivel_indentacao)
            self.tokens_pendentes.append(
                Token("", "INDENTA", pos_info['linha'], nivel_indentacao, pos_info['posicao'])
            )
        
        elif nivel_indentacao < nivel_atual:
            while self.pilha_indentacao and self.pilha_indentacao[-1] > nivel_indentacao:
                self.pilha_indentacao.pop()
                self.tokens_pendentes.append(
                    Token("", "DEDENTA", pos_info['linha'], nivel_indentacao, pos_info['posicao'])
                )
            
            if not self.pilha_indentacao or self.pilha_indentacao[-1] != nivel_indentacao:
                raise ValueError(
                    f"Indentação inconsistente na linha {pos_info['linha']}, coluna {pos_info['coluna']}"
                )
    
    def _reconhecer_proximo_token(self):
        """Reconhece e retorna o próximo token do código fonte."""
        # Se há tokens pendentes (INDENT/DEDENT), retorna eles primeiro
        if self.tokens_pendentes:
            return self.tokens_pendentes.pop(0)
        
        # Processa indentação no início de linha
        if self.inicio_linha and self.nivel_parenteses == 0:
            pos_info = self.buffer_leitura.get_posicao_info()
            self._processar_indentacao(pos_info)
            self.inicio_linha = False
            
            # Se gerou tokens de indentação, retorna o primeiro
            if self.tokens_pendentes:
                return self.tokens_pendentes.pop(0)
        
        # Pula espaços em branco (exceto newline)
        while not self.buffer_leitura.fim_arquivo():
            caractere = self.buffer_leitura.caractere_atual()
            
            # Newline marca início de nova linha
            if caractere == '\n' or caractere == '\r':
                pos_info = self.buffer_leitura.get_posicao_info()
                
                # Pula o newline
                if caractere == '\r' and not self.buffer_leitura.fim_arquivo():
                    self.buffer_leitura.avancar(1)
                    if self.buffer_leitura.caractere_atual() == '\n':
                        self.buffer_leitura.avancar(1)
                else:
                    self.buffer_leitura.avancar(1)
                
                self.inicio_linha = True
                
                # Só retorna NEWLINE se não estiver dentro de parênteses
                if self.nivel_parenteses == 0:
                    return Token("\\n", "NEWLINE", pos_info['linha'], pos_info['coluna'], pos_info['posicao'])
                else:
                    continue  # Ignora newline dentro de parênteses
            
            # Outros espaços em branco
            if caractere in ' \t':
                self.buffer_leitura.avancar(1)
                continue
            
            break
        
        # Fim do arquivo: gera DEDENTAs pendentes
        if self.buffer_leitura.fim_arquivo():
            pos_info = self.buffer_leitura.get_posicao_info()
            
            while len(self.pilha_indentacao) > 1:
                self.pilha_indentacao.pop()
                self.tokens_pendentes.append(
                    Token("", "DEDENTA", pos_info['linha'], 0, pos_info['posicao'])
                )
            
            if self.tokens_pendentes:
                return self.tokens_pendentes.pop(0)
            
            return None
        
        # Reconhece o próximo token normalmente
        pos_info = self.buffer_leitura.get_posicao_info()
        resultado = self.afd.match(self.buffer_leitura.resto_codigo())
        
        if resultado:
            lexema, tamanho, tipo = resultado
            
            # Reclassifica palavras reservadas
            if tipo == "IDENTIFICADOR" and lexema in self.palavras_reservadas:
                tipo = "PALAVRA_RESERVADA"
            
            # Rastreia parênteses/colchetes/chaves
            if lexema in '([{':
                self.nivel_parenteses += 1
            elif lexema in ')]}':
                self.nivel_parenteses -= 1
            
            token = Token(lexema, tipo, pos_info['linha'], pos_info['coluna'], pos_info['posicao'])
            self.buffer_leitura.avancar(tamanho)
            return token
        else:
            caractere = self.buffer_leitura.caractere_atual()
            raise ValueError(
                f"Token inválido na linha {pos_info['linha']}, coluna {pos_info['coluna']}: '{caractere}'"
            )
    
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
