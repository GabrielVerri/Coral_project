# Sintaxe da Linguagem Coral 🐍

Este documento descreve a sintaxe completa da linguagem de programação Coral, incluindo palavras reservadas, operadores, estruturas de controle e exemplos de uso.

## Índice

- [Características Gerais](#características-gerais)
- [Palavras Reservadas](#palavras-reservadas)
- [Tipos de Dados](#tipos-de-dados)
- [Operadores](#operadores)
- [Variáveis e Atribuição](#variáveis-e-atribuição)
- [Estruturas de Controle](#estruturas-de-controle)
- [Funções](#funções)
- [Classes](#classes)
- [Funções Nativas](#funções-nativas)
- [Comentários](#comentários)
- [Indentação](#indentação)
- [Exemplos Completos](#exemplos-completos)
- [Limitações Conhecidas](#limitações-conhecidas)
- [Recursos Implementados](#recursos-implementados)
- [Exemplos Práticos Disponíveis](#exemplos-práticos-disponíveis)

---

## Características Gerais

- **Sintaxe em Português**: Todas as palavras-chave são em português
- **Tipagem Dinâmica**: Não é necessário declarar tipos de variáveis
- **Sensível a maiúsculas**: `SE` é diferente de `se`
- **Indentação obrigatória**: Similar ao Python
- **Extensão de arquivo**: `.crl`

---

## Palavras Reservadas

### Estruturas de Controle
```
SE          - Condicional (if)
SENAO       - Caso contrário (else)
SENAOSE     - Caso contrário se (elif)
ENQUANTO    - Loop while
PARA        - Loop for
DENTRODE    - In (usado com PARA)
```

### Controle de Fluxo
```
QUEBRA      - Interrompe loop (break)
CONTINUA    - Pula para próxima iteração (continue)
PASSAR      - Instrução vazia (pass)
RETORNAR    - Retorna valor de função (return)
```

### Definições
```
FUNCAO      - Define função (def)
CLASSE      - Define classe (class)
```

### Literais e Valores
```
VAZIO       - Valor nulo (None/null)
VERDADE     - Booleano verdadeiro (True)
FALSO       - Booleano falso (False)
```

### Tipos (para anotações opcionais)
```
INTEIRO     - Tipo inteiro (int)
DECIMAL     - Tipo ponto flutuante (float)
TEXTO       - Tipo string (str)
BOOLEANO    - Tipo booleano (bool)
LISTA       - Tipo lista (list)
DICIONARIO  - Tipo dicionário (dict)
```

---

## Tipos de Dados

### Números
```coral
# Inteiros
idade = 25
ano = 2025

# Decimais
altura = 1.75
pi = 3.14159

# Notação científica
grande = 1.5e10
```

### Texto (Strings)
```coral
# String simples
nome = "João"
mensagem = 'Olá, mundo!'

# String multilinha
texto = """
Este é um texto
que ocupa várias
linhas
"""

# String com interpolação (f-string)
nome = "Maria"
idade = 25
mensagem = f"Olá, meu nome é {nome} e tenho {idade} anos"
# Resultado: "Olá, meu nome é Maria e tenho 25 anos"

# Interpolação com expressões
x = 10
y = 5
resultado = f"A soma de {x} + {y} é {x + y}"
# Resultado: "A soma de 10 + 5 é 15"
```

### Booleanos
```coral
ativo = VERDADE
desligado = FALSO
```

### Listas
```coral
# Lista vazia
lista = []

# Lista com elementos
numeros = [1, 2, 3, 4, 5]
misturado = [1, "texto", VERDADE, 3.14]

# Acesso por índice
primeiro = numeros[0]      # 1
ultimo = numeros[4]        # 5

# Modificação de elementos
numeros[0] = 10            # Altera primeiro elemento
numeros[2] = 99            # Altera terceiro elemento

# Concatenação
nova_lista = numeros + [6, 7, 8]

# Listas aninhadas (matrizes)
matriz = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Acesso a matriz (indexação encadeada)
elemento = matriz[0][0]    # 1
elemento = matriz[1][2]    # 6

# Modificação em matriz
matriz[0][0] = 99          # Modifica elemento [0][0]
matriz[2][1] = 88          # Modifica elemento [2][1]

# Iteração sobre listas
PARA item DENTRODE numeros:
    ESCREVA(item)

# Tamanho da lista
tamanho = TAMANHO(numeros)
```

### Dicionários
```coral
# Dicionário vazio
dados = {}

# Dicionário com pares chave-valor
pessoa = {
    "nome": "Maria",
    "idade": 30,
    "ativo": VERDADE
}

# Acesso por chave
nome = pessoa["nome"]
```

---

## Operadores

### Operadores Aritméticos
```coral
a + b      # Adição
a - b      # Subtração
a * b      # Multiplicação
a / b      # Divisão
a % b      # Módulo (resto)
a ** b     # Exponenciação
```

### Operadores Relacionais
```coral
a == b     # Igual
a != b     # Diferente
a < b      # Menor que
a > b      # Maior que
a <= b     # Menor ou igual
a >= b     # Maior ou igual
```

### Operadores Lógicos
```coral
a E b      # AND lógico
a OU b     # OR lógico
NAO a      # NOT lógico
```

### Operadores de Atribuição
```coral
x = 10     # Atribuição simples
x += 5     # x = x + 5
x -= 3     # x = x - 3
x *= 2     # x = x * 2
x /= 4     # x = x / 4
x %= 3     # x = x % 3
```

---

## Variáveis e Atribuição

### Declaração e Atribuição
```coral
# Atribuição simples
nome = "Coral"
idade = 25

# Atribuição múltipla (não suportada)
# a, b = 1, 2  # Não funciona

# Reatribuição
x = 10
x = 20
x = "agora é texto"
```

---

## Estruturas de Controle

### Condicional SE/SENAO
```coral
# SE simples
SE idade >= 18:
    ESCREVA("Maior de idade")

# SE com SENAO
SE nota >= 7:
    ESCREVA("Aprovado")
SENAO:
    ESCREVA("Reprovado")

# SE com SENAOSE
SE nota >= 9:
    ESCREVA("Excelente")
SENAOSE nota >= 7:
    ESCREVA("Bom")
SENAOSE nota >= 5:
    ESCREVA("Regular")
SENAO:
    ESCREVA("Insuficiente")

# Condições compostas
SE idade >= 18 E tem_documento:
    ESCREVA("Pode entrar")

SE chovendo OU frio:
    ESCREVA("Leve casaco")
```

### Loop ENQUANTO
```coral
# Loop básico
contador = 0
ENQUANTO contador < 5:
    ESCREVA(contador)
    contador = contador + 1

# Com QUEBRA
i = 0
ENQUANTO VERDADE:
    SE i >= 10:
        QUEBRA
    i += 1

# Com CONTINUA
n = 0
ENQUANTO n < 10:
    n += 1
    SE n % 2 == 0:
        CONTINUA
    ESCREVA(n)  # Imprime apenas ímpares
```

### Loop PARA
```coral
# Iterando sobre lista
numeros = [1, 2, 3, 4, 5]
PARA num DENTRODE numeros:
    ESCREVA(num)

# Iterando sobre INTERVALO
PARA i DENTRODE INTERVALO(10):
    ESCREVA(i)  # 0 a 9

PARA i DENTRODE INTERVALO(1, 11):
    ESCREVA(i)  # 1 a 10

PARA i DENTRODE INTERVALO(0, 20, 2):
    ESCREVA(i)  # 0, 2, 4, ..., 18

# Com QUEBRA e CONTINUA
PARA x DENTRODE [1, 2, 3, 4, 5]:
    SE x == 3:
        CONTINUA
    SE x == 5:
        QUEBRA
    ESCREVA(x)  # Imprime: 1, 2, 4
```

---

## Funções

### Definição de Funções
```coral
# Função simples
FUNCAO saudacao():
    ESCREVA("Olá!")

# Função com parâmetros
FUNCAO somar(a, b):
    RETORNAR a + b

# Função com múltiplos parâmetros
FUNCAO calcular_media(nota1, nota2, nota3):
    soma = nota1 + nota2 + nota3
    media = soma / 3
    RETORNAR media

# Função com anotação de tipo (opcional)
FUNCAO multiplicar(x: INTEIRO, y: INTEIRO):
    RETORNAR x * y
```

### Chamada de Funções
```coral
# Chamada simples
saudacao()

# Com argumentos
resultado = somar(5, 3)
ESCREVA(resultado)  # 8

# Função como expressão
dobro = somar(10, 10)
```

### Funções Recursivas
```coral
FUNCAO fatorial(n):
    SE n <= 1:
        RETORNAR 1
    RETORNAR n * fatorial(n - 1)

resultado = fatorial(5)  # 120
```

---

## Classes

### Definição de Classes
```coral
# Classe simples
CLASSE Pessoa:
    FUNCAO __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade
    
    FUNCAO apresentar(self):
        ESCREVA("Meu nome é", self.nome)
        ESCREVA("Tenho", self.idade, "anos")

# Uso
pessoa = Pessoa("João", 25)
pessoa.apresentar()
ESCREVA(pessoa.nome)
```

---

## Funções Nativas

### Entrada e Saída
```coral
# ESCREVA - Imprime valores
ESCREVA("Olá, mundo!")
ESCREVA("Valor:", 42)
ESCREVA("A", "B", "C")  # Múltiplos argumentos

# LER - Lê entrada do usuário
nome = LER("Digite seu nome: ")
idade = LER("Digite sua idade: ")
```

### Conversão de Tipos
```coral
# INTEIRO - Converte para inteiro
idade = INTEIRO(LER("Idade: "))
numero = INTEIRO("42")

# DECIMAL - Converte para decimal
altura = DECIMAL(LER("Altura: "))
pi = DECIMAL("3.14")

# TEXTO - Converte para texto
texto = TEXTO(123)
mensagem = TEXTO(VERDADE)
```

### Funções de Utilidade
```coral
# TIPO - Retorna o tipo da variável
t = TIPO(42)          # "int"
t = TIPO("texto")     # "str"
t = TIPO([1, 2, 3])   # "list"

# TAMANHO - Retorna tamanho de lista ou string
tam = TAMANHO([1, 2, 3, 4])    # 4
tam = TAMANHO("Coral")          # 5

# INTERVALO - Gera sequência numérica
nums = INTERVALO(5)           # [0, 1, 2, 3, 4]
nums = INTERVALO(1, 6)        # [1, 2, 3, 4, 5]
nums = INTERVALO(0, 10, 2)    # [0, 2, 4, 6, 8]
```

---

## Comentários

### Comentário de Linha
```coral
# Este é um comentário de linha única
x = 10  # Comentário no final da linha
```

### Comentário de Bloco
```coral
"""
Este é um comentário
de múltiplas linhas
ou docstring
"""
```

---

## Indentação

A indentação é **obrigatória** e define blocos de código. Use **4 espaços** ou **1 tab** consistentemente.

### Correto ✅
```coral
SE x > 0:
    ESCREVA("Positivo")
    y = x * 2
```

### Incorreto ❌
```coral
SE x > 0:
ESCREVA("Positivo")  # Erro: falta indentação
```

### Blocos Aninhados
```coral
PARA i DENTRODE INTERVALO(5):
    SE i % 2 == 0:
        ESCREVA("Par:", i)
    SENAO:
        ESCREVA("Ímpar:", i)
```

---

## Exemplos Completos

### Exemplo 1: Calculadora
```coral
ESCREVA("=== Calculadora ===")
a = DECIMAL(LER("Digite o primeiro número: "))
b = DECIMAL(LER("Digite o segundo número: "))

ESCREVA(f"Soma: {a + b}")
ESCREVA(f"Subtração: {a - b}")
ESCREVA(f"Multiplicação: {a * b}")
ESCREVA(f"Divisão: {a / b}")
```

### Exemplo 2: Verificar Número Primo
```coral
FUNCAO eh_primo(n):
    SE n < 2:
        RETORNAR FALSO
    
    PARA i DENTRODE INTERVALO(2, n):
        SE n % i == 0:
            RETORNAR FALSO
    
    RETORNAR VERDADE

numero = INTEIRO(LER("Digite um número: "))
SE eh_primo(numero):
    ESCREVA(f"{numero} é primo")
SENAO:
    ESCREVA(f"{numero} não é primo")
```

### Exemplo 3: Fatorial
```coral
FUNCAO fatorial(n):
    SE n <= 1:
        RETORNAR 1
    RETORNAR n * fatorial(n - 1)

num = INTEIRO(LER("Calcular fatorial de: "))
resultado = fatorial(num)
ESCREVA(f"Fatorial de {num} é {resultado}")
```

### Exemplo 4: Manipulação de Listas
```coral
# Criando e modificando listas
numeros = [1, 2, 3, 4, 5]
ESCREVA(f"Lista original: {numeros}")

# Modificando elementos
numeros[0] = 10
numeros[4] = 50
ESCREVA(f"Lista modificada: {numeros}")

# Filtrando números pares
pares = []
PARA n DENTRODE numeros:
    SE n % 2 == 0:
        pares = pares + [n]
ESCREVA(f"Números pares: {pares}")

# Matriz (lista de listas)
matriz = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Acessando e modificando matriz
ESCREVA(f"Elemento [1][1]: {matriz[1][1]}")
matriz[0][0] = 99
ESCREVA(f"Matriz após modificação:")
PARA linha DENTRODE matriz:
    ESCREVA(linha)
```

### Exemplo 5: Uso do Operador Módulo
```coral
# Sistema de turnos circular
jogadores = ["Ana", "Bruno", "Carlos", "Diana"]
ESCREVA("Simulando 8 rodadas:")

PARA rodada DENTRODE INTERVALO(1, 9):
    indice = rodada % TAMANHO(jogadores)
    jogador = jogadores[indice]
    ESCREVA(f"Rodada {rodada}: Vez de {jogador}")

# Verificando números pares/ímpares
ESCREVA("\nVerificando números de 1 a 10:")
PARA i DENTRODE INTERVALO(1, 11):
    SE i % 2 == 0:
        ESCREVA(f"{i} é par")
    SENAO:
        ESCREVA(f"{i} é ímpar")

# Extraindo último dígito
numero = 12345
ultimo_digito = numero % 10
ESCREVA(f"Último dígito de {numero}: {ultimo_digito}")
```

---

## Limitações Conhecidas

- Não há suporte para:
  - Importação de módulos
  - Tratamento de exceções (try/catch)
  - Geradores e iteradores
  - Compreensão de listas
  - Decoradores
  - Funções lambda
  - Operador ternário
  - Desempacotamento de tuplas
  - Índices negativos em listas (ex: `lista[-1]`)

---

## Recursos Implementados

✅ **Estruturas de dados completas**:
- Listas com acesso e modificação por índice
- Indexação encadeada para matrizes
- Dicionários com acesso por chave
- Concatenação de listas

✅ **Operadores completos**:
- Aritméticos: `+`, `-`, `*`, `/`, `%`, `**`
- Relacionais: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Lógicos: `E`, `OU`, `NAO`
- Atribuição: `=`, `+=`, `-=`, `*=`, `/=`, `%=`

✅ **Funções nativas**:
- I/O: `ESCREVA`, `LER`
- Conversão: `INTEIRO`, `DECIMAL`, `TEXTO`
- Utilidade: `TIPO`, `TAMANHO`, `INTERVALO`

✅ **Interpolação de strings**:
- F-strings com expressões: `f"Resultado: {x + y}"`
- Indexação em f-strings: `f"Primeiro: {lista[0]}"`

---

## Exemplos Práticos Disponíveis

Para ver exemplos funcionais completos, consulte:
- `exemplos/parser/manipulacao_listas.crl` - Todas as operações com listas
- `exemplos/parser/uso_modulo.crl` - Aplicações do operador módulo
- `exemplos/parser/teste_indexacao.crl` - Teste completo de indexação
- `exemplos/parser/programa_completo.crl` - Programa completo com classes
- `exemplos/parser/funcoes.crl` - Exemplos de funções

---

## Veja Também

- [Gramática Formal](especificacao_linguagem/gramatica_formal.md)
- [Exemplos de Código](../exemplos/)
- [Guia de Instalação](guias/instalacao.md)
- [Guia de Uso Local](guias/uso_local.md)
