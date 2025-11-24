"""
Interpretador da Linguagem Coral.

Percorre a AST (Árvore Sintática Abstrata) e executa o código,
mantendo um ambiente de variáveis e funções.
"""

import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from src.parser.ast_nodes import *
except ModuleNotFoundError:
    from parser.ast_nodes import *


class ErroExecucao(Exception):
    """Exceção lançada durante a execução do programa."""
    def __init__(self, mensagem, linha=None, coluna=None):
        self.mensagem = mensagem
        self.linha = linha
        self.coluna = coluna
        super().__init__(self.formatar_mensagem())
    
    def formatar_mensagem(self):
        if self.linha is not None and self.coluna is not None:
            return f"Erro de execução na linha {self.linha}, coluna {self.coluna}: {self.mensagem}"
        return f"Erro de execução: {self.mensagem}"


class Ambiente:
    """Gerencia o escopo de variáveis e funções."""
    
    def __init__(self, pai=None):
        self.variaveis = {}
        self.funcoes = {}
        self.pai = pai
    
    def definir_variavel(self, nome, valor):
        """Define uma variável no escopo atual."""
        self.variaveis[nome] = valor
    
    def obter_variavel(self, nome):
        """Obtém o valor de uma variável, procurando em escopos pai se necessário."""
        if nome in self.variaveis:
            return self.variaveis[nome]
        elif self.pai:
            return self.pai.obter_variavel(nome)
        else:
            raise ErroExecucao(f"Variável '{nome}' não definida")
    
    def definir_funcao(self, nome, funcao):
        """Define uma função no escopo atual."""
        self.funcoes[nome] = funcao
    
    def obter_funcao(self, nome):
        """Obtém uma função, procurando em escopos pai se necessário."""
        if nome in self.funcoes:
            return self.funcoes[nome]
        elif self.pai:
            return self.pai.obter_funcao(nome)
        else:
            raise ErroExecucao(f"Função '{nome}' não definida")
    
    def existe_variavel(self, nome):
        """Verifica se uma variável existe."""
        return nome in self.variaveis or (self.pai and self.pai.existe_variavel(nome))


class RetornoExcecao(Exception):
    """Exceção especial para controle de fluxo de RETORNAR."""
    def __init__(self, valor):
        self.valor = valor


class QuebraExcecao(Exception):
    """Exceção especial para controle de fluxo de QUEBRA."""
    pass


class ContinuaExcecao(Exception):
    """Exceção especial para controle de fluxo de CONTINUA."""
    pass


