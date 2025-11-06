# Analisador Sintático - Linguagem Coral

## Como Executar

Para executar o analisador sintático em um arquivo fonte:

```bash
python src/parser/parser.py <arquivo.crl>
```

Por exemplo:
```bash
python src/parser/parser.py exemplos/parser/funcoes.crl
```

## Formato da Saída

O analisador exibe a Árvore Sintática Abstrata (AST) do programa:

```
======================================================================
Árvore Sintática Abstrata (AST)
======================================================================

Programa(2 declarações)
  Funcao(somar, 2 params)
    Bloco(1 declarações)
      Retornar(ExpBinaria(Id(a) + Id(b)))
  Atribuicao(Id(resultado) = Chamada(somar, 2 args))

======================================================================
Análise concluída com sucesso!
======================================================================
```

## Tratamento de Erros

Em caso de erro sintático, será mostrada a linha e coluna do erro:

```
======================================================================
Erro Sintático
======================================================================
Erro sintático na linha 2, coluna 5: Esperado ':', encontrado 'NEWLINE'
```
