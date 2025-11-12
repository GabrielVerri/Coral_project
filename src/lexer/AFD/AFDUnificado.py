class AFDUnificado:
    """AFD unificado que reconhece todos os tokens da linguagem Coral."""
    
    def __init__(self, conversor):
        self.tabela_transicoes = conversor.get_tabela_transicoes_afd()
        self.estados_aceitacao = conversor.get_estados_aceitacao_afd()
        self.estado_atual = 'Sq0'
        
    def _get_tipo_caractere(self, char):
        if char == '\n':
            return '\\n'
        if char.isalpha():
            if char in 'EOUNVFARDLS':
                return char
            return 'letra'
        elif char == '_':
            return '_'
        elif char.isdigit():
            return 'digito'
        elif char == '.':
            return '.'
        elif char in ('+', '-', '*', '/', '%', '=', '!', '<', '>', '(', ')', '{', '}', '[', ']', ',', ':', ';'):
            return char
        elif char == '#':
            return '#'
        elif char in ('"', "'"):
            return char
        elif char.isspace() and char != '\n':
            return 'espaco'
        else:
            return 'outro'

    def _is_valid_identifier_char(self, char):
        return char.isalnum() or char == '_'

    def _check_word_boundary(self, entrada, pos):
        return pos >= len(entrada) or not self._is_valid_identifier_char(entrada[pos])

    def _consume_identifier(self, entrada, start_pos):
        pos = start_pos
        while pos < len(entrada) and self._is_valid_identifier_char(entrada[pos]):
            pos += 1
        return pos
            
    def match(self, entrada):
        """Reconhece um token no início da entrada."""
        if not entrada:
            return None

        # F-strings
        if entrada.startswith('f"""') or entrada.startswith("f'''"):
            aspas = entrada[1:4]
            if len(entrada) >= 7:
                pos = entrada.find(aspas, 4)
                if pos >= 0:
                    return (entrada[:pos+3], pos+3, "STRING_MULTILINE")
        elif entrada.startswith('f"') or entrada.startswith("f'"):
            delim = entrada[1]
            pos = 2
            while pos < len(entrada):
                if entrada[pos] == '\\':
                    pos += 2
                elif entrada[pos] == delim:
                    return (entrada[:pos+1], pos+1, "STRING")
                elif entrada[pos] == '\n':
                    break  # String não fechada
                else:
                    pos += 1

        # Identificadores e palavras reservadas
        if entrada[0] == '_' or entrada[0].isalpha():
            pos = self._consume_identifier(entrada, 0)
            lexema = entrada[:pos]
            
            if lexema == "VERDADE" and self._check_word_boundary(entrada, 7):
                return ("VERDADE", 7, "BOOLEANO")
            elif lexema == "FALSO" and self._check_word_boundary(entrada, 5):
                return ("FALSO", 5, "BOOLEANO")
            elif lexema == "E" and self._check_word_boundary(entrada, 1):
                return ("E", 1, "OPERADOR_LOGICO")
            elif lexema == "OU" and self._check_word_boundary(entrada, 2):
                return ("OU", 2, "OPERADOR_LOGICO")
            elif lexema == "NAO" and self._check_word_boundary(entrada, 3):
                return ("NAO", 3, "OPERADOR_LOGICO")
            
            return (entrada[:pos], pos, "IDENTIFICADOR")
            
        # Comentários
        if entrada.startswith('#'):
            pos = entrada.find('\n')
            if pos >= 0:
                return (entrada[:pos+1], pos+1, "COMENTARIO_LINHA")
            return (entrada, len(entrada), "COMENTARIO_LINHA")
            
        # Strings multilinhas
        if entrada.startswith('"""') or entrada.startswith("'''"):
            aspas = entrada[:3]
            if len(entrada) >= 6:
                pos = entrada.find(aspas, 3)
                if pos >= 0:
                    return (entrada[:pos+3], pos+3, "STRING_MULTILINE")
        
        # Strings normais
        if entrada[0] in ('"', "'"):
            aspas = entrada[0]
            pos = entrada.find(aspas, 1)
            if pos > 0 and not '\n' in entrada[:pos]:
                return (entrada[:pos+1], pos+1, "STRING")
            return None
        
        # Números inteiros e decimais
        if entrada[0].isdigit():
            pos = 0
            while pos < len(entrada) and entrada[pos].isdigit():
                pos += 1
                
            if pos < len(entrada) and entrada[pos] == '.':
                decimal_pos = pos + 1
                if decimal_pos < len(entrada) and entrada[decimal_pos].isdigit():
                    pos = decimal_pos
                    while pos < len(entrada) and entrada[pos].isdigit():
                        pos += 1
                    if pos < len(entrada) and self._is_valid_identifier_char(entrada[pos]):
                        return None
                    return (entrada[:pos], pos, "DECIMAL")
                return None
                
            if pos < len(entrada) and self._is_valid_identifier_char(entrada[pos]):
                return None
            return (entrada[:pos], pos, "INTEIRO")
        
        # Operadores compostos
        if len(entrada) >= 2:
            dois_chars = entrada[:2]
            if dois_chars in ["==", "!=", "<=", ">="]:
                return (dois_chars, 2, "OPERADOR_RELACIONAL")
            elif dois_chars in ["++", "--", "+=", "-=", "*=", "/="]:
                return (dois_chars, 2, "OPERADOR_ATRIBUICAO")
            elif dois_chars == "**":
                return ("**", 2, "OPERADOR_ARITMETICO")
        
        # Operadores e delimitadores simples
        primeiro_char = entrada[0]
        if primeiro_char in "+-*/%=!<>(){}[],;:":
            tipo_map = {
                '+': 'OPERADOR_ARITMETICO', '-': 'OPERADOR_ARITMETICO', 
                '*': 'OPERADOR_ARITMETICO', '/': 'OPERADOR_ARITMETICO',
                '%': 'OPERADOR_ARITMETICO', '=': 'OPERADOR_ATRIBUICAO',
                '!': 'OPERADOR_RELACIONAL', '<': 'OPERADOR_RELACIONAL',
                '>': 'OPERADOR_RELACIONAL', '(': 'DELIMITADOR',
                ')': 'DELIMITADOR', '{': 'DELIMITADOR', '}': 'DELIMITADOR',
                '[': 'DELIMITADOR', ']': 'DELIMITADOR', ',': 'DELIMITADOR',
                ';': 'DELIMITADOR', ':': 'DELIMITADOR'
            }
            return (primeiro_char, 1, tipo_map.get(primeiro_char, 'OPERADOR'))
        
        # Ponto como delimitador (rejeita casos como ".5")
        if primeiro_char == '.':
            if len(entrada) > 1 and entrada[1].isdigit():
                return None
            return ('.', 1, 'DELIMITADOR')
        
        # Fallback: usa tabela de transições do AFD
        self.estado_atual = 'Sq0'
        lexema = ""
        i = 0
        ultimo_estado_aceitacao = None
        ultima_posicao_aceitacao = -1
        
        while i < len(entrada):
            char = entrada[i]
            tipo_char = self._get_tipo_caractere(char)
            
            if (self.estado_atual in self.tabela_transicoes and 
                tipo_char in self.tabela_transicoes[self.estado_atual]):
                self.estado_atual = self.tabela_transicoes[self.estado_atual][tipo_char]
                lexema += char
                
                if self.estado_atual in self.estados_aceitacao:
                    ultimo_estado_aceitacao = self.estado_atual
                    ultima_posicao_aceitacao = i + 1
                
                i += 1
            else:
                break
        
        if ultimo_estado_aceitacao is not None:
            return (entrada[:ultima_posicao_aceitacao], 
                   ultima_posicao_aceitacao, 
                   self.estados_aceitacao[ultimo_estado_aceitacao])
        
        return None