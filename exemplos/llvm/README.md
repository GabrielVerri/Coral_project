## Exemplos LLVM IR

Este diretório contém exemplos mínimos para gerar LLVM IR a partir de programas Coral.

## Uso rápido

Gerar LLVM IR a partir de um arquivo Coral:

```bash
python coral.py --llvmir exemplos/llvm/aritmetica_simples.crl
```

Isso criará um arquivo `.ll` com código LLVM IR válido.

## Exemplos incluídos

- `aritmetica_simples.crl` — operações aritméticas e `ESCREVA`
- `decisao.crl` — `SE` / `SENAO` com comparações
- `loop_enquanto.crl` — `ENQUANTO` funcionando
- `loop_para.crl` — `PARA` com `INTERVALO` (corpo com ajustes)
- `fatorial.crl` — cálculo de fatorial (exemplo completo)

## Recursos principais

- Variáveis inteiras e literais
- Operações aritméticas: `+ - * / %`
- Comparações: `< > <= >= == !=`
- Lógica básica: `E`, `OU`, `NAO`
- Controle: `SE` / `SENAO`, `ENQUANTO`
- `ESCREVA` (strings literais e inteiros)

## Limitações

- Tipos tratados como `i32` (inteiros)
- Sem suporte a funções do usuário, listas, dicionários ou floats
- `PARA` está parcialmente suportado (estrutura gerada; corpo precisa refinamento)

## Testes rápidos

```bash
python coral.py --ast exemplos/llvm/fatorial.crl   # ver AST
python coral.py --llvmir exemplos/llvm/fatorial.crl # gerar LLVM IR
```

---

Este README é propositalmente enxuto — para detalhes e exemplos completos veja `exemplos/parser/README.md`.
