import sys
import os

# Adiciona o diretório src ao path do Python para imports
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, src_dir)

# Importa os AFDs necessários
from lexer.AFD import get_afds
from lexer.Token import Token
from lexer.Buffer import BufferLeitura, BufferTokens

class AnalisadorLexico:
    """Analisador léxico/Tokenizador para a linguagem Coral."""
    
    def __init__(self, codigo_fonte):
        # BUFFERS: Gerenciam leitura do código e armazenamento de tokens
        self.buffer_leitura = BufferLeitura(codigo_fonte)  # Controla posição, linha, coluna
        self.buffer_tokens = BufferTokens()                 # Armazena tokens reconhecidos
        
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
        # LOOP PRINCIPAL: Percorre todo o código fonte caractere por caractere
        while not self.buffer_leitura.fim_arquivo():
            caractere = self.buffer_leitura.caractere_atual()  # Caractere atual
            
            # Pula espaços, tabs, quebras de linha
            if caractere.isspace():
                self.buffer_leitura.avancar(1)  # Move ponteiro e atualiza linha/coluna
                continue                         # Volta para o início do loop
            
            # CAPTURA INFORMAÇÃO DE POSIÇÃO ANTES DO MATCH
            # Salva linha, coluna e posição onde o token começa
            pos_info = self.buffer_leitura.get_posicao_info()
            
            # TENTATIVA DE MATCH COM O AFD UNIFICADO
            # Como temos apenas 1 AFD unificado, não precisamos de loop
            afd_unificado = self.afds[0]  # Acessa diretamente o único AFD
            
            # TENTATIVA DE MATCH: 
            # - Passa o resto do código (da posição atual até o fim)
            # - Retorna None se não reconhecer, ou (lexema, tamanho, tipo) se reconhecer
            resultado = afd_unificado.match(self.buffer_leitura.resto_codigo())
            
            if resultado:  # AFD reconheceu um token
                    lexema, tamanho, tipo = resultado
                    # lexema: o texto do token
                    # tamanho: quantos caracteres o token ocupa 
                    # tipo: categoria do token (ex: "PALAVRA_RESERVADA", "INTEIRO")
                    
                    # Reclassifica identificadores como palavras reservadas
                    if tipo == "IDENTIFICADOR":
                        if lexema in self.palavras_reservadas:
                            tipo = "PALAVRA_RESERVADA"  # Muda o tipo do token
                    
                    # Comentários são reconhecidos mas não incluídos na saída final
                    if tipo not in ("COMENTARIO_LINHA", "COMENTARIO_BLOCO"):
                        # Cria objeto Token com informações de posição
                        token = Token(
                            lexema=lexema,
                            tipo=tipo,
                            linha=pos_info['linha'],
                            coluna=pos_info['coluna'],
                            posicao=pos_info['posicao']
                        )
                        self.buffer_tokens.adicionar(token)  # Adiciona ao buffer
                    
                    # Move o ponteiro pela quantidade de caracteres que o token ocupou
                    self.buffer_leitura.avancar(tamanho)
            else:
                # FASE 6: TRATAMENTO DE ERRO - AFD NÃO RECONHECEU
                # Se chegou aqui, o AFD não conseguiu fazer match com o caractere atual
                # Isso significa que temos um caractere/sequência inválida na linguagem
                raise ValueError(
                    f"Token inválido na linha {pos_info['linha']}, coluna {pos_info['coluna']}: '{caractere}'"
                )
        
        # RETORNO: Buffer completo com todos os tokens reconhecidos
        return self.buffer_tokens

class LexerCoral:
    """Interface principal do analisador léxico da linguagem Coral."""
    
    @staticmethod
    def analisar_arquivo(nome_arquivo):
        try:
            with open(nome_arquivo, "r", encoding="utf-8") as f:
                codigo_fonte = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo {nome_arquivo} não encontrado.")
        
        analisador = AnalisadorLexico(codigo_fonte)
        return analisador.tokenizar()
    
    @staticmethod
    def analisar_string(codigo_fonte):
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
        buffer_tokens = LexerCoral.analisar_arquivo(nome_arquivo)
        
        # EXIBIÇÃO DOS RESULTADOS
        # Formata e exibe todos os tokens encontrados em formato tabular
        print(f"{'TOKEN':20} | {'TIPO'}")
        print("-" * 40)
        
        # Itera sobre o buffer obtendo tokens como tuplas (lexema, tipo)
        for token, tipo in buffer_tokens.obter_tuplas():
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