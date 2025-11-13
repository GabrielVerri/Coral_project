# Coral Language 🐍

Linguagem de programação interpretada com sintaxe em português, desenvolvida para a disciplina de Compiladores e Linguagens Formais.

## 🚀 Instalação e Uso

```bash
git clone https://github.com/GabrielVerri/Coral_project.git
cd Coral_project
python coral.py arquivo.crl
```

> **Nota:** Use `python coral.py` para executar em qualquer máquina sem configuração.  
> Opcionalmente, você pode instalar o comando `coral` (ver [INSTALL.md](docs/guias/INSTALL.md)).

**Guias:** [INSTALL.md](docs/guias/INSTALL.md) | [Linux/Mac](docs/guias/LINUX.md)

## Comandos

```bash
python coral.py programa.crl          # Executar
python coral.py --lex programa.crl    # Ver tokens
python coral.py --parse programa.crl  # Ver AST
python coral.py --help                # Ajuda
```

## Estrutura do Projeto

```
Coral_project/
├── coral.py                      # Interpretador principal
├── install.bat / install.sh      # Instaladores
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

- **[INSTALL.md](docs/guias/INSTALL.md)** - Instalação e primeiros passos
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
