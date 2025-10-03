# Diagramas dos AFDs para a Linguagem Coral

Este documento contém os diagramas em formato Mermaid para os Autômatos Finitos Determinísticos (AFDs) que reconhecem os tokens da linguagem Coral, conforme especificado no Projeto Integrador. Cada seção descreve a expressão regular correspondente e apresenta o diagrama do AFD.

## 1. AFDIdentificadores

**Expressão Regular**: `[a-zA-Z_][a-zA-Z0-9_]*`

**Descrição**: Reconhece identificadores que começam com uma letra (`a-z`, `A-Z`) ou sublinhado (`_`), seguidos por zero ou mais letras, números ou sublinhados.

```mermaid
stateDiagram-v2
    [*] --> q0
    q0 --> q1 : letra
    q0 --> q2 : numero,outro
    q1 --> q1 : letra,numero
    q1 --> q2 : outro
    q2 --> q2 : letra,numero,outro

    state "q0 (inicial)" as q0
    state "q1 (aceitação)" as q1
    state "q2 (erro)" as q2
```

## 2. AFDOperadoresLogicos

**Expressão Regular**: `\b(E|OU|NAO)\b`

**Descrição**: Reconhece os operadores lógicos `E`, `OU` e `NAO`, com limites de palavra para evitar extensões (ex.: `E1` é inválido).

```mermaid
stateDiagram-v2
    [*] --> q0
    q0 --> q1 : E
    q0 --> q2 : O
    q0 --> q3 : N
    q0 --> q10 : outro
    q1 --> q4 : outro
    q2 --> q5 : U
    q2 --> q10 : outro
    q3 --> q6 : A
    q3 --> q10 : outro
    q5 --> q7 : outro
    q6 --> q8 : O
    q6 --> q10 : outro
    q8 --> q9 : outro
    q4 --> q10 : E,O,N,U,A,outro
    q7 --> q10 : E,O,N,U,A,outro
    q9 --> q10 : E,O,N,U,A,outro
    q10 --> q10 : E,O,N,U,A,outro

    state "q0 (inicial)" as q0
    state "q4 (aceitação E)" as q4
    state "q7 (aceitação OU)" as q7
    state "q9 (aceitação NAO)" as q9
    state "q10 (erro)" as q10
```

## 3. AFDOperadoresBooleanos

**Expressão Regular**: `\b(VERDADE|FALSO)\b`

**Descrição**: Reconhece os operadores booleanos `VERDADE` e `FALSO`, com limites de palavra para evitar extensões (ex.: `VERDADEIRO` é inválido).

```mermaid
stateDiagram-v2
    [*] --> q0
    q0 --> q1 : V
    q0 --> q6 : F
    q0 --> q12 : outro
    q1 --> q2 : E
    q1 --> q12 : outro
    q2 --> q3 : R
    q2 --> q12 : outro
    q3 --> q4 : D
    q3 --> q12 : outro
    q4 --> q5 : A
    q4 --> q12 : outro
    q5 --> q11 : outro
    q6 --> q7 : A
    q6 --> q12 : outro
    q7 --> q8 : L
    q7 --> q12 : outro
    q8 --> q9 : S
    q8 --> q12 : outro
    q9 --> q10 : O
    q9 --> q12 : outro
    q10 --> q11 : outro
    q11 --> q12 : V,F,outro
    q12 --> q12 : V,F,outro

    state "q0 (inicial)" as q0
    state "q5 (aceitação VERDADE)" as q5
    state "q10 (aceitação FALSO)" as q10
    state "q12 (erro)" as q12
```

## 4. AFDOperadoresAritmeticosRelacionais

**Expressão Regular**: `(\*\*|\*\*=|==|!=|<=|>=|\+=|-=|\*=|/=|%=|\+\+|--|\+|\-|\*|\/|%|=|!|<|>)`

**Descrição**: Reconhece operadores aritméticos (`+`, `-`, `*`, `/`, `%`, `**`, `++`, `--`) e relacionais (`==`, `!=`, `<=`, `>=`, `<`, `>`), além de operadores de atribuição composta (`+=`, `-=`, `*=`, `/=`, `%=`, `**=`).

