# Coral Language 🐍

Linguagem de programação desenvolvida para a disciplina de Compiladores e Linguagens Formais.

## Como Usar

### Instalação Rápida

**Linux/Mac:**
```bash
chmod +x scripts/instalar.sh
./scripts/instalar.sh
# Depois use: coral <arquivo.crl>
```

**Guia completo:** [docs/guias/LINUX.md](docs/guias/LINUX.md)

**Guia de instalação:** [docs/guias/INSTALL.md](docs/guias/INSTALL.md)

### Execução Rápida (sem instalar)

**Windows:**
```bash
python coral.py <arquivo.crl>
# ou
scripts\coral.bat <arquivo.crl>
```

**Linux/Mac:**
```bash
python3 coral.py <arquivo.crl>
# ou
./scripts/coral <arquivo.crl>
```

### Opções de Linha de Comando

```bash
# Executar análise completa (léxica + sintática)
python coral.py programa.crl

# Apenas análise léxica
python coral.py --lex programa.crl

# Apenas análise sintática
python coral.py --parse programa.crl

# Exibir versão
python coral.py --version

# Exibir ajuda
python coral.py --help
```

## Estrutura do Projeto

```
Coral_project/
├── coral.py              # Executável principal
├── coral.spec            # Configuração PyInstaller
├── src/
│   ├── lexer/           # Analisador léxico
│   ├── parser/          # Analisador sintático
│   ├── interpreter/     # Interpretador
│   └── utils/           # Utilitários compartilhados
├── scripts/
│   ├── coral.bat        # Script Windows
│   ├── coral            # Script Linux/Mac
│   ├── instalar.sh      # Instalador Linux/Mac
│   ├── build_executable.sh   # Build executável Linux/Mac
│   └── build_executable.bat  # Build executável Windows
├── exemplos/
│   ├── lexer/           # Exemplos para análise léxica
│   └── parser/          # Exemplos para análise sintática
├── test/                # Testes unitários
└── docs/                # Documentação
```

## Testando

Execute os exemplos incluídos:

```bash
# Executar programas
python coral.py exemplos/parser/ola_mundo.crl
python coral.py exemplos/parser/funcoes.crl
python coral.py exemplos/parser/lacos.crl

# Ver a AST (árvore sintática)
python coral.py --ast exemplos/parser/expressoes_aritmeticas.crl

# Apenas análise léxica
python coral.py --lex exemplos/lexer/ola_mundo_correto.crl
```

## Documentação

### Guias de Uso
- [Guia Linux/Mac](docs/guias/LINUX.md) - Como instalar e usar no Linux
- [Guia de Instalação](docs/guias/INSTALL.md) - Instalação detalhada

### Documentação Técnica
- [Analisador Léxico](src/lexer/README.md) - Como funciona o lexer
- [Analisador Sintático](src/parser/README.md) - Como funciona o parser
- [Especificação da Linguagem](docs/especificacao_linguagem/) - Gramática e regras
- [Diagramas](docs/diagramas/) - Diagramas AFD/AFN

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
