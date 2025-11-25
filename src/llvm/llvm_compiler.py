"""
Compilador LLVM IR para Coral.

Converte AST de Coral para LLVM IR.
Suporta:
- Variáveis inteiras
- Operações aritméticas básicas (+, -, *, /, %)
- Operadores relacionais (<, >, <=, >=, ==, !=)
- Operadores lógicos (E, OU, NAO)
- Atribuições
- Estruturas de decisão (SE, SENAO, SENAOSE)
- Loops (ENQUANTO, PARA com INTERVALO)
- Função ESCREVA para output
- Funções definidas pelo usuário (declaração, parâmetros, retorno, chamadas)
- Instrução RETORNAR
"""

import sys
import os

# Adiciona src ao path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from parser.ast_nodes import *


class LLVMCompiler:
    """Compilador de AST Coral para LLVM IR."""
    
    def __init__(self):
        self.output = []
        self.indent_level = 0
        self.temp_counter = 0
        self.label_counter = 0  # Para labels de blocos básicos
        self.var_map = {}  # Mapeia nomes de variáveis para registradores LLVM
        self.string_counter = 0
        self.strings = {}  # Mapeia strings para constantes globais
        self.functions = {}  # Mapeia nomes de funções para seus tipos/assinaturas
        self.current_function = None  # Nome da função sendo compilada
        self.function_params = {}  # Parâmetros da função atual
        
    def compile(self, ast):
        """
        Compila a AST para LLVM IR.
        
        Args:
            ast: Nó raiz da AST (ProgramaNode)
            
        Returns:
            String contendo o código LLVM IR
        """
        self.output = []
        self.temp_counter = 0
        self.label_counter = 0
        self.var_map = {}
        self.string_counter = 0
        self.strings = {}
        self.functions = {}
        self.current_function = None
        self.function_params = {}
        
        # Cabeçalho LLVM
        self._emit_header()
        
        # Processa o programa
        if type(ast).__name__ == 'ProgramaNode':
            # Primeira passada: coleta strings e funções
            self._collect_strings(ast)
            
            # Emite declarações de strings globais
            self._emit_string_declarations()
            
            # Emite declarações de funções externas (printf)
            self._emit_external_declarations()
            
            # Segunda passada: separa funções do código principal
            funcoes = []
            codigo_principal = []
            
            for decl in ast.declaracoes:
                if type(decl).__name__ == 'FuncaoNode':
                    funcoes.append(decl)
                else:
                    codigo_principal.append(decl)
            
            # Compila funções definidas pelo usuário
            for funcao in funcoes:
                self._compile_funcao(funcao)
            
            # Função main (código principal)
            self._emit_line("define i32 @main() {")
            self.indent_level += 1
            self.current_function = 'main'
            self._emit_line("entry:")
            self.indent_level += 1
            
            # Processa declarações do código principal
            for decl in codigo_principal:
                self._compile_node(decl)
            
            # Retorno da main
            self._emit_line("ret i32 0")
            self.indent_level -= 2
            self._emit_line("}")
            self.current_function = None
        
        return '\n'.join(self.output)
    
    def _emit_header(self):
        """Emite o cabeçalho do arquivo LLVM IR."""
        self._emit_line("; Código LLVM IR gerado pelo Coral Compiler")
        self._emit_line("; Linguagem Coral - https://github.com/GabrielVerri/Coral_project")
        self._emit_line("")
        self._emit_line("target triple = \"x86_64-pc-windows-msvc\"")
        self._emit_line("")
    
    def _emit_external_declarations(self):
        """Emite declarações de funções externas."""
        self._emit_line("; Declarações de funções externas")
        self._emit_line("declare i32 @printf(i8*, ...)")
        self._emit_line("")
    
    def _emit_string_declarations(self):
        """Emite declarações de strings globais."""
        if not self.strings:
            return
        
        self._emit_line("; Strings globais")
        for string_id in sorted(self.strings.keys()):
            string_val = self.strings[string_id]
            # Calcula o tamanho (inclui \0 e \n se necessário)
            size = len(string_val) + 2  # +1 para \n, +1 para \0
            escaped = string_val.replace('\\', '\\\\').replace('"', '\\"')
            self._emit_line(f'@.str.{string_id} = private unnamed_addr constant [{size} x i8] c"{escaped}\\0A\\00", align 1')
        self._emit_line("")
    
    def _collect_strings(self, node):
        """Coleta todas as strings do programa (primeira passada)."""
        if node is None:
            return
        
        node_type = type(node).__name__
        
        if node_type == 'ProgramaNode':
            for decl in node.declaracoes:
                self._collect_strings(decl)
        
        elif node_type == 'BlocoNode':
            for instr in node.declaracoes:
                self._collect_strings(instr)
        
        elif node_type == 'ChamadaFuncaoNode':
            # Verifica se é ESCREVA
            if hasattr(node, 'nome') and node.nome == 'ESCREVA':
                for arg in node.argumentos:
                    self._collect_strings(arg)
        
        elif node_type == 'LiteralNode':
            if isinstance(node.valor, str):
                if node.valor not in self.strings.values():
                    self.strings[self.string_counter] = node.valor
                    self.string_counter += 1
        
        elif node_type == 'AtribuicaoNode':
            self._collect_strings(node.expressao)
        
        elif node_type == 'SeNode':
            self._collect_strings(node.bloco_se)
            if node.blocos_senaose:
                for _, bloco in node.blocos_senaose:
                    self._collect_strings(bloco)
            if node.bloco_senao:
                self._collect_strings(node.bloco_senao)
        
        elif node_type == 'EnquantoNode':
            self._collect_strings(node.bloco)
        
        elif node_type == 'ParaNode':
            self._collect_strings(node.bloco)
    
    def _emit_line(self, line):
        """Emite uma linha de código com indentação."""
        indent = "  " * self.indent_level
        self.output.append(indent + line)
    
    def _new_temp(self):
        """Gera um novo registrador temporário."""
        temp = f"%t{self.temp_counter}"
        self.temp_counter += 1
        return temp
    
    def _new_label(self, prefix="label"):
        """Gera um novo label para bloco básico."""
        label = f"{prefix}{self.label_counter}"
        self.label_counter += 1
        return label
    
    def _compile_node(self, node):
        """
        Compila um nó da AST.
        
        Args:
            node: Nó da AST a compilar
            
        Returns:
            String com o registrador contendo o resultado (para expressões)
        """
        if node is None:
            return None
        
        node_type = type(node).__name__
        
        if node_type == 'AtribuicaoNode':
            return self._compile_atribuicao(node)
        
        elif node_type == 'ChamadaFuncaoNode':
            return self._compile_chamada_funcao(node)
        
        elif node_type == 'ExpressaoBinariaNode':
            return self._compile_expressao_binaria(node)
        
        elif node_type == 'ExpressaoUnariaNode':
            return self._compile_expressao_unaria(node)
        
        elif node_type == 'LiteralNode':
            return self._compile_literal(node)
        
        elif node_type == 'IdentificadorNode':
            return self._compile_identificador(node)
        
        elif node_type == 'SeNode':
            return self._compile_se(node)
        
        elif node_type == 'EnquantoNode':
            return self._compile_enquanto(node)
        
        elif node_type == 'ParaNode':
            return self._compile_para(node)
        
        elif node_type == 'BlocoNode':
            return self._compile_bloco(node)
        
        elif node_type == 'RetornarNode':
            return self._compile_retornar(node)
        
        elif node_type == 'FuncaoNode':
            # Funções são compiladas separadamente, não inline
            return None
        
        else:
            # Nó não suportado - ignora
            return None
    
    def _compile_atribuicao(self, node):
        """Compila uma atribuição."""
        nome_var = node.identificador.nome
        
        # Compila a expressão
        valor_reg = self._compile_node(node.expressao)
        
        if valor_reg is None:
            return None
        
        # Aloca espaço se é primeira atribuição
        if nome_var not in self.var_map:
            var_reg = self._new_temp()
            self._emit_line(f"{var_reg} = alloca i32, align 4")
            self.var_map[nome_var] = var_reg
        
        # Store do valor
        var_ptr = self.var_map[nome_var]
        self._emit_line(f"store i32 {valor_reg}, i32* {var_ptr}, align 4")
        
        return valor_reg
    
    def _compile_chamada_funcao(self, node):
        """Compila uma chamada de função."""
        # Funções nativas
        if node.nome == 'ESCREVA':
            return self._compile_escreva(node)
        
        # Funções definidas pelo usuário
        if node.nome in self.functions:
            func_info = self.functions[node.nome]
            tipo_ret = func_info['tipo_retorno']
            params_info = func_info['parametros']
            
            # Avalia argumentos
            args_regs = []
            for i, arg in enumerate(node.argumentos):
                arg_reg = self._compile_node(arg)
                if arg_reg:
                    # Por enquanto assume que todos são i32
                    args_regs.append(f"i32 {arg_reg}")
            
            # Chama função
            result = self._new_temp()
            args_str = ', '.join(args_regs) if args_regs else ''
            self._emit_line(f"{result} = call {tipo_ret} @{node.nome}({args_str})")
            return result
        
        return None
    
    def _compile_escreva(self, node):
        """Compila uma chamada a ESCREVA."""
        if not node.argumentos:
            # ESCREVA sem argumentos - apenas nova linha
            str_id = self._get_or_create_string("")
            str_ptr = self._new_temp()
            self._emit_line(f"{str_ptr} = getelementptr inbounds [{len('') + 2} x i8], [{len('') + 2} x i8]* @.str.{str_id}, i32 0, i32 0")
            result = self._new_temp()
            self._emit_line(f"{result} = call i32 (i8*, ...) @printf(i8* {str_ptr})")
            return result
        
        # Com argumentos
        for arg in node.argumentos:
            arg_type = type(arg).__name__
            
            if arg_type == 'LiteralNode':
                if isinstance(arg.valor, str):
                    # String literal
                    str_id = self._get_or_create_string(arg.valor)
                    str_size = len(arg.valor) + 2
                    str_ptr = self._new_temp()
                    self._emit_line(f"{str_ptr} = getelementptr inbounds [{str_size} x i8], [{str_size} x i8]* @.str.{str_id}, i32 0, i32 0")
                    result = self._new_temp()
                    self._emit_line(f"{result} = call i32 (i8*, ...) @printf(i8* {str_ptr})")
                
                elif isinstance(arg.valor, int):
                    # Inteiro - usa formato "%d\n"
                    fmt_id = self._get_or_create_string("%d")
                    fmt_size = len("%d") + 2
                    fmt_ptr = self._new_temp()
                    self._emit_line(f"{fmt_ptr} = getelementptr inbounds [{fmt_size} x i8], [{fmt_size} x i8]* @.str.{fmt_id}, i32 0, i32 0")
                    result = self._new_temp()
                    self._emit_line(f"{result} = call i32 (i8*, ...) @printf(i8* {fmt_ptr}, i32 {arg.valor})")
            
            elif arg_type == 'IdentificadorNode':
                # Variável - carrega e imprime
                var_ptr = self.var_map.get(arg.nome)
                if var_ptr:
                    # Load do valor
                    val_reg = self._new_temp()
                    self._emit_line(f"{val_reg} = load i32, i32* {var_ptr}, align 4")
                    
                    # Printf
                    fmt_id = self._get_or_create_string("%d")
                    fmt_size = len("%d") + 2
                    fmt_ptr = self._new_temp()
                    self._emit_line(f"{fmt_ptr} = getelementptr inbounds [{fmt_size} x i8], [{fmt_size} x i8]* @.str.{fmt_id}, i32 0, i32 0")
                    result = self._new_temp()
                    self._emit_line(f"{result} = call i32 (i8*, ...) @printf(i8* {fmt_ptr}, i32 {val_reg})")
            
            elif arg_type == 'ExpressaoBinariaNode':
                # Expressão - avalia e imprime
                val_reg = self._compile_node(arg)
                if val_reg:
                    fmt_id = self._get_or_create_string("%d")
                    fmt_size = len("%d") + 2
                    fmt_ptr = self._new_temp()
                    self._emit_line(f"{fmt_ptr} = getelementptr inbounds [{fmt_size} x i8], [{fmt_size} x i8]* @.str.{fmt_id}, i32 0, i32 0")
                    result = self._new_temp()
                    self._emit_line(f"{result} = call i32 (i8*, ...) @printf(i8* {fmt_ptr}, i32 {val_reg})")
        
        return None
    
    def _compile_expressao_binaria(self, node):
        """Compila uma expressão binária."""
        # Compila operandos
        esq_reg = self._compile_node(node.esquerda)
        dir_reg = self._compile_node(node.direita)
        
        if esq_reg is None or dir_reg is None:
            return None
        
        # Operação
        op = node.operador.lexema if hasattr(node.operador, 'lexema') else node.operador
        result = self._new_temp()
        
        # Operadores aritméticos
        if op == '+':
            self._emit_line(f"{result} = add nsw i32 {esq_reg}, {dir_reg}")
        elif op == '-':
            self._emit_line(f"{result} = sub nsw i32 {esq_reg}, {dir_reg}")
        elif op == '*':
            self._emit_line(f"{result} = mul nsw i32 {esq_reg}, {dir_reg}")
        elif op == '/':
            self._emit_line(f"{result} = sdiv i32 {esq_reg}, {dir_reg}")
        elif op == '%':
            self._emit_line(f"{result} = srem i32 {esq_reg}, {dir_reg}")
        
        # Operadores relacionais
        elif op == '<':
            self._emit_line(f"{result} = icmp slt i32 {esq_reg}, {dir_reg}")
        elif op == '>':
            self._emit_line(f"{result} = icmp sgt i32 {esq_reg}, {dir_reg}")
        elif op == '<=':
            self._emit_line(f"{result} = icmp sle i32 {esq_reg}, {dir_reg}")
        elif op == '>=':
            self._emit_line(f"{result} = icmp sge i32 {esq_reg}, {dir_reg}")
        elif op == '==':
            self._emit_line(f"{result} = icmp eq i32 {esq_reg}, {dir_reg}")
        elif op == '!=':
            self._emit_line(f"{result} = icmp ne i32 {esq_reg}, {dir_reg}")
        
        # Operadores lógicos
        elif op == 'E':
            self._emit_line(f"{result} = and i1 {esq_reg}, {dir_reg}")
        elif op == 'OU':
            self._emit_line(f"{result} = or i1 {esq_reg}, {dir_reg}")
        
        else:
            # Operador não suportado
            return None
        
        return result
    
    def _compile_literal(self, node):
        """Compila um literal."""
        if isinstance(node.valor, int):
            return str(node.valor)
        elif isinstance(node.valor, float):
            # Por enquanto, trata floats como inteiros
            return str(int(node.valor))
        else:
            # Outros tipos não suportados em expressões
            return None
    
    def _compile_identificador(self, node):
        """Compila um identificador (variável)."""
        var_ptr = self.var_map.get(node.nome)
        if var_ptr is None:
            return None
        
        # Load do valor
        result = self._new_temp()
        self._emit_line(f"{result} = load i32, i32* {var_ptr}, align 4")
        return result
    
    def _get_or_create_string(self, string_val):
        """Retorna o ID de uma string, criando se necessário."""
        for str_id, val in self.strings.items():
            if val == string_val:
                return str_id
        
        # Cria nova string
        str_id = self.string_counter
        self.strings[str_id] = string_val
        self.string_counter += 1
        return str_id
    
    def _compile_expressao_unaria(self, node):
        """Compila uma expressão unária."""
        expr_reg = self._compile_node(node.expressao)
        if expr_reg is None:
            return None
        
        op = node.operador.lexema if hasattr(node.operador, 'lexema') else node.operador
        result = self._new_temp()
        
        if op == '-':
            # Negação aritmética: 0 - expr
            self._emit_line(f"{result} = sub nsw i32 0, {expr_reg}")
        elif op == 'NAO':
            # Negação lógica
            self._emit_line(f"{result} = xor i1 {expr_reg}, true")
        else:
            return None
        
        return result
    
    def _compile_bloco(self, node):
        """Compila um bloco de instruções."""
        if not hasattr(node, 'declaracoes'):
            return None
        
        for instr in node.declaracoes:
            self._compile_node(instr)
        
        return None
    
    def _compile_se(self, node):
        """Compila uma estrutura SE/SENAO."""
        # Labels
        label_then = self._new_label("then")
        label_else = self._new_label("else") if node.bloco_senao or node.blocos_senaose else None
        label_end = self._new_label("endif")
        
        # Avalia condição
        cond_reg = self._compile_node(node.condicao)
        if cond_reg is None:
            return None
        
        # Branch condicional
        if label_else:
            self._emit_line(f"br i1 {cond_reg}, label %{label_then}, label %{label_else}")
        else:
            self._emit_line(f"br i1 {cond_reg}, label %{label_then}, label %{label_end}")
        
        # Bloco THEN (SE)
        self.indent_level -= 1
        self._emit_line(f"{label_then}:")
        self.indent_level += 1
        self._compile_node(node.bloco_se)
        self._emit_line(f"br label %{label_end}")
        
        # Blocos SENAOSE
        if node.blocos_senaose:
            for i, (cond_senaose, bloco_senaose) in enumerate(node.blocos_senaose):
                # Label do SENAOSE atual
                self.indent_level -= 1
                self._emit_line(f"{label_else}:")
                self.indent_level += 1
                
                # Avalia condição do SENAOSE
                cond_se_reg = self._compile_node(cond_senaose)
                
                # Cria labels para próximo bloco
                label_then_se = self._new_label("then")
                
                # Verifica se há mais SENAOSE ou SENAO depois
                if i < len(node.blocos_senaose) - 1:
                    label_else = self._new_label("else")
                    self._emit_line(f"br i1 {cond_se_reg}, label %{label_then_se}, label %{label_else}")
                elif node.bloco_senao:
                    label_else = self._new_label("else")
                    self._emit_line(f"br i1 {cond_se_reg}, label %{label_then_se}, label %{label_else}")
                else:
                    self._emit_line(f"br i1 {cond_se_reg}, label %{label_then_se}, label %{label_end}")
                
                # Bloco do SENAOSE
                self.indent_level -= 1
                self._emit_line(f"{label_then_se}:")
                self.indent_level += 1
                self._compile_node(bloco_senaose)
                self._emit_line(f"br label %{label_end}")
        
        # Bloco ELSE (SENAO)
        if node.bloco_senao:
            self.indent_level -= 1
            self._emit_line(f"{label_else}:")
            self.indent_level += 1
            self._compile_node(node.bloco_senao)
            self._emit_line(f"br label %{label_end}")
        
        # Bloco final
        self.indent_level -= 1
        self._emit_line(f"{label_end}:")
        self.indent_level += 1
        
        return None
    
    def _compile_enquanto(self, node):
        """Compila um loop ENQUANTO."""
        # Labels
        label_cond = self._new_label("while_cond")
        label_body = self._new_label("while_body")
        label_end = self._new_label("while_end")
        
        # Branch para condição
        self._emit_line(f"br label %{label_cond}")
        
        # Bloco da condição
        self.indent_level -= 1
        self._emit_line(f"{label_cond}:")
        self.indent_level += 1
        
        # Avalia condição
        cond_reg = self._compile_node(node.condicao)
        if cond_reg is None:
            return None
        
        # Branch condicional
        self._emit_line(f"br i1 {cond_reg}, label %{label_body}, label %{label_end}")
        
        # Bloco do corpo
        self.indent_level -= 1
        self._emit_line(f"{label_body}:")
        self.indent_level += 1
        self._compile_node(node.bloco)
        self._emit_line(f"br label %{label_cond}")
        
        # Bloco final
        self.indent_level -= 1
        self._emit_line(f"{label_end}:")
        self.indent_level += 1
        
        return None
    
    def _compile_para(self, node):
        """Compila um loop PARA com INTERVALO."""
        # Suporta apenas PARA x DENTRODE INTERVALO(inicio, fim)
        if type(node.iteravel).__name__ != 'ChamadaFuncaoNode':
            return None
        
        if node.iteravel.nome != 'INTERVALO':
            return None
        
        # Extrai argumentos do INTERVALO
        args = node.iteravel.argumentos
        if len(args) < 1 or len(args) > 3:
            return None
        
        # INTERVALO(fim) ou INTERVALO(inicio, fim) ou INTERVALO(inicio, fim, passo)
        if len(args) == 1:
            inicio_reg = "0"
            fim_reg = self._compile_node(args[0])
            passo_reg = "1"
        elif len(args) == 2:
            inicio_reg = self._compile_node(args[0])
            fim_reg = self._compile_node(args[1])
            passo_reg = "1"
        else:
            inicio_reg = self._compile_node(args[0])
            fim_reg = self._compile_node(args[1])
            passo_reg = self._compile_node(args[2])
        
        # Aloca variável do loop
        var_nome = node.variavel
        if var_nome not in self.var_map:
            var_reg = self._new_temp()
            self._emit_line(f"{var_reg} = alloca i32, align 4")
            self.var_map[var_nome] = var_reg
        
        var_ptr = self.var_map[var_nome]
        
        # Inicializa variável
        self._emit_line(f"store i32 {inicio_reg}, i32* {var_ptr}, align 4")
        
        # Labels
        label_cond = self._new_label("for_cond")
        label_body = self._new_label("for_body")
        label_inc = self._new_label("for_inc")
        label_end = self._new_label("for_end")
        
        # Branch para condição
        self._emit_line(f"br label %{label_cond}")
        
        # Bloco da condição
        self.indent_level -= 1
        self._emit_line(f"{label_cond}:")
        self.indent_level += 1
        
        # Load valor atual
        current_reg = self._new_temp()
        self._emit_line(f"{current_reg} = load i32, i32* {var_ptr}, align 4")
        
        # Compara com fim
        cond_reg = self._new_temp()
        self._emit_line(f"{cond_reg} = icmp slt i32 {current_reg}, {fim_reg}")
        self._emit_line(f"br i1 {cond_reg}, label %{label_body}, label %{label_end}")
        
        # Bloco do corpo
        self.indent_level -= 1
        self._emit_line(f"{label_body}:")
        self.indent_level += 1
        self._compile_node(node.bloco)
        self._emit_line(f"br label %{label_inc}")
        
        # Bloco de incremento
        self.indent_level -= 1
        self._emit_line(f"{label_inc}:")
        self.indent_level += 1
        
        # Incrementa variável
        val_reg = self._new_temp()
        self._emit_line(f"{val_reg} = load i32, i32* {var_ptr}, align 4")
        next_reg = self._new_temp()
        self._emit_line(f"{next_reg} = add nsw i32 {val_reg}, {passo_reg}")
        self._emit_line(f"store i32 {next_reg}, i32* {var_ptr}, align 4")
        self._emit_line(f"br label %{label_cond}")
        
        # Bloco final
        self.indent_level -= 1
        self._emit_line(f"{label_end}:")
        self.indent_level += 1
        
        return None

    
    def _compile_funcao(self, node):
        '''Compila uma fun��o definida pelo usu�rio.'''
        nome = node.nome
        parametros = node.parametros
        tipo_retorno = node.tipo_retorno if hasattr(node, 'tipo_retorno') and node.tipo_retorno else None
        
        # Mapeia tipos Coral para LLVM
        tipo_map = {
            'INTEIRO': 'i32',
            'DECIMAL': 'double',
            'TEXTO': 'i8*',
            'BOOLEANO': 'i1',
            None: 'i32'
        }
        
        # Constr�i assinatura da fun��o
        tipo_ret_llvm = tipo_map.get(tipo_retorno, 'i32')
        params_llvm = []
        param_names = []
        
        for param in parametros:
            param_nome = param.nome
            param_tipo = param.tipo_anotacao if hasattr(param, 'tipo_anotacao') and param.tipo_anotacao else None
            param_tipo_llvm = tipo_map.get(param_tipo, 'i32')
            params_llvm.append(f'{param_tipo_llvm} %{param_nome}')
            param_names.append((param_nome, param_tipo_llvm))
        
        # Registra fun��o
        self.functions[nome] = {
            'tipo_retorno': tipo_ret_llvm,
            'parametros': param_names
        }
        
        # Emite defini��o da fun��o
        params_str = ', '.join(params_llvm) if params_llvm else ''
        self._emit_line(f'define {tipo_ret_llvm} @{nome}({params_str}) {{')
        self.indent_level += 1
        self.current_function = nome
        
        # Entry label
        self._emit_line('entry:')
        self.indent_level += 1
        
        # Salva contexto de vari�veis
        old_var_map = self.var_map.copy()
        self.var_map = {}
        
        # Aloca espa�o para par�metros
        self.function_params = {}
        for param_nome, param_tipo in param_names:
            param_ptr = self._new_temp()
            self._emit_line(f'{param_ptr} = alloca {param_tipo}, align 4')
            self._emit_line(f'store {param_tipo} %{param_nome}, {param_tipo}* {param_ptr}, align 4')
            self.var_map[param_nome] = param_ptr
            self.function_params[param_nome] = param_tipo
        
        # Compila corpo da fun��o
        self._compile_node(node.bloco)
        
        # Retorno padr�o
        if tipo_ret_llvm == 'i32':
            self._emit_line('ret i32 0')
        elif tipo_ret_llvm == 'double':
            self._emit_line('ret double 0.0')
        elif tipo_ret_llvm == 'i1':
            self._emit_line('ret i1 false')
        elif tipo_ret_llvm == 'i8*':
            self._emit_line('ret i8* null')
        
        # Restaura contexto
        self.var_map = old_var_map
        self.function_params = {}
        self.current_function = None
        
        self.indent_level -= 2
        self._emit_line('}')
        self._emit_line('')
        
        return None
    
    def _compile_retornar(self, node):
        '''Compila uma instru��o RETORNAR.'''
        if node.expressao is None:
            self._emit_line('ret i32 0')
        else:
            valor_reg = self._compile_node(node.expressao)
            if valor_reg:
                self._emit_line(f'ret i32 {valor_reg}')
            else:
                self._emit_line('ret i32 0')
        return None

    
    def _compile_funcao(self, node):
        """Compila uma função definida pelo usuário."""
        nome = node.nome
        parametros = node.parametros
        tipo_retorno = node.tipo_retorno if hasattr(node, 'tipo_retorno') and node.tipo_retorno else None
        
        # Mapeia tipos Coral para LLVM
        tipo_map = {
            'INTEIRO': 'i32',
            'DECIMAL': 'double',
            'TEXTO': 'i8*',
            'BOOLEANO': 'i1',
            None: 'i32'
        }
        
        # Constrói assinatura da função
        tipo_ret_llvm = tipo_map.get(tipo_retorno, 'i32')
        params_llvm = []
        param_names = []
        
        for param in parametros:
            param_nome = param.nome
            param_tipo = param.tipo_anotacao if hasattr(param, 'tipo_anotacao') and param.tipo_anotacao else None
            param_tipo_llvm = tipo_map.get(param_tipo, 'i32')
            params_llvm.append(f'{param_tipo_llvm} %{param_nome}')
            param_names.append((param_nome, param_tipo_llvm))
        
        # Registra função
        self.functions[nome] = {
            'tipo_retorno': tipo_ret_llvm,
            'parametros': param_names
        }
        
        # Emite definição da função
        params_str = ', '.join(params_llvm) if params_llvm else ''
        self._emit_line(f'define {tipo_ret_llvm} @{nome}({params_str}) {{')
        self.indent_level += 1
        self.current_function = nome
        
        # Entry label
        self._emit_line('entry:')
        self.indent_level += 1
        
        # Salva contexto de variáveis
        old_var_map = self.var_map.copy()
        self.var_map = {}
        
        # Aloca espaço para parâmetros
        self.function_params = {}
        for param_nome, param_tipo in param_names:
            param_ptr = self._new_temp()
            self._emit_line(f'{param_ptr} = alloca {param_tipo}, align 4')
            self._emit_line(f'store {param_tipo} %{param_nome}, {param_tipo}* {param_ptr}, align 4')
            self.var_map[param_nome] = param_ptr
            self.function_params[param_nome] = param_tipo
        
        # Compila corpo da função
        self._compile_node(node.bloco)
        
        # Retorno padrão
        if tipo_ret_llvm == 'i32':
            self._emit_line('ret i32 0')
        elif tipo_ret_llvm == 'double':
            self._emit_line('ret double 0.0')
        elif tipo_ret_llvm == 'i1':
            self._emit_line('ret i1 false')
        elif tipo_ret_llvm == 'i8*':
            self._emit_line('ret i8* null')
        
        self.var_map = old_var_map
        self.function_params = {}
        self.current_function = None
        
        self.indent_level -= 2
        self._emit_line('}')
        self._emit_line('')
        
        return None
    
    def _compile_retornar(self, node):
        """Compila uma instrução RETORNAR."""
        if node.expressao is None:
            self._emit_line('ret i32 0')
        else:
            valor_reg = self._compile_node(node.expressao)
            if valor_reg:
                self._emit_line(f'ret i32 {valor_reg}')
            else:
                self._emit_line('ret i32 0')
        return None
