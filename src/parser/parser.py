"""
Parser Preditivo LL(1) para a linguagem Coral.

Implementa um analisador sintático descendente recursivo que constrói
uma Árvore Sintática Abstrata (AST) a partir do fluxo de tokens.
"""

import sys
import os

if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

try:
    from src.parser.ast_nodes import *
    from src.parser.first_follow import FirstFollowSets
    from src.utils import (PALAVRAS_RESERVADAS, OPERADORES_LOGICOS, 
                           OPERADORES_BOOLEANOS, TIPO_MAP)
except ModuleNotFoundError:
    from .ast_nodes import *
    from .first_follow import FirstFollowSets
    from utils import (PALAVRAS_RESERVADAS, OPERADORES_LOGICOS,
                       OPERADORES_BOOLEANOS, TIPO_MAP)


class ErroSintatico(Exception):
    """Exceção lançada quando há erro de sintaxe durante o parsing."""
    def __init__(self, mensagem, linha=None, coluna=None):
        self.mensagem = mensagem
        self.linha = linha
        self.coluna = coluna
        super().__init__(self.formatar_mensagem())
    
    def formatar_mensagem(self):
        if self.linha is not None and self.coluna is not None:
            return f"Erro sintático na linha {self.linha}, coluna {self.coluna}: {self.mensagem}"
        return f"Erro sintático: {self.mensagem}"


