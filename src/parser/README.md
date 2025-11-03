# Parser - Analisador Sintático da Linguagem Coral

Este diretório contém a implementação do analisador sintático (parser) da linguagem Coral, responsável por transformar o fluxo de tokens gerado pelo lexer em uma Árvore Sintática Abstrata (AST).

## Arquitetura

O parser implementa um **analisador preditivo LL(1)** descendente recursivo, baseado na gramática formal documentada em `docs/especificacao_linguagem/gramatica_formal.md`.

### Componentes Principais

#### 1. `parser.py` - Parser Principal
- **Classe `ParserCoral`**: Implementa o algoritmo de parsing descendente
- **Classe `ErroSintatico`**: Exceção customizada para erros de sintaxe
- Utiliza os conjuntos FIRST e FOLLOW para decisões de parsing
- Produz uma AST a partir do fluxo de tokens

#### 2. `ast_nodes.py` - Nós da AST
Define todas as classes de nós da Árvore Sintática Abstrata:

**Estrutura Base:**
- `ASTNode`: Classe base para todos os nós
- `ProgramaNode`: Nó raiz do programa

**Declarações:**
- `DeclaracaoNode`: Classe base para declarações
- `ExpressaoNode`: Classe base para expressões

**Expressões:**
- `ExpressaoBinariaNode`: Operações binárias (+, -, *, /, ==, E, OU, etc.)
- `ExpressaoUnariaNode`: Operações unárias (-, NAO)
- `LiteralNode`: Valores literais (números, strings, booleanos)
- `IdentificadorNode`: Variáveis
- `AtribuicaoNode`: Atribuições (=, +=, -=, etc.)

**Estruturas de Controle:**
- `SeNode`: Condicional SE/SENAOSE/SENAO
- `EnquantoNode`: Laço ENQUANTO
- `ParaNode`: Laço PARA
- `BlocoNode`: Bloco de código indentado

**Funções:**
- `FuncaoNode`: Definição de função
- `ParametroNode`: Parâmetro de função
- `ChamadaFuncaoNode`: Chamada de função
- `RetornarNode`: Comando RETORNAR

**Classes:**
- `ClasseNode`: Definição de classe

**Coleções:**
- `ListaNode`: Lista literal [1, 2, 3]
- `DicionarioNode`: Dicionário {"chave": valor}
- `TuplaNode`: Tupla (1, 2, 3)

**Comandos:**
- `QuebraNode`: QUEBRA (break)
- `ContinuaNode`: CONTINUA (continue)
- `PassarNode`: PASSAR (pass)

**Acesso:**
- `AcessoAtributoNode`: obj.atributo
- `IndexacaoNode`: lista[0]

#### 3. `first_follow.py` - Conjuntos FIRST e FOLLOW
- **Classe `FirstFollowSets`**: Armazena os conjuntos FIRST e FOLLOW
- Conjuntos pré-calculados para todos os não-terminais da gramática
- Utilizados pelo parser para tomar decisões de parsing
- Baseados nos cálculos documentados na gramática formal

## Gramática Implementada

O parser implementa a seguinte gramática context-free (Tipo 2 de Chomsky):

```
G_Coral = (V, Σ, P, S)

V = {Programa, Declaracao, Expressao, ExprResto, Termo, TermoResto, Fator, FatorResto,
     FatorPrimario, EstruturaControle, BlocoSenaoSe, SenaoOpcional, Funcao, ListaParametros,
     Parametro, Classe, Bloco, ChamadaFuncao, ListaArgumentos}

Σ = {INTEIRO, DECIMAL, BOOLEANO, STRING, ID, SE, SENAOSE, SENAO, ENQUANTO, PARA,
     DENTRODE, FUNCAO, CLASSE, RETORNAR, QUEBRA, CONTINUA, PASSAR, E, OU, NAO,
     +, -, *, /, %, ==, !=, <, >, <=, >=, =, +=, -=, *=, /=, %=,
     (, ), [, ], {, }, :, ,, INDENT, DEDENT, NEWLINE}

S = Programa
```

### Propriedades da Gramática

**Sem Recursão à Esquerda**: Todas as produções foram transformadas usando o padrão A ⇒ β (α)*

**Fatorada à Esquerda**: Produções ambíguas foram fatoradas (ExprResto, TermoResto, FatorResto, SenaoOpcional)

**LL(1)**: A gramática satisfaz todas as condições para parsing preditivo:
- FIRST(α) ∩ FIRST(β) = ∅ para todas as produções alternativas A → α | β
- Se A → α e α ⇒* ε, então FIRST(α) ∩ FOLLOW(A) = ∅

## Uso

### Exemplo Básico

