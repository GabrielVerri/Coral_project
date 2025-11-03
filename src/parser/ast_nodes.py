"""
Nós da Árvore Sintática Abstrata (AST) para a linguagem Coral.

Cada classe representa um nó da AST correspondente a uma construção
sintática da linguagem.
"""

class ASTNode:
    """Classe base para todos os nós da AST."""
    def __init__(self, linha=None, coluna=None):
        self.linha = linha
        self.coluna = coluna
    
    def __repr__(self):
        return f"{self.__class__.__name__}()"


class ProgramaNode(ASTNode):
    """Nó raiz do programa - contém lista de declarações."""
    def __init__(self, declaracoes):
        super().__init__()
        self.declaracoes = declaracoes
    
    def __repr__(self):
        return f"Programa({len(self.declaracoes)} declarações)"


class DeclaracaoNode(ASTNode):
    """Classe base para declarações (expressões, estruturas, funções, classes)."""
    pass


class ExpressaoNode(DeclaracaoNode):
    """Classe base para expressões."""
    pass


class ExpressaoBinariaNode(ExpressaoNode):
    """Expressão binária (ex: a + b, x == y)."""
    def __init__(self, esquerda, operador, direita, linha=None, coluna=None):
        super().__init__(linha, coluna)
        self.esquerda = esquerda
        self.operador = operador
        self.direita = direita
    
    def __repr__(self):
        return f"ExpBinaria({self.esquerda} {self.operador.lexema} {self.direita})"


class ExpressaoUnariaNode(ExpressaoNode):
    """Expressão unária (ex: -x, NAO condicao)."""
    def __init__(self, operador, expressao, linha=None, coluna=None):
        super().__init__(linha, coluna)
        self.operador = operador
        self.expressao = expressao
    
    def __repr__(self):
        return f"ExpUnaria({self.operador.lexema} {self.expressao})"


class LiteralNode(ExpressaoNode):
    """Literal (número, string, booleano)."""
    def __init__(self, valor, tipo, linha=None, coluna=None):
        super().__init__(linha, coluna)
        self.valor = valor
        self.tipo = tipo
    
    def __repr__(self):
        return f"Literal({self.valor}:{self.tipo})"


class IdentificadorNode(ExpressaoNode):
    """Identificador (variável)."""
    def __init__(self, nome, linha=None, coluna=None):
        super().__init__(linha, coluna)
        self.nome = nome
    
    def __repr__(self):
        return f"Id({self.nome})"


class AtribuicaoNode(DeclaracaoNode):
    """Atribuição (ex: x = 10, y += 5)."""
    def __init__(self, identificador, operador, expressao, linha=None, coluna=None):
        super().__init__(linha, coluna)
        self.identificador = identificador
        self.operador = operador
        self.expressao = expressao
    
    def __repr__(self):
        return f"Atribuicao({self.identificador} {self.operador} {self.expressao})"


class SeNode(DeclaracaoNode):
    """Estrutura condicional SE."""
    def __init__(self, condicao, bloco_se, blocos_senaose, bloco_senao, linha=None, coluna=None):
        super().__init__(linha, coluna)
        self.condicao = condicao
        self.bloco_se = bloco_se
        self.blocos_senaose = blocos_senaose or []
        self.bloco_senao = bloco_senao
    
    def __repr__(self):
        return f"Se(senaose={len(self.blocos_senaose)}, senao={self.bloco_senao is not None})"


class EnquantoNode(DeclaracaoNode):
    """Laço ENQUANTO."""
    def __init__(self, condicao, bloco, linha=None, coluna=None):
        super().__init__(linha, coluna)
        self.condicao = condicao
        self.bloco = bloco
    
    def __repr__(self):
        return f"Enquanto({self.condicao})"


class ParaNode(DeclaracaoNode):
    """Laço PARA."""
    def __init__(self, variavel, iteravel, bloco, linha=None, coluna=None):
        super().__init__(linha, coluna)
        self.variavel = variavel
        self.iteravel = iteravel
        self.bloco = bloco
    
    def __repr__(self):
        return f"Para({self.variavel} DENTRODE {self.iteravel})"