class InterpretadorCoral:
    """Interpretador que executa a AST da linguagem Coral."""
    
    def __init__(self):
        self.ambiente_global = Ambiente()
        self.ambiente_atual = self.ambiente_global
        self._registrar_funcoes_nativas()
    
    def _mapa_tipos_python(self):
        """Mapeia tipos Coral para tipos Python."""
        return {
            'INTEIRO': int,
            'DECIMAL': float,
            'TEXTO': str,
            'BOOLEANO': bool,
            'LISTA': list,
            'DICIONARIO': dict
        }
    
    def _validar_tipo(self, valor, tipo_esperado, nome_parametro, nome_funcao):
        """Valida se o valor corresponde ao tipo esperado."""
        if tipo_esperado is None:
            return  # Sem anotação de tipo, aceita qualquer coisa
        
        mapa = self._mapa_tipos_python()
        tipo_python = mapa.get(tipo_esperado)
        
        if tipo_python is None:
            # Tipo desconhecido, ignora validação
            return
        
        if not isinstance(valor, tipo_python):
            tipo_recebido = type(valor).__name__
            # Mapeia tipos Python de volta para nomes Coral
            mapa_reverso = {
                'int': 'INTEIRO',
                'float': 'DECIMAL',
                'str': 'TEXTO',
                'bool': 'BOOLEANO',
                'list': 'LISTA',
                'dict': 'DICIONARIO'
            }
            tipo_recebido_coral = mapa_reverso.get(tipo_recebido, tipo_recebido)
            
            raise ErroExecucao(
                f"Erro de tipo na função '{nome_funcao}': "
                f"parâmetro '{nome_parametro}' espera {tipo_esperado}, "
                f"mas recebeu {tipo_recebido_coral}"
            )
    
    def _registrar_funcoes_nativas(self):
        """Registra funções nativas (built-in) da linguagem."""
        # Função ESCREVA para imprimir na tela
        self.ambiente_global.definir_funcao('ESCREVA', lambda *args: print(*args))
        # Função LER para ler entrada do usuário
        self.ambiente_global.definir_funcao('LER', lambda prompt="": input(prompt))
        # Função TIPO para obter o tipo de uma variável
        self.ambiente_global.definir_funcao('TIPO', lambda x: type(x).__name__)
        # Função TAMANHO para obter tamanho de lista/string
        self.ambiente_global.definir_funcao('TAMANHO', lambda x: len(x))
        # Função INTERVALO para gerar sequências numéricas (equivalente a range do Python)
        def intervalo(inicio, fim=None, passo=1):
            if fim is None:
                # INTERVALO(n) -> 0 até n-1
                return list(range(inicio))
            else:
                # INTERVALO(inicio, fim, passo) -> inicio até fim-1 com passo
                return list(range(inicio, fim, passo))
        self.ambiente_global.definir_funcao('INTERVALO', intervalo)
        
        # Funções de conversão de tipo
        def converter_inteiro(valor):
            """Converte texto ou número para inteiro"""
            try:
                return int(valor)
            except (ValueError, TypeError):
                raise ErroExecucao(f"Não foi possível converter '{valor}' para INTEIRO")
        
        def converter_decimal(valor):
            """Converte texto ou número para decimal (float)"""
            try:
                return float(valor)
            except (ValueError, TypeError):
                raise ErroExecucao(f"Não foi possível converter '{valor}' para DECIMAL")
        
        def converter_texto(valor):
            """Converte qualquer valor para texto"""
            return str(valor)
        
        self.ambiente_global.definir_funcao('INTEIRO', converter_inteiro)
        self.ambiente_global.definir_funcao('DECIMAL', converter_decimal)
        self.ambiente_global.definir_funcao('TEXTO', converter_texto)
    
    def interpretar(self, ast):
        """
        Interpreta a AST completa.
        
        Args:
            ast: ProgramaNode - raiz da AST
        """
        try:
            self.visitar(ast)
        except ErroExecucao as e:
            print(f"\n{e.formatar_mensagem()}")
            sys.exit(1)
    
    def visitar(self, no):
        """Visita um nó da AST e executa a ação apropriada."""
        nome_metodo = f'visitar_{type(no).__name__}'
        metodo = getattr(self, nome_metodo, self.visitar_generico)
        return metodo(no)
    
    def visitar_generico(self, no):
        """Método chamado quando não há implementação específica."""
        raise ErroExecucao(f"Nó '{type(no).__name__}' não implementado no interpretador")
    
    def visitar_ProgramaNode(self, no):
        """Executa o programa completo."""
        for declaracao in no.declaracoes:
            self.visitar(declaracao)
    
    def visitar_LiteralNode(self, no):
        """Retorna o valor literal, processando interpolação de strings se necessário."""
        valor = no.valor
        
        # Se for string formatada (f"string"), processa interpolação {variavel}
        if isinstance(valor, str) and hasattr(no, 'formatada') and no.formatada:
            valor = self._processar_interpolacao(valor)
        
        return valor
    
    def _processar_interpolacao(self, texto):
        """Processa interpolação de variáveis/expressões em strings usando {expressao}."""
        import re
        
        # Encontra todas as ocorrências de {expressao}
        def substituir(match):
            expressao_str = match.group(1)
            try:
                # Parse e avalia a expressão
                from src.lexer.lexer import LexerCoral
                from src.parser.parser import ParserCoral
                
                # Analisa a expressão
                lexer = LexerCoral.analisar_string(expressao_str)
                tokens = []
                while True:
                    token = lexer.getNextToken()
                    tokens.append(token)
                    if token.tipo == "EOF":
                        break
                
                # Parse como expressão
                parser = ParserCoral(tokens)
                # Usa o método interno para parsear apenas uma expressão
                expressao_node = parser.expressao()
                
                # Avalia a expressão
                valor = self.visitar(expressao_node)
                return str(valor)
            except:
                # Se falhar, mantém o texto original
                return match.group(0)
        
        # Substitui {expressao} pelos valores (captura tudo entre { e })
        texto_interpolado = re.sub(r'\{([^}]+)\}', substituir, texto)
        return texto_interpolado
    
    def visitar_IdentificadorNode(self, no):
        """Retorna o valor da variável."""
        return self.ambiente_atual.obter_variavel(no.nome)
    
    def visitar_AcessoAtributoNode(self, no):
        """Retorna o valor de um atributo de um objeto."""
        objeto = self.visitar(no.objeto)
        
        # Se for instância de classe
        if isinstance(objeto, InstanciaClasse):
            return objeto.obter_atributo(no.atributo)
        
        # Tenta acessar atributo Python nativo (para compatibilidade)
        try:
            return getattr(objeto, no.atributo)
        except AttributeError:
            raise ErroExecucao(f"Objeto não possui atributo '{no.atributo}'")
    
    def visitar_AtribuicaoNode(self, no):
        """Executa uma atribuição de variável ou atributo."""
        valor = self.visitar(no.expressao)
        
        # Se é atribuição a elemento de lista/dict: lista[0] = valor
        if type(no.identificador).__name__ == 'IndexacaoNode':
            alvo = no.identificador
            
            # Obtem o objeto base (precisa ser uma referência, não cópia)
            if type(alvo.objeto).__name__ == 'IdentificadorNode':
                # Acessa diretamente a variável no ambiente
                nome_var = alvo.objeto.nome
                objeto = self.ambiente_atual.obter_variavel(nome_var)
            elif type(alvo.objeto).__name__ == 'IndexacaoNode':
                # Indexação encadeada: matriz[0][1]
                objeto = self.visitar(alvo.objeto)
            else:
                objeto = self.visitar(alvo.objeto)
            
            indice = self.visitar(alvo.indice)
            
            if no.operador == '=':
                objeto[indice] = valor
            else:
                # Operadores compostos: +=, -=, etc
                valor_atual = objeto[indice]
                if no.operador == '+=':
                    objeto[indice] = valor_atual + valor
                elif no.operador == '-=':
                    objeto[indice] = valor_atual - valor
                elif no.operador == '*=':
                    objeto[indice] = valor_atual * valor
                elif no.operador == '/=':
                    objeto[indice] = valor_atual / valor
                elif no.operador == '%=':
                    objeto[indice] = valor_atual % valor
            return
        
        # Se é atribuição a atributo: self.nome = valor
        if type(no.identificador).__name__ == 'AcessoAtributoNode':
            alvo = no.identificador
            objeto = self.visitar(alvo.objeto)
            
            if isinstance(objeto, InstanciaClasse):
                if no.operador == '=':
                    objeto.definir_atributo(alvo.atributo, valor)
                else:
                    # Operadores compostos: +=, -=, etc
                    valor_atual = objeto.obter_atributo(alvo.atributo)
                    if no.operador == '+=':
                        objeto.definir_atributo(alvo.atributo, valor_atual + valor)
                    elif no.operador == '-=':
                        objeto.definir_atributo(alvo.atributo, valor_atual - valor)
                    elif no.operador == '*=':
                        objeto.definir_atributo(alvo.atributo, valor_atual * valor)
                    elif no.operador == '/=':
                        objeto.definir_atributo(alvo.atributo, valor_atual / valor)
                    elif no.operador == '%=':
                        objeto.definir_atributo(alvo.atributo, valor_atual % valor)
            else:
                raise ErroExecucao(f"Não é possível atribuir atributo a este tipo de objeto")
            return
        
        # Atribuição normal a variável
        if type(no.identificador).__name__ == 'IdentificadorNode':
            nome = no.identificador.nome
        else:
            nome = no.identificador
            
        # Operadores de atribuição composta
        if no.operador == '=':
            self.ambiente_atual.definir_variavel(nome, valor)
        elif no.operador == '+=':
            valor_atual = self.ambiente_atual.obter_variavel(nome)
            self.ambiente_atual.definir_variavel(nome, valor_atual + valor)
        elif no.operador == '-=':
            valor_atual = self.ambiente_atual.obter_variavel(nome)
            self.ambiente_atual.definir_variavel(nome, valor_atual - valor)
        elif no.operador == '*=':
            valor_atual = self.ambiente_atual.obter_variavel(nome)
            self.ambiente_atual.definir_variavel(nome, valor_atual * valor)
        elif no.operador == '/=':
            valor_atual = self.ambiente_atual.obter_variavel(nome)
            self.ambiente_atual.definir_variavel(nome, valor_atual / valor)
        elif no.operador == '%=':
            valor_atual = self.ambiente_atual.obter_variavel(nome)
            self.ambiente_atual.definir_variavel(nome, valor_atual % valor)
    
    def visitar_ExpressaoBinariaNode(self, no):
        """Executa uma expressão binária."""
        esquerda = self.visitar(no.esquerda)
        direita = self.visitar(no.direita)
        operador = no.operador.lexema
        
        # Operadores aritméticos
        if operador == '+':
            return esquerda + direita
        elif operador == '-':
            return esquerda - direita
        elif operador == '*':
            return esquerda * direita
        elif operador == '/':
            if direita == 0:
                raise ErroExecucao("Divisão por zero", no.linha, no.coluna)
            return esquerda / direita
        elif operador == '%':
            return esquerda % direita
        elif operador == '**':
            return esquerda ** direita
        
        # Operadores relacionais
        elif operador == '==':
            return esquerda == direita
        elif operador == '!=':
            return esquerda != direita
        elif operador == '<':
            return esquerda < direita
        elif operador == '>':
            return esquerda > direita
        elif operador == '<=':
            return esquerda <= direita
        elif operador == '>=':
            return esquerda >= direita
        
        # Operadores lógicos
        elif operador == 'E':
            return esquerda and direita
        elif operador == 'OU':
            return esquerda or direita
        
        else:
            raise ErroExecucao(f"Operador '{operador}' não reconhecido", no.linha, no.coluna)
    
    def visitar_ExpressaoUnariaNode(self, no):
        """Executa uma expressão unária."""
        operador = no.operador.lexema
        expressao = self.visitar(no.expressao)
        
        if operador == '-':
            return -expressao
        elif operador == 'NAO':
            return not expressao
        else:
            raise ErroExecucao(f"Operador unário '{operador}' não reconhecido", no.linha, no.coluna)
    
    def visitar_ChamadaFuncaoNode(self, no):
        """Executa uma chamada de função ou método."""
        # Avalia os argumentos
        argumentos = [self.visitar(arg) for arg in no.argumentos]
        
        # Se for chamada de método: obj.metodo()
        # Usa type().__name__ para evitar problemas com múltiplos imports do mesmo módulo
        if type(no.nome).__name__ == 'AcessoAtributoNode':
            metodo = self.visitar(no.nome)
            
            # Se for método vinculado
            if isinstance(metodo, MetodoVinculado):
                return metodo(*argumentos)
            
            # Se for função/método callable
            if callable(metodo):
                return metodo(*argumentos)
            
            raise ErroExecucao(f"'{no.nome.atributo}' não é um método válido")
        
        # Chamada de função normal ou construtor de classe
        nome_funcao = no.nome
        
        # Primeiro tenta buscar como função
        try:
            funcao = self.ambiente_atual.obter_funcao(nome_funcao)
        except ErroExecucao:
            # Se não encontrou como função, tenta como variável (pode ser classe)
            try:
                funcao = self.ambiente_atual.obter_variavel(nome_funcao)
            except ErroExecucao:
                raise ErroExecucao(f"'{nome_funcao}' não está definido", no.linha, no.coluna)
        
        # Se for função nativa (Python) ou classe
        if callable(funcao) and not isinstance(funcao, FuncaoNode):
            return funcao(*argumentos)
        
        # Se for função definida pelo usuário
        if isinstance(funcao, FuncaoNode):
            return self._executar_funcao_usuario(funcao, argumentos)
        
        raise ErroExecucao(f"'{nome_funcao}' não é uma função válida", no.linha, no.coluna)
    
    def _executar_funcao_usuario(self, funcao, argumentos):
        """Executa uma função definida pelo usuário."""
        # Verifica número de argumentos
        params_obrigatorios = [p for p in funcao.parametros if p.valor_padrao is None]
        if len(argumentos) < len(params_obrigatorios):
            raise ErroExecucao(
                f"Função '{funcao.nome}' espera {len(params_obrigatorios)} argumentos, "
                f"mas recebeu {len(argumentos)}"
            )
        
        # Cria novo ambiente para a função
        ambiente_funcao = Ambiente(self.ambiente_global)
        
        # Vincula parâmetros aos argumentos
        for i, parametro in enumerate(funcao.parametros):
            if i < len(argumentos):
                # VALIDAÇÃO DE TIPOS
                self._validar_tipo(
                    argumentos[i], 
                    parametro.tipo_anotacao, 
                    parametro.nome, 
                    funcao.nome
                )
                ambiente_funcao.definir_variavel(parametro.nome, argumentos[i])
            elif parametro.valor_padrao is not None:
                # Usa valor padrão
                ambiente_anterior = self.ambiente_atual
                self.ambiente_atual = ambiente_funcao
                valor_padrao = self.visitar(parametro.valor_padrao)
                self.ambiente_atual = ambiente_anterior
                ambiente_funcao.definir_variavel(parametro.nome, valor_padrao)
        
        # Executa o corpo da função
        ambiente_anterior = self.ambiente_atual
        self.ambiente_atual = ambiente_funcao
        
        try:
            self.visitar(funcao.bloco)
            retorno = None  # Função sem retorno explícito retorna None
        except RetornoExcecao as e:
            retorno = e.valor
        finally:
            self.ambiente_atual = ambiente_anterior
        
        # VALIDAÇÃO DO TIPO DE RETORNO
        if funcao.tipo_retorno is not None and retorno is not None:
            self._validar_tipo(
                retorno,
                funcao.tipo_retorno,
                'retorno',
                funcao.nome
            )
        
        return retorno
    
    def visitar_FuncaoNode(self, no):
        """Define uma função."""
        self.ambiente_atual.definir_funcao(no.nome, no)
    
    def visitar_BlocoNode(self, no):
        """Executa um bloco de declarações."""
        for declaracao in no.declaracoes:
            self.visitar(declaracao)
    
    def visitar_SeNode(self, no):
        """Executa uma estrutura condicional SE/SENAOSE/SENAO."""
        # Testa a condição principal
        if self.visitar(no.condicao):
            self.visitar(no.bloco_se)
            return
        
        # Testa os SENAOSE
        for condicao, bloco in no.blocos_senaose:
            if self.visitar(condicao):
                self.visitar(bloco)
                return
        
        # Executa o SENAO se existir
        if no.bloco_senao:
            self.visitar(no.bloco_senao)
    
    def visitar_EnquantoNode(self, no):
        """Executa um laço ENQUANTO."""
        try:
            while self.visitar(no.condicao):
                try:
                    self.visitar(no.bloco)
                except ContinuaExcecao:
                    continue
        except QuebraExcecao:
            pass
    
    def visitar_ParaNode(self, no):
        """Executa um laço PARA."""
        iteravel = self.visitar(no.iteravel)
        nome_variavel = no.variavel.nome
        
        try:
            for valor in iteravel:
                self.ambiente_atual.definir_variavel(nome_variavel, valor)
                try:
                    self.visitar(no.bloco)
                except ContinuaExcecao:
                    continue
        except QuebraExcecao:
            pass
    
    def visitar_RetornarNode(self, no):
        """Executa um RETORNAR."""
        valor = None
        if no.expressao:
            valor = self.visitar(no.expressao)
        raise RetornoExcecao(valor)
    
    def visitar_QuebraNode(self, no):
        """Executa um QUEBRA."""
        raise QuebraExcecao()
    
    def visitar_ContinuaNode(self, no):
        """Executa um CONTINUA."""
        raise ContinuaExcecao()
    
    def visitar_PassarNode(self, no):
        """Executa um PASSAR (não faz nada)."""
        pass
    
    def visitar_ListaNode(self, no):
        """Cria uma lista."""
        return [self.visitar(elemento) for elemento in no.elementos]
    
    def visitar_IndexacaoNode(self, no):
        """Acessa elemento de lista ou dicionário por índice."""
        objeto = self.visitar(no.objeto)
        indice = self.visitar(no.indice)
        
        try:
            return objeto[indice]
        except (IndexError, KeyError, TypeError) as e:
            raise ErroExecucao(
                f"Erro ao acessar índice: {str(e)}",
                no.linha,
                no.coluna
            )
    
    def visitar_DicionarioNode(self, no):
        """Cria um dicionário."""
        resultado = {}
        for chave_no, valor_no in no.pares:
            chave = self.visitar(chave_no)
            valor = self.visitar(valor_no)
            resultado[chave] = valor
        return resultado
    
    def visitar_ClasseNode(self, no):
        """Define uma classe."""
        classe = ClasseCoral(no.nome, no.bloco, self)
        self.ambiente_atual.definir_variavel(no.nome, classe)