class ParserCoral:
    """
    Parser preditivo LL(1) para a linguagem Coral.
    
    Utiliza os conjuntos FIRST e FOLLOW para decidir qual produção aplicar
    durante a análise sintática descendente.
    """
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicao = 0
        self.token_atual = tokens[0] if tokens else None
        self.first_follow = FirstFollowSets()
    
    def avancar(self):
        if self.posicao < len(self.tokens) - 1:
            self.posicao += 1
            self.token_atual = self.tokens[self.posicao]
        return self.token_atual
    
    def verificar(self, tipo_esperado):
        if not self.token_atual:
            return False
        
        if tipo_esperado in PALAVRAS_RESERVADAS:
            return (self.token_atual.tipo == 'PALAVRA_RESERVADA' and 
                    self.token_atual.lexema == tipo_esperado)
        
        if tipo_esperado in OPERADORES_LOGICOS:
            return (self.token_atual.tipo == 'OPERADOR_LOGICO' and 
                    self.token_atual.lexema == tipo_esperado)
        
        if tipo_esperado == 'BOOLEANO':
            if self.token_atual.tipo == 'BOOLEANO':
                return True
            if self.token_atual.lexema in OPERADORES_BOOLEANOS:
                return True
            return False
        
        if tipo_esperado in ['(', ')', '[', ']', '{', '}', ':', ',', 
                             '+', '-', '*', '/', '%', '**',
                             '==', '!=', '<', '>', '<=', '>=',
                             '=', '+=', '-=', '*=', '/=', '%=']:
            return self.token_atual.lexema == tipo_esperado
        
        tipo_verificar = TIPO_MAP.get(tipo_esperado, tipo_esperado)
        return self.token_atual.tipo == tipo_verificar
    
    def consumir(self, tipo_esperado, mensagem_erro=None):
        """
        Consome o token atual se for do tipo esperado, caso contrário lança erro.
        
        Args:
            tipo_esperado: Tipo do token ou lexema esperado
            mensagem_erro: Mensagem de erro customizada
            
        Returns:
            Token consumido
        """
        if not self.verificar(tipo_esperado):
            if mensagem_erro is None:
                token_encontrado = self.token_atual.lexema if self.token_atual else 'EOF'
                mensagem_erro = f"Esperado '{tipo_esperado}', encontrado '{token_encontrado}'"
            raise ErroSintatico(
                mensagem_erro,
                self.token_atual.linha if self.token_atual else None,
                self.token_atual.coluna if self.token_atual else None
            )
        token = self.token_atual
        self.avancar()
        return token
    
    def olhar_adiante(self, offset=1):
        """
        Retorna o token à frente sem consumir.
        
        Args:
            offset: Quantos tokens olhar à frente (padrão: 1)
            
        Returns:
            Token na posição atual + offset, ou None se não existir
        """
        posicao_futura = self.posicao + offset
        if posicao_futura < len(self.tokens):
            return self.tokens[posicao_futura]
        return None
    
    def fim_arquivo(self):
        """Verifica se chegou ao fim do arquivo."""
        return self.token_atual is None or self.token_atual.tipo == 'EOF'
    
    # ===== MÉTODOS DE PARSING =====
    
    def parse(self):
        """
        Método principal do parser. Inicia a análise sintática.
        
        Returns:
            ProgramaNode - raiz da AST
        """
        return self.programa()
    
    def programa(self):
        """
        Analisa o programa completo.
        
        Returns:
            ProgramaNode: Nó raiz da árvore sintática abstrata.
        """
        declaracoes = []
        
        while not self.fim_arquivo():
            if self.verificar('NEWLINE'):
                self.avancar()
                continue
            
            declaracao = self.declaracao()
            if declaracao:
                declaracoes.append(declaracao)
        
        return ProgramaNode(declaracoes)
    
    def declaracao(self):
        """
        Processa uma declaração (estrutura de controle, função, classe ou expressão).
        
        Returns:
            ASTNode: Nó da declaração processada.
        """
        if self.verificar('SE'):
            return self.estrutura_se()
        elif self.verificar('ENQUANTO'):
            return self.estrutura_enquanto()
        elif self.verificar('PARA'):
            return self.estrutura_para()
        elif self.verificar('FUNCAO'):
            return self.funcao()
        elif self.verificar('CLASSE'):
            return self.classe()
        elif self.verificar('RETORNAR'):
            return self.retornar()
        elif self.verificar('QUEBRA'):
            return self.quebra()
        elif self.verificar('CONTINUA'):
            return self.continua()
        elif self.verificar('PASSAR'):
            return self.passar()
        else:
            # Tenta parsing de expressão/atribuição
            return self.expressao_ou_atribuicao()
    
    def expressao_ou_atribuicao(self):
        """
        Trata expressões ou atribuições.
        Se encontrar ID seguido de =, +=, -=, etc., é atribuição.
        Caso contrário, é expressão.
        """
        if self.verificar('ID'):
            proximo = self.olhar_adiante(1)
            if proximo and proximo.lexema in ['=', '+=', '-=', '*=', '/=', '%=']:
                return self.atribuicao()
        
        return self.expressao()
    
    def atribuicao(self):
        """
        Processa uma atribuição de variável.
        
        Returns:
            AtribuicaoNode: Nó de atribuição.
        """
        identificador_token = self.consumir('ID')
        identificador = IdentificadorNode(
            identificador_token.lexema,
            identificador_token.linha,
            identificador_token.coluna
        )
        
        operador = self.token_atual
        if operador.lexema not in ['=', '+=', '-=', '*=', '/=', '%=']:
            raise ErroSintatico(
                f"Operador de atribuição esperado, encontrado '{operador.lexema}'",
                operador.linha,
                operador.coluna
            )
        self.avancar()
        
        expressao = self.expressao()
        
        return AtribuicaoNode(
            identificador,
            operador.lexema,
            expressao,
            identificador_token.linha,
            identificador_token.coluna
        )
    
    def expressao(self):
        """
        Processa uma expressão.
        
        Returns:
            ExpressaoNode: Nó de expressão.
        """
        termo = self.termo()
        return self.expr_resto(termo)
    
    def expr_resto(self, esquerda):
        """
        Processa o resto de uma expressão (operadores E, OU).
        
        Args:
            esquerda: Nó da expressão à esquerda.
            
        Returns:
            ExpressaoNode: Nó de expressão completa ou o nó esquerda se não houver continuação.
        """
        if self.verificar('E') or self.verificar('OU'):
            operador = self.token_atual
            self.avancar()
            direita = self.termo()
            binaria = ExpressaoBinariaNode(
                esquerda,
                operador,
                direita,
                operador.linha,
                operador.coluna
            )
            return self.expr_resto(binaria)
        
        return esquerda
    
    def termo(self):
        """
        Processa um termo (soma seguido de operadores relacionais).
        
        Returns:
            ExpressaoNode: Nó de termo.
        """
        soma = self.soma()
        return self.termo_resto(soma)
    
    def termo_resto(self, esquerda):
        """
        Processa o resto de um termo (operadores relacionais).
        
        Args:
            esquerda: Nó da expressão à esquerda.
            
        Returns:
            ExpressaoNode: Nó completo ou o nó esquerda se não houver continuação.
        """
        if self.token_atual and self.token_atual.lexema in ['==', '!=', '<', '>', '<=', '>=']:
            operador = self.token_atual
            self.avancar()
            direita = self.soma()
            binaria = ExpressaoBinariaNode(
                esquerda,
                operador,
                direita,
                operador.linha,
                operador.coluna
            )
            return self.termo_resto(binaria)
        
        return esquerda
    
    def soma(self):
        """
        Processa uma soma (fator seguido de operadores de adição e subtração).
        
        Returns:
            ExpressaoNode: Nó de soma.
        """
        fator = self.fator()
        return self.soma_resto(fator)
    
    def soma_resto(self, esquerda):
        """
        Processa o resto de uma soma (operadores de adição e subtração).
        
        Args:
            esquerda: Nó da expressão à esquerda.
            
        Returns:
            ExpressaoNode: Nó completo ou o nó esquerda se não houver continuação.
        """
        if self.token_atual and self.token_atual.lexema in ['+', '-']:
            operador = self.token_atual
            self.avancar()
            direita = self.fator()
            binaria = ExpressaoBinariaNode(
                esquerda,
                operador,
                direita,
                operador.linha,
                operador.coluna
            )
            return self.soma_resto(binaria)
        
        return esquerda
    
    def fator(self):
        """
        Processa um fator (exponenciação seguido de operadores de multiplicação).
        
        Returns:
            ExpressaoNode: Nó de fator.
        """
        exponencial = self.exponenciacao()
        return self.fator_resto(exponencial)
    
    def fator_resto(self, esquerda):
        """
        Processa o resto de um fator (operadores de multiplicação, divisão e módulo).
        
        Args:
            esquerda: Nó da expressão à esquerda.
            
        Returns:
            ExpressaoNode: Nó completo ou o nó esquerda se não houver continuação.
        """
        if self.token_atual and self.token_atual.lexema in ['*', '/', '%']:
            operador = self.token_atual
            self.avancar()
            direita = self.exponenciacao()
            binaria = ExpressaoBinariaNode(
                esquerda,
                operador,
                direita,
                operador.linha,
                operador.coluna
            )
            return self.fator_resto(binaria)
        
        return esquerda
    
    def exponenciacao(self):
        """
        Processa exponenciação com associatividade à direita.
        
        Returns:
            ExpressaoNode: Nó de exponenciação.
        """
        base = self.fator_primario()
        
        if self.token_atual and self.token_atual.lexema == '**':
            operador = self.token_atual
            self.avancar()
            expoente = self.exponenciacao()
            return ExpressaoBinariaNode(
                base,
                operador,
                expoente,
                operador.linha,
                operador.coluna
            )
        
        return base
    
    def fator_primario(self):
        """
        Processa um fator primário (literais, identificadores, operadores unários, etc.).
        
        Returns:
            ExpressaoNode: Nó de fator primário.
        """
        if self.verificar('INTEIRO'):
            token = self.token_atual
            self.avancar()
            return LiteralNode(int(token.lexema), 'INTEIRO', token.linha, token.coluna)
        
        if self.verificar('DECIMAL'):
            token = self.token_atual
            self.avancar()
            return LiteralNode(float(token.lexema), 'DECIMAL', token.linha, token.coluna)
        
        if self.verificar('BOOLEANO'):
            token = self.token_atual
            self.avancar()
            valor = token.lexema == 'VERDADE'
            return LiteralNode(valor, 'BOOLEANO', token.linha, token.coluna)
        
        if self.verificar('VAZIO'):
            token = self.token_atual
            self.avancar()
            return LiteralNode(None, 'VAZIO', token.linha, token.coluna)
        
        if self.verificar('STRING'):
            token = self.token_atual
            self.avancar()
            valor = token.lexema[1:-1] if len(token.lexema) >= 2 else token.lexema
            return LiteralNode(valor, 'STRING', token.linha, token.coluna)
        
        if self.verificar('ID'):
            token = self.token_atual
            self.avancar()
            
            if self.verificar('('):
                self.avancar()
                argumentos = self.lista_argumentos()
                self.consumir(')', "Esperado ')' após argumentos da função")
                return ChamadaFuncaoNode(token.lexema, argumentos, token.linha, token.coluna)
            
            return IdentificadorNode(token.lexema, token.linha, token.coluna)
        
        if self.verificar('('):
            self.avancar()
            expressao = self.expressao()
            self.consumir(')', "Esperado ')' após expressão")
            return expressao
        
        if self.verificar('['):
            token = self.token_atual
            self.avancar()
            elementos = self.lista_argumentos()
            self.consumir(']', "Esperado ']' após elementos da lista")
            return ListaNode(elementos, token.linha, token.coluna)
        
        if self.verificar('{'):
            token = self.token_atual
            self.avancar()
            
            # TODO: Implementar parsing de dicionários vs conjuntos
            elementos = self.lista_argumentos()
            self.consumir('}', "Esperado '}' após elementos")
            return DicionarioNode([], token.linha, token.coluna)
        
        if self.verificar('-'):
            operador = self.token_atual
            self.avancar()
            expressao = self.exponenciacao()
            return ExpressaoUnariaNode(operador, expressao, operador.linha, operador.coluna)
        
        if self.verificar('NAO'):
            operador = self.token_atual
            self.avancar()
            expressao = self.exponenciacao()
            return ExpressaoUnariaNode(operador, expressao, operador.linha, operador.coluna)
        
        raise ErroSintatico(
            f"Expressão esperada, encontrado '{self.token_atual.tipo if self.token_atual else 'EOF'}'",
            self.token_atual.linha if self.token_atual else None,
            self.token_atual.coluna if self.token_atual else None
        )
    
    def lista_argumentos(self):
        """
        Processa uma lista de argumentos separados por vírgula.
        
        Returns:
            list: Lista de nós de expressão.
        """
        argumentos = []
        
        if self.token_atual and self.token_atual.lexema in [')', ']', '}']:
            return argumentos
        
        argumentos.append(self.expressao())
        
        # Argumentos adicionais
        while self.verificar(','):
            self.avancar()
            argumentos.append(self.expressao())
        
        return argumentos
    
    def estrutura_se(self):
        """
        Processa uma estrutura condicional SE/SENAOSE/SENAO.
        
        Returns:
            SeNode: Nó de estrutura condicional.
        """
        token_se = self.consumir('SE')
        condicao = self.expressao()
        self.consumir(':', "Esperado ':' após condição do SE")
        bloco_se = self.bloco()
        
        blocos_senaose = []
        while self.verificar('SENAOSE'):
            self.avancar()
            condicao_senaose = self.expressao()
            self.consumir(':', "Esperado ':' após condição do SENAOSE")
            bloco_senaose = self.bloco()
            blocos_senaose.append((condicao_senaose, bloco_senaose))
        
        bloco_senao = None
        if self.verificar('SENAO'):
            self.avancar()
            self.consumir(':', "Esperado ':' após SENAO")
            bloco_senao = self.bloco()
        
        return SeNode(
            condicao,
            bloco_se,
            blocos_senaose,
            bloco_senao,
            token_se.linha,
            token_se.coluna
        )
    
    def estrutura_enquanto(self):
        """
        Processa uma estrutura de repetição ENQUANTO.
        
        Returns:
            EnquantoNode: Nó de loop ENQUANTO.
        """
        token_enquanto = self.consumir('ENQUANTO')
        condicao = self.expressao()
        self.consumir(':', "Esperado ':' após condição do ENQUANTO")
        bloco = self.bloco()
        
        return EnquantoNode(condicao, bloco, token_enquanto.linha, token_enquanto.coluna)
    
    def estrutura_para(self):
        """
        Processa uma estrutura de repetição PARA.
        
        Returns:
            ParaNode: Nó de loop PARA.
        """
        token_para = self.consumir('PARA')
        token_var = self.consumir('ID', "Esperado identificador após PARA")
        variavel = IdentificadorNode(token_var.lexema, token_var.linha, token_var.coluna)
        
        self.consumir('DENTRODE', "Esperado 'DENTRODE' no laço PARA")
        iteravel = self.expressao()
        self.consumir(':', "Esperado ':' após expressão do PARA")
        bloco = self.bloco()
        
        return ParaNode(variavel, iteravel, bloco, token_para.linha, token_para.coluna)
    
    def funcao(self):
        """
        Processa uma declaração de função.
        
        Returns:
            FuncaoNode: Nó de declaração de função.
        """
        token_funcao = self.consumir('FUNCAO')
        token_nome = self.consumir('ID', "Esperado nome da função")
        nome = token_nome.lexema
        
        self.consumir('(', "Esperado '(' após nome da função")
        parametros = self.lista_parametros()
        self.consumir(')', "Esperado ')' após parâmetros da função")
        self.consumir(':', "Esperado ':' após assinatura da função")
        
        bloco = self.bloco()
        
        return FuncaoNode(nome, parametros, bloco, token_funcao.linha, token_funcao.coluna)
    
    def lista_parametros(self):
        """
        Processa uma lista de parâmetros de função.
        
        Returns:
            list: Lista de nós de parâmetros.
        """
        parametros = []
        
        if self.verificar(')'):
            return parametros
        parametros.append(self.parametro())
        
        while self.verificar(','):
            self.avancar()
            parametros.append(self.parametro())
        
        return parametros
    
    def parametro(self):
        """
        Processa um parâmetro de função (com ou sem valor padrão).
        
        Returns:
            ParametroNode: Nó de parâmetro.
        """
        token = self.consumir('ID', "Esperado nome do parâmetro")
        nome = token.lexema
        
        valor_padrao = None
        if self.verificar('='):
            self.avancar()
            valor_padrao = self.expressao()
        
        return ParametroNode(nome, valor_padrao, token.linha, token.coluna)
    
    def classe(self):
        """
        Processa uma declaração de classe.
        
        Returns:
            ClasseNode: Nó de declaração de classe.
        """
        token_classe = self.consumir('CLASSE')
        token_nome = self.consumir('ID', "Esperado nome da classe")
        nome = token_nome.lexema
        
        self.consumir(':', "Esperado ':' após nome da classe")
        bloco = self.bloco()
        
        return ClasseNode(nome, bloco, token_classe.linha, token_classe.coluna)
    
    def bloco(self):
        """
        Processa um bloco de código indentado.
        
        Returns:
            BlocoNode: Nó de bloco com declarações.
        """
        self.consumir('NEWLINE', "Esperado nova linha antes do bloco")
        self.consumir('INDENTA', "Esperado indentação para início do bloco")
        
        declaracoes = []
        while not self.verificar('DEDENTA') and not self.fim_arquivo():
            if self.verificar('NEWLINE'):
                self.avancar()
                continue
            
            declaracao = self.declaracao()
            if declaracao:
                declaracoes.append(declaracao)
        
        self.consumir('DEDENTA', "Esperado fim de indentação para fechar o bloco")
        
        return BlocoNode(declaracoes)
    
    def retornar(self):
        """
        Processa uma instrução de retorno.
        
        Returns:
            RetornarNode: Nó de retorno.
        """
        token = self.consumir('RETORNAR')
        
        expressao = None
        if not self.verificar('NEWLINE') and not self.fim_arquivo():
            expressao = self.expressao()
        
        return RetornarNode(expressao, token.linha, token.coluna)
    
    def quebra(self):
        """Processa uma instrução QUEBRA."""
        token = self.consumir('QUEBRA')
        return QuebraNode(token.linha, token.coluna)
    
    def continua(self):
        """Processa uma instrução CONTINUA."""
        token = self.consumir('CONTINUA')
        return ContinuaNode(token.linha, token.coluna)
    
    def passar(self):
        """Processa uma instrução PASSAR."""
        token = self.consumir('PASSAR')
        return PassarNode(token.linha, token.coluna)

