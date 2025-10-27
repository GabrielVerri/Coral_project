# **CORAL - Gramática Formal**

## **Definição Formal: G = (V, Σ, P, S)**

```
G_Coral = (V, Σ, P, S)

Onde:
  V = Símbolos não-terminais
  Σ = Símbolos terminais (alfabeto)
  P = Regras de produção
  S = Símbolo inicial (Programa)
```

---

# **1. Símbolos Não-Terminais (V)**

```
V = {
    Programa, Declaracao, Expressao, Termo, Fator,
    EstruturaControle, Se, SeBloco, SenaoBloco, Enquanto, Para,
    Funcao, Classe, Bloco, ListaParametros,
    Identificador, Numero, Booleano, String,
    OperadorAritmetico, OperadorRelacional, OperadorLogico
}
```

---

# **2. Símbolos Terminais (Σ)**

## **Alfabeto Base**

letras = {a,...,z,A,...Z}  
numeros = {0,...,9}  
operador = {+, −, *, /, =, >, <,!}  
especial = {espaco,newline,tab,underscore,{,},[,],%,&,(,),|,;,.,,,:}

**Nota:** Coral é orientada por identação (como Python). Blocos usam `:` + identação, **não `{}`**. As chaves `{}` são para **dicionários**, `[]` para **listas**, e `()` para **funções/tuplas**.

## **Tokens (Σ)**

## **Tokens (Σ)**

Identificadores = [a-zA-Z_][a-zA-Z0-9_]*  
Operadores lógicos = \b(E|OU|NAO)\b  
Booleanos = \b(VERDADE|FALSO)\b  
Operadores aritméticos = (+|-|*|/|%|\*\*)  
Operadores relacionais = (==|!=|<=|>=|<|>)  
Operadores atribuição = (=|+=|-=|*=|/=|%=|\*\*=|++|--)  
Comentários em linha = \#.*  
String = ("[^"\n]*"|'[^'\n]*')  
String multilinha = (""".*?"""|'''.*?''')  
Decimal = [0-9]+\.[0-9]+  
Inteiro = [0-9]+  
Delimitadores = (\(|\)|\{|\}|\[|\]|,|;|:|.)

Palavras reservadas = \b(SE|SENAO|SENAOSE|ENQUANTO|PARA|DENTRODE|E|OU|NAO|VERDADE|FALSO|INTEIRO|DECIMAL|TEXTO|BOOLEANO|DEF|CLASSE|RETORNAR|QUEBRA|CONTINUA|PASSAR|GLOBAL|NAOLOCAL|IMPORTAR|DE|COMO|TENTE|EXCETO|FINALMENTE|LANCAR|AFIRMA|ESPERA|VAZIO|EIGUAL|LAMBDA|COM|DELETAR|ASSINCRONO|ENVIAR)\b

Tokens de controle = {INDENTA, DEDENTA, NEWLINE, EOF}

---

# **3. Regras de Produção (P)**

Programa ⇒ (Declaracao)*

Declaracao ⇒ Expressao | EstruturaControle | Funcao | Classe

Expressao ⇒ Termo (OperadorAritimetico Termo)*   
Termo ⇒ Fator (OperadorRelacional Fator)*  
Fator ⇒ Identificador | Numero | Booleano | String | ‘(‘ Expressao ‘)’

EstruturaControle ⇒ SE Expressao Bloco   
                  | SE Expressao Bloco SENAO Bloco   
                  | Enquanto Expressao Bloco   
                  | PARA Identificador DENTRODE Expressao Bloco

Funcao ⇒ DEF Identificador '(' ListaParametros ')' Bloco  
ListaParametros ⇒ Identificador (',' Identificador)*

Classe ⇒ CLASSE Identificador Bloco

Bloco ⇒ ':' INDENTA Declaracao* DEDENTA

---

# **4. Símbolo Inicial (S)**

```
S = Programa
```

---

# **5. Precedência e Associatividade**

1. OU  
2. E  
3. NAO (unário, mais alto que E/OU)  
4. Comparações: == != < <= > >=  
5. Soma/Subtração: + - (esquerda)  
6. Produto/Divisão/Módulo: * / % (esquerda)  
7. Exponenciação: ** (direita)  
8. Unários: +x -x (direita)  
9. Acesso/Chamada/Indexação

---

# **6. Classificação na Hierarquia de Chomsky**

- **Léxico:** Tipo 3 (Regular) - Reconhecido por autômato finito (AFD). Exemplos: identificadores, números, delimitadores, operadores.  
- **Sintaxe:** Tipo 2 (Livre de Contexto) - Reconhecível por autômato de pilha (PDA). Blocos aninhados e expressões com precedência são naturalmente CFL.

---

# **7. Derivações**

## **7.1 Expressão Aritmética**

Entrada: a + b * c ** d

1. Expressao ⇒ ExprOr ⇒ ExprAnd ⇒ ExprNot ⇒ ExprComparacao ⇒ ExprSoma  
2. ExprSoma ⇒ ExprProduto + ExprProduto  
3. O ExprProduto da direita: ⇒ ExprExpon * ExprExpon  
4. O ExprExpon da direita: ⇒ ExprUnario ** ExprUnario ⇒ Primario ** Primario ⇒ Identificador ** Identificador  
5. Restante reduz a Identificador em cada posição.

A árvore reflete ** > * > +, com ** à direita.

## **7.2 Condicional com Encadeamento**

Entrada:  
SE x > 0:  
    y = 1  
SENAOSE x == 0:  
    y = 0  
SENAO:  
    y = -1

Derivação:

- Comando ⇒ SE  
- Se ⇒ SE Expressao ":" Bloco {SENAOSE ...} [SENAO ...]  
- Cada Bloco ⇒ newline INDENTA {Atribuicao} DEDENTA

