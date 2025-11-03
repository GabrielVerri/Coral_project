# Exemplos do Parser

Este diretório contém exemplos de código Coral (`.crl`) para testar o analisador sintático (parser).

## Como Executar

```bash
# A partir do diretório raiz do projeto
python src/parser/parser.py exemplos/parser/expressoes_aritmeticas.crl
```

## Arquivos de Exemplo (.crl)

### 1. `expressoes_aritmeticas.crl`
Demonstra precedência de operadores aritméticos:
- Adição, subtração, multiplicação, divisão
- Uso de parênteses para alterar precedência
- Expressões compostas

**Status**: Totalmente funcional

### 2. `expressoes_logicas.crl`
Operadores lógicos e relacionais:
- Comparações: `>`, `<`, `>=`, `<=`, `==`, `!=`
- Operadores lógicos: `E`, `OU`, `NAO`
- Expressões booleanas compostas

**Status**: Totalmente funcional

### Limitação Atual

O lexer atual possui suporte completo para INDENTA/DEDENTA, portanto:
- Todos os exemplos com funções, classes e estruturas de controle funcionam
- Blocos indentados são processados corretamente
- Todas as estruturas da linguagem estão habilitadas

### Exemplos Funcionando

Todos os exemplos estão funcionais:
- Expressões aritméticas simples
- Atribuições
- Expressões com parênteses
- Chamadas de função
- Estruturas de controle (SE, ENQUANTO, PARA)
- Definição de funções e classes
- Blocos indentados

## Roadmap

1. Parser implementado e funcional
2. Suporte INDENTA/DEDENTA implementado no lexer
3. Todos os exemplos com blocos habilitados
4. Testes completos do parser

## Script de Teste

Para testar um arquivo específico:

```bash
python src/parser/parser.py exemplos/parser/<arquivo>.crl
```

### Saída Esperada

```
======================================================================
Parser Coral - Análise Sintática
======================================================================

Arquivo: exemplos/parser/expressoes_aritmeticas.crl

[1/2] Análise Léxica...
✓ 31 tokens gerados

[2/2] Análise Sintática...
✓ AST construída com sucesso!

======================================================================
Árvore Sintática Abstrata (AST)
======================================================================

Programa(4 declarações)
  Atribuicao(Id(x) = ExpBinaria(...))
  ...

======================================================================
Análise concluída com sucesso!
======================================================================
```

**O que o script faz:**
1. Encontra todos os arquivos `.crl` no diretório
2. Para cada arquivo:
   - Exibe o código fonte
   - Executa análise léxica (tokenização)
   - Executa análise sintática (parsing)
   - Exibe a AST (Árvore Sintática Abstrata) gerada
3. Exibe resumo final com sucessos/falhas

## Estrutura de um Exemplo Completo

```python
from src.lexer import AnalisadorLexico
from src.parser import ParserCoral, ErroSintatico

# 1. Código fonte
codigo = """
FUNCAO somar(a, b):
    RETORNAR a + b
"""

# 2. Análise Léxica
lexer = AnalisadorLexico(codigo)
tokens = lexer.analisar()

# 3. Análise Sintática
try:
    parser = ParserCoral(tokens)
    ast = parser.parse()
    print("Parsing bem-sucedido!")
    print(ast)
except ErroSintatico as e:
    print(f"Erro na linha {e.linha}: {e.mensagem}")
```

## Mais Exemplos

Para exemplos de código Coral válido, veja também:
- `exemplos/lexer/*.crl` - Exemplos de código que o lexer consegue tokenizar
- `docs/especificacao_linguagem/Exemplos_de_codigo.co` - Especificação de exemplos

## Testes

Para testes completos do parser, veja:
- `test/parser_test/` - Testes unitários do parser (a ser implementado)