def exibir_ast(no, indentacao=0, profundidade_maxima=10):
    """
    Exibe a AST de forma hierárquica e legível.
    
    Args:
        no: Nó da AST
        indentacao: Nível de indentação
        profundidade_maxima: Profundidade máxima
    """
    if indentacao > profundidade_maxima:
        print("  " * indentacao + "...")
        return
    
    prefixo = "  " * indentacao
    print(f"{prefixo}{no}")
    
    # Exibe filhos dependendo do tipo de nó
    if hasattr(no, 'declaracoes') and no.declaracoes:
        for i, decl in enumerate(no.declaracoes):
            if i < 20:  # Limita exibição
                exibir_ast(decl, indentacao + 1, profundidade_maxima)
        if len(no.declaracoes) > 20:
            print("  " * (indentacao + 1) + f"... e mais {len(no.declaracoes) - 20} declarações")
    
    elif hasattr(no, 'esquerda') and hasattr(no, 'direita'):
        if no.esquerda:
            exibir_ast(no.esquerda, indentacao + 1, profundidade_maxima)
        if no.direita:
            exibir_ast(no.direita, indentacao + 1, profundidade_maxima)
    
    elif hasattr(no, 'expressao') and no.expressao:
        exibir_ast(no.expressao, indentacao + 1, profundidade_maxima)
    
    elif hasattr(no, 'condicao') and hasattr(no, 'bloco_se'):
        print(f"{prefixo}  Condição:")
        exibir_ast(no.condicao, indentacao + 2, profundidade_maxima)
        print(f"{prefixo}  Bloco SE:")
        exibir_ast(no.bloco_se, indentacao + 2, profundidade_maxima)
        if hasattr(no, 'blocos_senaose') and no.blocos_senaose:
            for i, (cond, bloco) in enumerate(no.blocos_senaose):
                print(f"{prefixo}  SENAOSE {i+1}:")
                exibir_ast(cond, indentacao + 2, profundidade_maxima)
                exibir_ast(bloco, indentacao + 2, profundidade_maxima)
        if hasattr(no, 'bloco_senao') and no.bloco_senao:
            print(f"{prefixo}  Bloco SENAO:")
            exibir_ast(no.bloco_senao, indentacao + 2, profundidade_maxima)
    
    elif hasattr(no, 'bloco') and no.bloco:
        exibir_ast(no.bloco, indentacao + 1, profundidade_maxima)


