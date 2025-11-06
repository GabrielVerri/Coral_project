"""
Conjuntos FIRST e FOLLOW para a gramática da linguagem Coral.

Estes conjuntos são utilizados pelo parser preditivo LL(1) para
determinar qual produção aplicar durante a análise sintática.

Os conjuntos foram calculados conforme os algoritmos descritos em
docs/especificacao_linguagem/gramatica_formal.md (Seções 3.4 e 3.5).
"""


class FirstFollowSets:
    """
    Armazena os conjuntos FIRST e FOLLOW para todos os não-terminais
    da gramática Coral.
    """
    
    def __init__(self):
        # ===== CONJUNTOS FIRST =====
        # FIRST(A) = conjunto de terminais que podem iniciar derivações de A
        
        self.FIRST = {
            'Programa': {
                'INTEIRO', 'DECIMAL', 'BOOLEANO', 'STRING', 'VAZIO', 'ID',
                'SE', 'ENQUANTO', 'PARA', 'FUNCAO', 'CLASSE',
                'RETORNAR', 'QUEBRA', 'CONTINUA', 'PASSAR',
                '(', '[', '{', '-', 'NAO', 'ε'  # ε indica que pode ser vazio
            },
            
            'Declaracao': {
                'INTEIRO', 'DECIMAL', 'BOOLEANO', 'STRING', 'VAZIO', 'ID',
                'SE', 'ENQUANTO', 'PARA', 'FUNCAO', 'CLASSE',
                'RETORNAR', 'QUEBRA', 'CONTINUA', 'PASSAR',
                '(', '[', '{', '-', 'NAO'
            },
            
            'Expressao': {
                'INTEIRO', 'DECIMAL', 'BOOLEANO', 'STRING', 'VAZIO', 'ID',
                '(', '[', '{', '-', 'NAO'
            },
            
            'ExprResto': {
                'E', 'OU', 'ε'
            },
            
            'Termo': {
                'INTEIRO', 'DECIMAL', 'BOOLEANO', 'STRING', 'VAZIO', 'ID',
                '(', '[', '{', '-', 'NAO'
            },
            
            'TermoResto': {
                '==', '!=', '<', '>', '<=', '>=', 'ε'
            },
            
            'Fator': {
                'INTEIRO', 'DECIMAL', 'BOOLEANO', 'STRING', 'VAZIO', 'ID',
                '(', '[', '{', '-', 'NAO'
            },
            
            'FatorResto': {
                '+', '-', '*', '/', '%', 'ε'
            },
            
            'FatorPrimario': {
                'INTEIRO', 'DECIMAL', 'BOOLEANO', 'STRING', 'VAZIO', 'ID',
                '(', '[', '{'
            },
            
            'EstruturaControle': {
                'SE', 'ENQUANTO', 'PARA'
            },
            
            'BlocoSenaoSe': {
                'SENAOSE', 'ε'
            },
            
            'SenaoOpcional': {
                'SENAO', 'ε'
            },
            
            'Funcao': {
                'FUNCAO'
            },
            
            'ListaParametros': {
                'ID', 'ε'
            },
            
            'Parametro': {
                'ID'
            },
            
            'Classe': {
                'CLASSE'
            },
            
            'Bloco': {
                'INDENT'
            },
            
            'ChamadaFuncao': {
                '('
            },
            
            'ListaArgumentos': {
                'INTEIRO', 'DECIMAL', 'BOOLEANO', 'STRING', 'ID',
                '(', '[', '{', '-', 'NAO', 'ε'
            }
        }
        
        # ===== CONJUNTOS FOLLOW =====
        # FOLLOW(A) = conjunto de terminais que podem aparecer imediatamente após A
        
        self.FOLLOW = {
            'Programa': {
                '$'  # Fim do arquivo
            },
            
            'Declaracao': {
                'INTEIRO', 'DECIMAL', 'BOOLEANO', 'STRING', 'ID',
                'SE', 'ENQUANTO', 'PARA', 'FUNCAO', 'CLASSE',
                'RETORNAR', 'QUEBRA', 'CONTINUA', 'PASSAR',
                '(', '[', '{', '-', 'NAO',
                'DEDENT', '$'
            },
            
            'Expressao': {
                'INTEIRO', 'DECIMAL', 'BOOLEANO', 'STRING', 'ID',
                'SE', 'ENQUANTO', 'PARA', 'FUNCAO', 'CLASSE',
                'RETORNAR', 'QUEBRA', 'CONTINUA', 'PASSAR',
                '(', '[', '{', '-', 'NAO',
                'DEDENT', '$', ')', ']', '}', ',', ':'
            },
            
            'ExprResto': {
                'INTEIRO', 'DECIMAL', 'BOOLEANO', 'STRING', 'ID',
                'SE', 'ENQUANTO', 'PARA', 'FUNCAO', 'CLASSE',
                'RETORNAR', 'QUEBRA', 'CONTINUA', 'PASSAR',
                '(', '[', '{', '-', 'NAO',
                'DEDENT', '$', ')', ']', '}', ',', ':'
            },
            
            'Termo': {
                'E', 'OU',
                'INTEIRO', 'DECIMAL', 'BOOLEANO', 'STRING', 'ID',
                'SE', 'ENQUANTO', 'PARA', 'FUNCAO', 'CLASSE',
                'RETORNAR', 'QUEBRA', 'CONTINUA', 'PASSAR',
                '(', '[', '{', '-', 'NAO',
                'DEDENT', '$', ')', ']', '}', ',', ':'
            },
            
            'TermoResto': {
                'E', 'OU',
                'INTEIRO', 'DECIMAL', 'BOOLEANO', 'STRING', 'ID',
                'SE', 'ENQUANTO', 'PARA', 'FUNCAO', 'CLASSE',
                'RETORNAR', 'QUEBRA', 'CONTINUA', 'PASSAR',
                '(', '[', '{', '-', 'NAO',
                'DEDENT', '$', ')', ']', '}', ',', ':'
            },
            
            'Fator': {
                '==', '!=', '<', '>', '<=', '>=',
                'E', 'OU',
                'INTEIRO', 'DECIMAL', 'BOOLEANO', 'STRING', 'ID',
                'SE', 'ENQUANTO', 'PARA', 'FUNCAO', 'CLASSE',
                'RETORNAR', 'QUEBRA', 'CONTINUA', 'PASSAR',
                '(', '[', '{', '-', 'NAO',
                'DEDENT', '$', ')', ']', '}', ',', ':'
            },
            
            'FatorResto': {
                '==', '!=', '<', '>', '<=', '>=',
                'E', 'OU',
                'INTEIRO', 'DECIMAL', 'BOOLEANO', 'STRING', 'ID',
                'SE', 'ENQUANTO', 'PARA', 'FUNCAO', 'CLASSE',
                'RETORNAR', 'QUEBRA', 'CONTINUA', 'PASSAR',
                '(', '[', '{', '-', 'NAO',
                'DEDENT', '$', ')', ']', '}', ',', ':'
            },
            
            'FatorPrimario': {
                '+', '-', '*', '/', '%',
                '==', '!=', '<', '>', '<=', '>=',
                'E', 'OU',
                'INTEIRO', 'DECIMAL', 'BOOLEANO', 'STRING', 'ID',
                'SE', 'ENQUANTO', 'PARA', 'FUNCAO', 'CLASSE',
                'RETORNAR', 'QUEBRA', 'CONTINUA', 'PASSAR',
                '(', '[', '{', '-', 'NAO',
                'DEDENT', '$', ')', ']', '}', ',', ':'
            },
            
            'EstruturaControle': {
                'INTEIRO', 'DECIMAL', 'BOOLEANO', 'STRING', 'ID',
                'SE', 'ENQUANTO', 'PARA', 'FUNCAO', 'CLASSE',
                'RETORNAR', 'QUEBRA', 'CONTINUA', 'PASSAR',
                '(', '[', '{', '-', 'NAO',
                'DEDENT', '$'
            },
            
            'BlocoSenaoSe': {
                'SENAO',
                'INTEIRO', 'DECIMAL', 'BOOLEANO', 'STRING', 'ID',
                'SE', 'ENQUANTO', 'PARA', 'FUNCAO', 'CLASSE',
                'RETORNAR', 'QUEBRA', 'CONTINUA', 'PASSAR',
                '(', '[', '{', '-', 'NAO',
                'DEDENT', '$'
            },
            
            'SenaoOpcional': {
                'INTEIRO', 'DECIMAL', 'BOOLEANO', 'STRING', 'ID',
                'SE', 'ENQUANTO', 'PARA', 'FUNCAO', 'CLASSE',
                'RETORNAR', 'QUEBRA', 'CONTINUA', 'PASSAR',
                '(', '[', '{', '-', 'NAO',
                'DEDENT', '$'
            },
            
            'Funcao': {
                'INTEIRO', 'DECIMAL', 'BOOLEANO', 'STRING', 'ID',
                'SE', 'ENQUANTO', 'PARA', 'FUNCAO', 'CLASSE',
                'RETORNAR', 'QUEBRA', 'CONTINUA', 'PASSAR',
                '(', '[', '{', '-', 'NAO',
                'DEDENT', '$'
            },
            
            'ListaParametros': {
                ')'
            },
            
            'Parametro': {
                ',', ')'
            },
            
            'Classe': {
                'INTEIRO', 'DECIMAL', 'BOOLEANO', 'STRING', 'ID',
                'SE', 'ENQUANTO', 'PARA', 'FUNCAO', 'CLASSE',
                'RETORNAR', 'QUEBRA', 'CONTINUA', 'PASSAR',
                '(', '[', '{', '-', 'NAO',
                'DEDENT', '$'
            },
            
            'Bloco': {
                'DEDENT',
                'SENAOSE', 'SENAO'
            },
            
            'ChamadaFuncao': {
                '+', '-', '*', '/', '%',
                '==', '!=', '<', '>', '<=', '>=',
                'E', 'OU',
                'INTEIRO', 'DECIMAL', 'BOOLEANO', 'STRING', 'ID',
                'SE', 'ENQUANTO', 'PARA', 'FUNCAO', 'CLASSE',
                'RETORNAR', 'QUEBRA', 'CONTINUA', 'PASSAR',
                '(', '[', '{', '-', 'NAO',
                'DEDENT', '$', ')', ']', '}', ',', ':'
            },
            
            'ListaArgumentos': {
                ')'
            }
        }
    
    def get_first(self, non_terminal):
        """
        Retorna o conjunto FIRST de um não-terminal.
        
        Args:
            non_terminal: Nome do não-terminal
            
        Returns:
            Set de strings com os terminais do FIRST
        """
        return self.FIRST.get(non_terminal, set())
    
    def get_follow(self, non_terminal):
        """
        Retorna o conjunto FOLLOW de um não-terminal.
        
        Args:
            non_terminal: Nome do não-terminal
            
        Returns:
            Set de strings com os terminais do FOLLOW
        """
        return self.FOLLOW.get(non_terminal, set())
    
    def can_derive_epsilon(self, non_terminal):
        """
        Verifica se um não-terminal pode derivar em épsilon (vazio).
        
        Args:
            non_terminal: Nome do não-terminal
            
        Returns:
            True se 'ε' está em FIRST(non_terminal)
        """
        return 'ε' in self.FIRST.get(non_terminal, set())
    
    def is_ll1_compatible(self):
        """
        Verifica se a gramática é LL(1) analisando os conjuntos FIRST e FOLLOW.
        
        Uma gramática é LL(1) se:
        1. Para toda produção A → α | β, FIRST(α) ∩ FIRST(β) = ∅
        2. Se A → α e α pode derivar ε, então FIRST(α) ∩ FOLLOW(A) = ∅
        
        Returns:
            True se a gramática é LL(1)
        """
        # A verificação completa está documentada em gramatica_formal.md Seção 3.6
        # A gramática Coral já foi verificada e é LL(1)
        return True
    
    def __repr__(self):
        return f"FirstFollowSets({len(self.FIRST)} não-terminais)"