class ClasseCoral:
    """Representa uma classe definida pelo usuário."""
    
    def __init__(self, nome, bloco, interpretador):
        self.nome = nome
        self.bloco = bloco
        self.interpretador = interpretador
        self.metodos = {}
        self._extrair_metodos()
    
    def _extrair_metodos(self):
        """Extrai métodos do bloco da classe."""
        for declaracao in self.bloco.declaracoes:
            if isinstance(declaracao, FuncaoNode):
                self.metodos[declaracao.nome] = declaracao
    
    def __call__(self, *args, **kwargs):
        """Permite instanciar a classe como: obj = MinhaClasse()"""
        instancia = InstanciaClasse(self)
        
        # Chama __construtor__ se existir
        if '__construtor__' in self.metodos:
            construtor = self.metodos['__construtor__']
            # Cria ambiente para o construtor
            ambiente_construtor = Ambiente(self.interpretador.ambiente_global)
            ambiente_construtor.definir_variavel('self', instancia)
            
            # Vincula parâmetros
            for i, parametro in enumerate(construtor.parametros):
                if i < len(args):
                    ambiente_construtor.definir_variavel(parametro.nome, args[i])
            
            # Executa o corpo do construtor
            ambiente_anterior = self.interpretador.ambiente_atual
            self.interpretador.ambiente_atual = ambiente_construtor
            try:
                self.interpretador.visitar(construtor.bloco)
            except RetornoExcecao:
                pass  # Construtor não deve retornar valor
            finally:
                self.interpretador.ambiente_atual = ambiente_anterior
        
        return instancia


