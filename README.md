# Coral Language 🐍

Linguagem de programação desenvolvida para a disciplina de Compiladores e Linguagens Formais.

## Como Usar

### Windows - Início Rápido

**Opção 1: Configurar ambiente (recomendado)**
```powershell
# Configure o ambiente Coral para a sessão atual do terminal
.\setup_env.bat

# Agora pode usar o comando 'coral' diretamente
coral teste.crl
coral --cat teste.crl
coral --help
```

**Opção 2: Executar diretamente (sem configurar)**
```powershell
# Usando Python
python coral.py teste.crl

# Usando o script
.\scripts\coral.bat teste.crl
```

**Opção 3: Instalação permanente**
```powershell
# Adiciona ao PATH do sistema (requer reabrir terminal)
.\scripts\instalar.bat

# Depois de reabrir o terminal:
coral teste.crl
```

### Linux/Mac

```bash
# Instalação
chmod +x scripts/instalar.sh
./scripts/instalar.sh

# Uso
coral programa.crl
```

**Guias:** [Linux/Mac](docs/guias/LINUX.md) | [Instalação](docs/guias/INSTALL.md)

### Opções de Linha de Comando

```bash
# Executar programa (mostra apenas o output)
coral programa.crl

# Exibir código fonte do arquivo
coral --cat programa.crl

# Apenas análise léxica
coral --lex programa.crl

# Apenas análise sintática
coral --parse programa.crl

# Exibir AST (Árvore Sintática Abstrata)
coral --ast programa.crl

# Exibir versão
coral --version

# Exibir ajuda
coral --help
```

## Estrutura do Projeto

```
Coral_project/
├── coral.py              # Executável principal do interpretador
├── coral.spec            # Configuração PyInstaller
├── setup_env.bat         # Configuração rápida de ambiente (Windows)
├── src/
│   ├── lexer/           # Analisador léxico (tokenização)
│   ├── parser/          # Analisador sintático (AST)
│   ├── interpreter/     # Interpretador (execução)
│   └── utils/           # Utilitários compartilhados
├── scripts/
│   ├── coral.bat        # Script executável Windows
│   ├── coral            # Script executável Linux/Mac
│   ├── instalar.bat     # Instalador permanente Windows
│   ├── instalar.sh      # Instalador Linux/Mac
│   ├── build_executable.sh   # Build executável Linux/Mac
│   └── build_executable.bat  # Build executável Windows
├── exemplos/
│   ├── lexer/           # Exemplos para análise léxica
│   └── parser/          # Exemplos para análise sintática e execução
├── test/                # Testes unitários
└── docs/                # Documentação completa
```

## Testando

Execute os exemplos incluídos:

```powershell
# Primeiro configure o ambiente (Windows)
.\setup_env.bat

# Executar programas (mostra apenas o output)
coral exemplos\parser\ola_mundo.crl
coral exemplos\parser\funcoes.crl
coral exemplos\parser\lacos.crl
coral exemplos\parser\expressoes_aritmeticas.crl

# Ver o código fonte
coral --cat exemplos\parser\ola_mundo.crl

# Ver a AST (árvore sintática)
coral --ast exemplos\parser\expressoes_aritmeticas.crl

# Apenas análise léxica
coral --lex exemplos\lexer\ola_mundo_correto.crl
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
