# Identação em Coral

## Características Principais

Coral é uma **linguagem orientada por identação**, inspirada em Python. Isso significa que a estrutura do código é definida pela identação (espaços ou tabulações), não por delimitadores como chaves `{}`.

## Regras de Identação

### 1. Blocos de Código

Blocos de código são definidos por:
- **Dois pontos (`:`)** ao final da linha que inicia o bloco
- **Identação aumentada** nas linhas seguintes que pertencem ao bloco
- **Retorno à identação anterior** para finalizar o bloco

**Exemplo:**

```coral
SE x > 0:
    ESCREVA("Positivo")    # Bloco identado
    y = x * 2              # Ainda dentro do bloco
ESCREVA("Fim")             # Fora do bloco (sem identação)
```

### 2. Estruturas que Exigem Identação

As seguintes estruturas da linguagem exigem blocos identados:

#### Condicionais
```coral
SE condicao:
    # bloco identado
    instrucao1
    instrucao2
SENAO:
    # outro bloco identado
    instrucao3
```

#### Laços de Repetição
```coral
ENQUANTO condicao:
    # bloco identado
    instrucao

PARA item DENTRODE lista:
    # bloco identado
    processar(item)
```

#### Funções
```coral
FUNCAO calcular(x, y):
    # bloco identado
    resultado = x + y
    RETORNAR resultado
```

#### Classes
```coral
CLASSE MinhaClasse:
    # bloco identado
    FUNCAO __init__(self):
        self.valor = 0
```

#### Tratamento de Exceções
```coral
TENTE:
    # bloco identado
    operacao_perigosa()
EXCETO ErroTipo:
    # bloco identado
    tratar_erro()
```

### 3. Blocos Aninhados

Blocos podem ser aninhados, aumentando a identação a cada nível:

```coral
PARA i DENTRODE range(10):
    SE i % 2 == 0:
        ENQUANTO i > 0:
            ESCREVA(i)
            i = i - 1
```

### 4. Identação Consistente

**IMPORTANTE:** A identação deve ser consistente em todo o arquivo:

- ✅ **Usar apenas espaços** OU **apenas tabulações**
- ✅ **Manter o mesmo número de espaços** para cada nível de identação (recomendado: 4 espaços)
- ❌ **NÃO misturar espaços e tabulações**

**Exemplo correto (4 espaços por nível):**
```coral
SE x > 0:
    SE y > 0:
        ESCREVA("Ambos positivos")
```

**Exemplo INCORRETO (mistura de espaços):**
```coral
SE x > 0:
  SE y > 0:    # 2 espaços
      ESCREVA("Erro!")  # 6 espaços - inconsistente!
```

### 5. Uso de Delimitadores

**Importante:** Em Coral, os delimitadores têm usos específicos:

| Delimitador | Uso em Coral |
|-------------|--------------|
| `{ }` | **Dicionários** apenas (ex: `dados = {"nome": "João", "idade": 25}`) |
| `( )` | **Chamadas de função** e **tuplas** (ex: `calcular(x, y)` ou `coords = (10, 20)`) |
| `[ ]` | **Listas** (ex: `numeros = [1, 2, 3, 4]`) |
| `:` | **Início de blocos** de código identados |

**Chaves NÃO são usadas para blocos de código!**

### 6. Diferenças com C/Java/JavaScript

| Aspecto | Coral (Python-like) | C/Java/JavaScript |
|---------|---------------------|-------------------|
| Delimitadores de bloco | Identação obrigatória + `:` | `{ }` chaves |
| Fim de bloco | Redução de identação | `}` chave de fechamento |
| Dicionários | `{"chave": "valor"}` | Varia por linguagem |
| Chamadas de função | `funcao(args)` | `funcao(args)` |
| Ponto e vírgula | Opcional | Obrigatório (maioria) |

**Exemplo comparativo:**

**Coral:**
```coral
SE x > 0:
    ESCREVA("Positivo")
    y = x * 2
```

**Java/C:**
```java
if (x > 0) {
    escreva("Positivo");
    y = x * 2;
}
```

### 7. Exemplos de Uso de Delimitadores

#### Dicionários (chaves `{}`)
```coral
pessoa = {
    "nome": "Maria",
    "idade": 30,
    "cidade": "São Paulo"
}
```

#### Listas (colchetes `[]`)
```coral
numeros = [1, 2, 3, 4, 5]
PARA n DENTRODE numeros:
    ESCREVA(n * 2)
```

#### Funções (parênteses `()`)
```coral
FUNCAO somar(a, b):
    RETORNAR a + b

resultado = somar(10, 20)  # Chamada de função
```

#### Tuplas (parênteses `()`)
```coral
coordenadas = (10, 20, 30)
x, y, z = coordenadas
```

### 8. Vantagens da Identação

1. **Legibilidade**: Código visualmente limpo e organizado
2. **Menos caracteres**: Não precisa de `{` e `}`
3. **Força boas práticas**: Identação correta é obrigatória, não opcional
4. **Reduz erros**: Não há confusão com chaves esquecidas ou mal posicionadas

### 9. Tokens Especiais de Identação

O analisador léxico gera tokens especiais para controlar a identação:

- **`INDENTA`**: Indica aumento de nível de identação (início de bloco)
- **`DEDENTA`**: Indica redução de nível de identação (fim de bloco)
- **`NEWLINE`**: Indica fim de linha significativo

**Exemplo de análise:**
```coral
SE x > 0:
    y = 1
z = 2
```

**Tokens gerados:**
```
SE, x, >, 0, :, NEWLINE
INDENTA, y, =, 1, NEWLINE
DEDENTA, z, =, 2, NEWLINE
```

## Resumo

- ✅ Use **dois pontos (`:`)** para iniciar blocos
- ✅ Use **identação consistente** (4 espaços recomendado)
- ✅ **Use chaves `{}` apenas para dicionários**, não para blocos de código
- ✅ A identação **não é opcional** - faz parte da gramática da linguagem