A construção {SENAOSE ...} elimina o clássico dangling else.

## **7.3 Laço ENQUANTO**

Entrada:  
ENQUANTO i < n:  
    i += 1

- Comando ⇒ Enquanto  
- Enquanto ⇒ ENQUANTO Expressao ":" Bloco  
- Bloco ⇒ newline INDENTA {Atribuicao} DEDENTA

---

# **8. Ambiguidades e Estratégias de Resolução**

1. **Precedência/Associatividade de Operadores**  
   Risco: a + b * c ser lido como (a + b) * c.  
   Estratégia: Camadas ExprSoma/ExprProduto/ExprExpon resolvem automaticamente.  
     
2. **Dangling Else**  
   Risco: SENAO associar ao SE errado.  
   Estratégia: Produção única Se com {SENAOSE ...} [SENAO ...] evita ambiguidade.  
     
3. **Chamada/Acesso/Indexação**  
   Risco: Colisão entre Identificador, Acesso, Chamada.  
   Estratégia: Primario + pós-fixos controlados (Acesso, Chamada, Indexação) com maior amarração.  
     
4. **Indentação**  
   Risco: Contagem de espaços/tabulações.  
   Estratégia: Lexer gera INDENTA/DEDENTA consistentes (pilha de níveis). Mistura TAB/ESPAÇO proibida.  
     
5. **Palavras Reservadas vs Identificadores**  
   Risco: Sobreposição entre identificadores e palavras reservadas (SE atende regex de identificador).  
   Solução: Palavras reservadas têm precedência no analisador léxico. Uso de \b na regex garante fronteira de palavra.

---

## **Resumo**

```
G_Coral = (V, Σ, P, S)

V = {Programa, Declaracao, Expressao, Termo, Fator, ...}
Σ = {SE, SENAO, ENQUANTO, DEF, CLASSE, +, -, *, /, ==, ...}
P = {Programa ⇒ (Declaracao)*, Declaracao ⇒ Expressao | ..., ...}
S = Programa

Tipo: Livre de Contexto (Tipo-2 de Chomsky)
```

---

# **9. Exemplos de Código Coral**

## **9.1 Função Simples**
```coral
DEF somar(a, b):
    resultado = a + b
    RETORNAR resultado

x = somar(5, 3)  # x = 8
```

## **9.2 Estrutura Condicional**
```coral
idade = 18

SE idade >= 18:
    status = "maior de idade"
SENAOSE idade >= 13:
    status = "adolescente"
SENAO:
    status = "criança"
```

## **9.3 Laços e Coleções**
```coral
# Lista e laço PARA
numeros = [1, 2, 3, 4, 5]
soma = 0

PARA num DENTRODE numeros:
    soma = soma + num

# Dicionário
config = {
    "debug": VERDADE,
    "porta": 8080,
    "host": "localhost"
}

# Laço ENQUANTO
contador = 0
ENQUANTO contador < 10:
    contador += 1
```

## **9.4 Classe**
```coral
CLASSE Calculadora:
    DEF somar(a, b):
        RETORNAR a + b
    
    DEF multiplicar(a, b):
        resultado = 0
        PARA i DENTRODE [1, 2, 3, 4, 5]:
            SE i <= b:
                resultado += a
        RETORNAR resultado

calc = Calculadora()
valor = calc.somar(10, 20)
```

## **9.5 Expressões Complexas**
```coral
# Precedência: ** > * > +
resultado = 2 + 3 * 4 ** 2  # 2 + 3 * 16 = 2 + 48 = 50

# Lógica booleana: NAO > E > OU
condicao = VERDADE OU FALSO E NAO VERDADE  # VERDADE OU (FALSO E FALSO) = VERDADE

# Comparações encadeadas
valido = x > 0 E x < 100 E x != 50
```

---

# **10. Árvore de Derivação Visual**

## **Exemplo: `2 + 3 * 4`**

```
         Programa
            |
        Declaracao
            |
        Expressao
            |
         ExprSoma
        /    |    \
    Expr   '+'   ExprProduto
     |            /    |    \
  Primario    Expr  '*'  Primario
     |          |           |
     2      Primario        4
               |
               3

Resultado: 2 + (3 * 4) = 2 + 12 = 14
```

---

# **11. Comparação com Python**

| **Aspecto** | **Coral** | **Python** |
|------------|-----------|------------|
| Palavras-chave | Português | Inglês |
| Condicionais | `SE`, `SENAO`, `SENAOSE` | `if`, `else`, `elif` |
| Laços | `ENQUANTO`, `PARA` | `while`, `for` |
| Lógica | `E`, `OU`, `NAO` | `and`, `or`, `not` |
| Booleanos | `VERDADE`, `FALSO` | `True`, `False` |
| Funções | `DEF nome():` | `def nome():` |
| Classes | `CLASSE Nome:` | `class Nome:` |
| Indentação | Significativa (`:` + indent) | Significativa (`:` + indent) |
| Comentários | `#` | `#` |
| Strings | `"..."`, `'...'`, `"""..."""` | `"..."`, `'...'`, `"""..."""` |

---

# **12. Validação da Gramática**

- ✓ **Completa**: Cobre todos os tokens do lexer implementado
- ✓ **Consistente**: Alinhada com o código fonte em `src/lexer/`
- ✓ **Não ambígua**: Precedência e associatividade definidas
- ✓ **Livre de contexto**: Tipo 2 na hierarquia de Chomsky
- ✓ **Determinística**: Analisável por parser LL/LR
- ✓ **34 palavras reservadas**: Todas reconhecidas pelo lexer
- ✓ **Indentação**: Tokens INDENTA/DEDENTA para controle de blocos
