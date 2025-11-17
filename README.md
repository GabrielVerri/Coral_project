# Coral Language 🐍

Linguagem de programação interpretada com sintaxe em português, desenvolvida para a disciplina de Compiladores e Linguagens Formais.

## Como usar (forma recomendada)

A forma **principal** de usar a linguagem Coral é instalando o comando
`coral` via script de instalação (sem precisar clonar o repositório).

1. Siga o guia em `docs/guias/instalacao.md` para instalar o comando `coral`.
2. Crie um arquivo com extensão `.crl` (por exemplo, `programa.crl`):

```coral
ESCREVA("Olá, Coral!")
```

3. Execute o programa com:

```bash
coral programa.crl
coral --help
```

> Essa é a forma recomendada de uso para quem quer apenas **programar em Coral**.

**Guias:** [Instalação](docs/guias/instalacao.md) | [Uso local / exemplos](docs/guias/uso_local.md)

## Comandos (após instalação)

```bash
coral programa.crl          # Executar
coral --lex programa.crl    # Ver tokens
coral --parse programa.crl  # Ver análise sintática
coral --ast programa.crl    # Ver AST
coral --help                # Ajuda
coral --logo                # Ver logo
```

## Uso local para desenvolvimento

Para detalhes de **uso local**, criação de arquivos `.crl`, exemplos e
execução com Python, consulte o guia:

- `docs/guias/uso_local.md` (uso local, exemplos e fluxo de desenvolvimento)

## Estrutura do Projeto

```
Coral_project/
├── coral.py                      # Interpretador principal
├── install.ps1                   # Instalador Windows (PowerShell)
├── install.sh                    # Instalador Linux/macOS
├── install.bat                   # Launcher Windows (CMD)
├── src/
│   ├── lexer/                   # Análise léxica (AFN→AFD)
│   ├── parser/                  # Análise sintática (LL1)
│   ├── interpreter/             # Execução do código
│   └── utils/                   # Palavras reservadas e tipos
├── exemplos/
│   ├── lexer/                   # Exemplos de análise léxica
│   └── parser/                  # Programas completos
├── test/                        # Testes unitários
├── docs/
│   ├── especificacao_linguagem/ # Gramática e sintaxe
│   ├── diagramas/               # AFD/AFN
│   └── guias/                   # Guias de instalação
└── scripts/                     # Scripts executáveis
```

## Documentação

- **[instalacao.md](docs/guias/instalacao.md)** - Instalação e primeiros passos
- **[Especificação](docs/especificacao_linguagem/)** - Gramática e sintaxe
- **[Lexer](src/lexer/README.md)** - Analisador léxico
- **[Parser](src/parser/README.md)** - Analisador sintático
- **[Diagramas AFD/AFN](docs/diagramas/)** - Autômatos

## Exemplos

```bash
python coral.py exemplos/parser/ola_mundo.crl
python coral.py exemplos/parser/teste_classe_self.crl
python coral.py exemplos/parser/teste_validacao_tipos.crl
```

Veja mais em [`exemplos/`](exemplos/).

## Desenvolvimento

### Requisitos
- Python 3.7+
- pytest (para testes)

### Executar Testes
```bash
python test/run_tests.py
```

## Licença

Projeto acadêmico desenvolvido para a disciplina de Compiladores e Linguagens Formais.

## Autores

Coral Language Team
