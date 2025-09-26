# Analisador Léxico - Linguagem Coral

## Como Executar

Para executar o analisador léxico em um arquivo fonte:

```bash
python src/lexer/main.py <arquivo.crl>
```

Por exemplo:
```bash
python src/lexer/main.py exemplos/ola_mundo.crl
```

## Formato da Saída

O analisador gera uma tabela com duas colunas mostrando os tokens reconhecidos:

```
TOKEN                | TIPO
----------------------------------------
ESCREVA             | PALAVRA_RESERVADA
(                   | SIMBOLO
"Olá mundo"         | STRING
)                   | SIMBOLO
```

Em caso de erro léxico (token inválido), será mostrada a linha e coluna do erro:

```
Erro léxico: Token inválido na linha 1, coluna 1: 'ESCREV'
```