class InstanciaClasse:
    """Representa uma instância de uma classe."""
    
    def __init__(self, classe):
        self.classe = classe
        self.atributos = {}
    
    def obter_atributo(self, nome):
        """Obtém um atributo ou método da instância."""
        if nome in self.atributos:
            return self.atributos[nome]
        elif nome in self.classe.metodos:
            # Retorna método vinculado à instância
            return MetodoVinculado(self, self.classe.metodos[nome])
        else:
            raise ErroExecucao(f"Atributo '{nome}' não encontrado")
    
    def definir_atributo(self, nome, valor):
        """Define um atributo da instância."""
        self.atributos[nome] = valor


class MetodoVinculado:
    """Representa um método vinculado a uma instância."""
    
    def __init__(self, instancia, metodo):
        self.instancia = instancia
        self.metodo = metodo
    
    def __call__(self, *args):
        """Executa o método com 'self' automaticamente vinculado."""
        interpretador = self.instancia.classe.interpretador
        ambiente_metodo = Ambiente(interpretador.ambiente_global)
        ambiente_metodo.definir_variavel('self', self.instancia)
        
        # Vincula parâmetros
        for i, parametro in enumerate(self.metodo.parametros):
            if i < len(args):
                ambiente_metodo.definir_variavel(parametro.nome, args[i])
        
        # Executa o método
        ambiente_anterior = interpretador.ambiente_atual
        interpretador.ambiente_atual = ambiente_metodo
        try:
            interpretador.visitar(self.metodo.bloco)
            retorno = None
        except RetornoExcecao as e:
            retorno = e.valor
        finally:
            interpretador.ambiente_atual = ambiente_anterior
        
        return retorno


def executar_programa(ast, exibir_mensagem=True):
    """Executa um programa Coral a partir da AST."""
    if exibir_mensagem:
        print(f"{'='*70}")
        print(f"Executando Programa Coral")
        print(f"{'='*70}\n")
    
    interpretador = InterpretadorCoral()
    interpretador.interpretar(ast)
    
    if exibir_mensagem:
        print(f"\n{'='*70}")
        print(f"Programa executado com sucesso!")
        print(f"{'='*70}")