```python
from src.lexer.scanner import AnalisadorLexico
from src.parser import ParserCoral

# Código fonte
codigo = """
FUNCAO somar(a, b):
    RETORNAR a + b

x = somar(10, 20)
"""

# 1. Análise Léxica
lexer = AnalisadorLexico(codigo)
tokens = lexer.analisar()

# 2. Análise Sintática
parser = ParserCoral(tokens)
ast = parser.parse()

# 3. AST gerada
print(ast)  # ProgramaNode com as declarações
```

### Tratamento de Erros

```python
from src.parser import ParserCoral, ErroSintatico

try:
    parser = ParserCoral(tokens)
    ast = parser.parse()
except ErroSintatico as e:
    print(f"Erro na linha {e.linha}, coluna {e.coluna}:")
    print(f"  {e.mensagem}")
```

## Estrutura de Precedência

O parser implementa a seguinte precedência de operadores (do menor ao maior):

1. **Operadores Lógicos**: `E`, `OU`
2. **Operadores Relacionais**: `==`, `!=`, `<`, `>`, `<=`, `>=`
3. **Operadores Aritméticos**: `+`, `-`, `*`, `/`, `%`
4. **Operadores Unários**: `-`, `NAO`
5. **Chamadas de Função e Acesso**: `()`, `[]`, `.`

## Integração com o Lexer

O parser recebe tokens no formato produzido pelo `AnalisadorLexico`:

```python
class Token:
    def __init__(self, tipo, lexema, linha, coluna):
        self.tipo = tipo      # Tipo do token (ex: 'ID', 'INTEIRO', 'SE')
        self.lexema = lexema  # Texto original
        self.linha = linha    # Número da linha
        self.coluna = coluna  # Número da coluna
```

Tokens especiais importantes para o parser:
- `INDENT`: Marca início de bloco indentado
- `DEDENT`: Marca fim de bloco indentado
- `NEWLINE`: Quebra de linha
- `EOF`: Fim do arquivo

## Exemplos de AST Gerada

### Expressão Aritmética
```python
# Código: x = 10 + 20 * 3
ast = AtribuicaoNode(
    identificador=IdentificadorNode('x'),
    operador='=',
    expressao=ExpressaoBinariaNode(
        esquerda=LiteralNode(10, 'INTEIRO'),
        operador='+',
        direita=ExpressaoBinariaNode(
            esquerda=LiteralNode(20, 'INTEIRO'),
            operador='*',
            direita=LiteralNode(3, 'INTEIRO')
        )
    )
)
```

### Estrutura SE
```python
# Código:
# SE x > 10:
#     RETORNAR VERDADEIRO
# SENAO:
#     RETORNAR FALSO

ast = SeNode(
    condicao=ExpressaoBinariaNode(
        esquerda=IdentificadorNode('x'),
        operador='>',
        direita=LiteralNode(10, 'INTEIRO')
    ),
    bloco_se=BlocoNode([
        RetornarNode(LiteralNode(True, 'BOOLEANO'))
    ]),
    blocos_senaose=[],
    bloco_senao=BlocoNode([
        RetornarNode(LiteralNode(False, 'BOOLEANO'))
    ])
)
```

### Função
```python
# Código:
# FUNCAO dobrar(n):
#     RETORNAR n * 2

ast = FuncaoNode(
    nome='dobrar',
    parametros=[ParametroNode('n')],
    bloco=BlocoNode([
        RetornarNode(
            ExpressaoBinariaNode(
                esquerda=IdentificadorNode('n'),
                operador='*',
                direita=LiteralNode(2, 'INTEIRO')
            )
        )
    ])
)
```

## Algoritmo de Parsing

O parser utiliza o algoritmo de **análise preditiva descendente recursiva**:

```
parse():
    return programa()

programa():
    declaracoes = []
    while not EOF:
        declaracoes.append(declaracao())
    return ProgramaNode(declaracoes)

declaracao():
    if token_atual in FIRST(EstruturaControle):
        return estrutura_controle()
    if token_atual in FIRST(Funcao):
        return funcao()
    if token_atual in FIRST(Classe):
        return classe()
    else:
        return expressao_ou_atribuicao()

// ... métodos recursivos para cada não-terminal
```

## Referências

- **Gramática Formal**: `docs/especificacao_linguagem/gramatica_formal.md`
- **Lexer**: `src/lexer/scanner.py`
- **Tokens**: `docs/especificacao_linguagem/Tipo_de_tokens`
- **Exemplos**: `exemplos/lexer/*.crl`

## Próximos Passos

- [ ] Implementar análise semântica (tabela de símbolos, verificação de tipos)
- [ ] Adicionar testes unitários para o parser
- [ ] Implementar geração de código ou interpretação da AST
- [ ] Melhorar mensagens de erro com sugestões de correção
- [ ] Adicionar recuperação de erros (error recovery)