def main():
    """Função principal para execução via linha de comando."""
    import sys
    import os
    
    # Adiciona o diretório pai ao path para imports
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    
    from src.lexer.lexer import LexerCoral
    
    if len(sys.argv) != 2:
        print("Uso: python parser.py <arquivo.crl>")
        print("\nExemplo:")
        print("  python src/parser/parser.py exemplos/parser/funcoes.crl")
        sys.exit(1)
    
    arquivo = sys.argv[1]
    
    try:
        # Lê o arquivo
        if not os.path.exists(arquivo):
            print(f"Erro: Arquivo '{arquivo}' não encontrado.")
            sys.exit(1)
        
        with open(arquivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
        
        print(f"{'='*70}")
        print(f"Arquivo: {arquivo}")
        print(f"{'='*70}")
        
        # Análise léxica
        lexer = LexerCoral.analisar_arquivo(arquivo)
        tokens = []
        while True:
            token = lexer.getNextToken()
            tokens.append(token)
            if token.tipo == "EOF":
                break
        
        # Análise sintática
        parser = ParserCoral(tokens)
        ast = parser.parse()
        
        # Exibe a AST
        print(f"\n{'='*70}")
        print(f"Árvore Sintática Abstrata (AST)")
        print(f"{'='*70}\n")
        exibir_ast(ast)
        print(f"\n{'='*70}")
        print(f"Análise concluída com sucesso!")
        print(f"{'='*70}\n")
        
    except ErroSintatico as e:
        print(f"\n{'='*70}")
        print(f"Erro Sintático")
        print(f"{'='*70}")
        print(f"{e.formatar_mensagem()}\n")
        sys.exit(1)
        
    except FileNotFoundError as e:
        print(f"\nErro: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n{'='*70}")
        print(f"Erro Inesperado")
        print(f"{'='*70}")
        print(f"{type(e).__name__}: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