```mermaid
stateDiagram-v2
    [*] --> q0
    q0 --> q1 : +
    q0 --> q2 : -
    q0 --> q3 : *
    q0 --> q4 : /
    q0 --> q5 : %
    q0 --> q6 : =
    q0 --> q7 : !
    q0 --> q8 : <
    q0 --> q9 : >
    q0 --> q15 : outro
    q1 --> q10 : +
    q1 --> q11 : =
    q1 --> q14 : outro
    q2 --> q12 : -
    q2 --> q13 : =
    q2 --> q14 : outro
    q3 --> q16 : *
    q3 --> q17 : =
    q3 --> q14 : outro
    q4 --> q18 : =
    q4 --> q14 : outro
    q5 --> q19 : =
    q5 --> q14 : outro
    q6 --> q20 : =
    q6 --> q14 : outro
    q7 --> q21 : =
    q7 --> q14 : outro
    q8 --> q22 : =
    q8 --> q14 : outro
    q9 --> q23 : =
    q9 --> q14 : outro
    q10 --> q14 : outro
    q11 --> q14 : outro
    q12 --> q14 : outro
    q13 --> q14 : outro
    q14 --> q15 : +,-,*,/,%,=,!,<,>,outro
    q16 --> q24 : =
    q16 --> q14 : outro
    q17 --> q14 : outro
    q18 --> q14 : outro
    q19 --> q14 : outro
    q20 --> q14 : outro
    q21 --> q14 : outro
    q22 --> q14 : outro
    q23 --> q14 : outro
    q24 --> q14 : outro
    q15 --> q15 : +,-,*,/,%,=,!,<,>,outro

    state "q0 (inicial)" as q0
    state "q1 (+)" as q1
    state "q2 (-)" as q2
    state "q3 (*)" as q3
    state "q4 (/)" as q4
    state "q5 (%)" as q5
    state "q6 (=)" as q6
    state "q7 (!)" as q7
    state "q8 (<)" as q8
    state "q9 (>)" as q9
    state "q10 (++)" as q10
    state "q11 (+=)" as q11
    state "q12 (--)" as q12
    state "q13 (-=)" as q13
    state "q16 (**)" as q16
    state "q17 (*=)" as q17
    state "q18 (/=)" as q18
    state "q19 (%=)" as q19
    state "q20 (==)" as q20
    state "q21 (!=)" as q21
    state "q22 (<=)" as q22
    state "q23 (>=)" as q23
    state "q24 (**=)" as q24
    state "q14 (auxiliar)" as q14
    state "q15 (erro)" as q15
```

## 5. AFDComentariosLinha

**Expressão Regular**: `\#.*`

**Descrição**: Reconhece comentários em linha que começam com `#` e aceitam qualquer sequência de caracteres após isso.

```mermaid
stateDiagram-v2
    [*] --> q0
    q0 --> q1 : #
    q0 --> q2 : outro
    q1 --> q1 : outro
    q2 --> q2 : #,outro

    state "q0 (inicial)" as q0
    state "q1 (aceitação)" as q1
    state "q2 (erro)" as q2
```

## 6. AFDStringLiteral

**Expressão Regular**: `("([^"\n])*"|'([^'\n])*'|"""([^"]|("(?!"")))*"""|'''([^']|('(?!'')))*''')`

**Descrição**: Reconhece strings delimitadas por aspas simples (`'`), duplas (`"`) ou triplas (`"""`, `'''`), com conteúdo que não inclui quebras de linha (`\n`) ou aspas de fechamento não correspondidas.

```mermaid
stateDiagram-v2
    [*] --> q0
    q0 --> q1 : "
    q0 --> q5 : '
    q0 --> q15 : outro
    q1 --> q2 : "
    q1 --> q3 : outro
    q1 --> q15 : \n
    q2 --> q9 : "
    q2 --> q15 : outro
    q3 --> q2 : "
    q3 --> q3 : outro
    q3 --> q15 : \n
    q5 --> q6 : '
    q5 --> q7 : outro
    q5 --> q15 : \n
    q6 --> q10 : '
    q6 --> q15 : outro
    q7 --> q6 : '
    q7 --> q7 : outro
    q7 --> q15 : \n
    q9 --> q11 : "
    q9 --> q15 : outro
    q10 --> q12 : '
    q10 --> q15 : outro
    q11 --> q4 : "
    q11 --> q13 : outro
    q11 --> q15 : \n
    q12 --> q8 : '
    q12 --> q14 : outro
    q12 --> q15 : \n
    q13 --> q4 : "
    q13 --> q13 : outro
    q13 --> q15 : \n
    q14 --> q8 : '
    q14 --> q14 : outro
    q14 --> q15 : \n
    q4 --> q15 : outro
    q8 --> q15 : outro
    q15 --> q15 : ",',\n,outro

    state "q0 (inicial)" as q0
    state "q2 (aceitação \")" as q2
    state "q4 (aceitação \"\"\")" as q4
    state "q6 (aceitação ')" as q6
    state "q8 (aceitação ''')" as q8
    state "q15 (erro)" as q15
```

## 7. AFDDecimal

**Expressão Regular**: `[0-9]+(\.[0-9]+)?`

**Descrição**: Reconhece números inteiros (`[0-9]+`) e decimais (`[0-9]+.[0-9]+`), com a parte decimal sendo opcional.

```mermaid
stateDiagram-v2
    [*] --> q0
    q0 --> q1 : numero
    q0 --> q4 : outro
    q1 --> q1 : numero
    q1 --> q2 : .
    q1 --> q4 : outro
    q2 --> q3 : numero
    q2 --> q4 : outro
    q3 --> q3 : numero
    q3 --> q4 : outro
    q4 --> q4 : numero,.,outro

    state "q0 (inicial)" as q0
    state "q1 (aceitação inteiro)" as q1
    state "q2 (transição)" as q2
    state "q3 (aceitação decimal)" as q3
    state "q4 (erro)" as q4
```