class BlocoNode(ASTNode):
    """Bloco de código (conjunto de declarações indentadas)."""
    def __init__(self, declaracoes, linha=None, coluna=None):
        super().__init__(linha, coluna)
        self.declaracoes = declaracoes
    
    def __repr__(self):
        return f"Bloco({len(self.declaracoes)} declarações)"


class FuncaoNode(DeclaracaoNode):
    """Definição de função."""
    def __init__(self, nome, parametros, bloco, linha=None, coluna=None):
        super().__init__(linha, coluna)
        self.nome = nome
        self.parametros = parametros
        self.bloco = bloco
    
    def __repr__(self):
        return f"Funcao({self.nome}, {len(self.parametros)} params)"


class ParametroNode(ASTNode):
    """Parâmetro de função."""
    def __init__(self, nome, valor_padrao=None, linha=None, coluna=None):
        super().__init__(linha, coluna)
        self.nome = nome
        self.valor_padrao = valor_padrao
    
    def __repr__(self):
        return f"Param({self.nome})"


class ChamadaFuncaoNode(ExpressaoNode):
    """Chamada de função."""
    def __init__(self, nome, argumentos, linha=None, coluna=None):
        super().__init__(linha, coluna)
        self.nome = nome
        self.argumentos = argumentos
    
    def __repr__(self):
        return f"Chamada({self.nome}, {len(self.argumentos)} args)"


class RetornarNode(DeclaracaoNode):
    """Comando RETORNAR."""
    def __init__(self, expressao=None, linha=None, coluna=None):
        super().__init__(linha, coluna)
        self.expressao = expressao
    
    def __repr__(self):
        return f"Retornar({self.expressao})"


class ClasseNode(DeclaracaoNode):
    """Definição de classe."""
    def __init__(self, nome, bloco, linha=None, coluna=None):
        super().__init__(linha, coluna)
        self.nome = nome
        self.bloco = bloco
    
    def __repr__(self):
        return f"Classe({self.nome})"


class ListaNode(ExpressaoNode):
    """Lista literal [1, 2, 3]."""
    def __init__(self, elementos, linha=None, coluna=None):
        super().__init__(linha, coluna)
        self.elementos = elementos
    
    def __repr__(self):
        return f"Lista({len(self.elementos)} elementos)"


class DicionarioNode(ExpressaoNode):
    """Dicionário literal {"chave": valor}."""
    def __init__(self, pares, linha=None, coluna=None):
        super().__init__(linha, coluna)
        self.pares = pares
    
    def __repr__(self):
        return f"Dicionario({len(self.pares)} pares)"


class TuplaNode(ExpressaoNode):
    """Tupla literal (1, 2, 3)."""
    def __init__(self, elementos, linha=None, coluna=None):
        super().__init__(linha, coluna)
        self.elementos = elementos
    
    def __repr__(self):
        return f"Tupla({len(self.elementos)} elementos)"


class QuebraNode(DeclaracaoNode):
    """Comando QUEBRA (break)."""
    def __init__(self, linha=None, coluna=None):
        super().__init__(linha, coluna)
    
    def __repr__(self):
        return "Quebra()"


class ContinuaNode(DeclaracaoNode):
    """Comando CONTINUA (continue)."""
    def __init__(self, linha=None, coluna=None):
        super().__init__(linha, coluna)
    
    def __repr__(self):
        return "Continua()"


class PassarNode(DeclaracaoNode):
    """Comando PASSAR (pass)."""
    def __init__(self, linha=None, coluna=None):
        super().__init__(linha, coluna)
    
    def __repr__(self):
        return "Passar()"


class AcessoAtributoNode(ExpressaoNode):
    """Acesso a atributo (obj.attr)."""
    def __init__(self, objeto, atributo, linha=None, coluna=None):
        super().__init__(linha, coluna)
        self.objeto = objeto
        self.atributo = atributo
    
    def __repr__(self):
        return f"Acesso({self.objeto}.{self.atributo})"


class IndexacaoNode(ExpressaoNode):
    """Indexação (lista[0], dict["chave"])."""
    def __init__(self, objeto, indice, linha=None, coluna=None):
        super().__init__(linha, coluna)
        self.objeto = objeto
        self.indice = indice
    
    def __repr__(self):
        return f"Indexacao({self.objeto}[{self.indice}])"
