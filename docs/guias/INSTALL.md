# Guia de Instalação e Uso - Coral Language

## Instalação

### Requisitos
- Python 3.7 ou superior
- Git (opcional, para clonar o repositório)

### Passos

1. **Clone o repositório** (ou baixe o ZIP)
   ```bash
   git clone https://github.com/GabrielVerri/Coral_project.git
   cd Coral_project
   ```

2. **Verifique a instalação do Python**
   ```bash
   python --version
   # ou
   python3 --version
   ```

3. **Pronto!** Coral não requer dependências externas.

## Uso Básico

### Windows

```powershell
# Método 1: Usando o arquivo .bat
coral.bat meu_programa.crl

# Método 2: Usando Python diretamente
python coral.py meu_programa.crl
```

### Linux/Mac

```bash
# Método 1: Tornar o script executável (primeira vez)
chmod +x coral
./coral meu_programa.crl

# Método 2: Usando Python diretamente
python3 coral.py meu_programa.crl
```

## Comandos Disponíveis

### Análise Completa (Padrão)
Executa análise léxica e sintática, gerando a AST.

```bash
python coral.py programa.crl
```

**Saída:**
```
======================================================================
Coral Language Interpreter v0.1.0
======================================================================

======================================================================
Análise Sintática - Arquivo: programa.crl
======================================================================

Programa(2 declarações)
  ...

Análise sintática concluída com sucesso!

======================================================================
Compilação concluída com sucesso!
======================================================================
```

### Análise Léxica (--lex)
Exibe apenas os tokens identificados.

```bash
python coral.py --lex programa.crl
```

**Saída:**
```
======================================================================
Análise Léxica - Arquivo: programa.crl
======================================================================

TOKEN                | TIPO
------------------------------------------
ESCREVA              | IDENTIFICADOR
(                    | DELIMITADOR
"Olá"                | STRING
)                    | DELIMITADOR

Análise léxica concluída: 4 tokens encontrados.
```

### Análise Sintática (--parse)
Exibe apenas a AST.

```bash
python coral.py --parse programa.crl
```

### Outras Opções

```bash
# Ver versão
python coral.py --version

# Ver ajuda
python coral.py --help
```

## Criando seu Primeiro Programa

1. **Crie um arquivo** `ola.crl`:
   ```coral
   texto = "Olá, Coral!"
   ESCREVA(texto)
   ```

2. **Execute:**
   ```bash
   python coral.py ola.crl
   ```

3. **Veja a AST gerada!**

## Exemplos Práticos

### Executar exemplos incluídos

```bash
# Olá Mundo
python coral.py exemplos/parser/ola_mundo.crl

# Funções
python coral.py exemplos/parser/funcoes.crl

# Laços de repetição
python coral.py exemplos/parser/lacos.crl

# Expressões aritméticas
python coral.py exemplos/parser/expressoes_aritmeticas.crl

# Ver AST ao invés de executar
python coral.py --ast exemplos/parser/estrutura_se.crl

# Análise léxica de operadores
python coral.py --lex exemplos/lexer/operadores_logicos.crl
```

## Solução de Problemas

### "python não é reconhecido como comando"

**Windows:**
- Certifique-se de que Python está no PATH
- Tente `py` ao invés de `python`

**Linux/Mac:**
- Use `python3` ao invés de `python`

### "Arquivo não encontrado"

- Verifique o caminho do arquivo
- Use caminho relativo a partir da pasta raiz do projeto
- No Windows, use `\` ou `/` para caminhos
  - `exemplos\parser\ola_mundo.crl`
  - `exemplos/parser/ola_mundo.crl`

### Arquivo sem extensão .crl

O interpretador aceita qualquer arquivo, mas irá perguntar se você deseja continuar:
```
Aviso: Arquivo 'programa.txt' não possui extensão .crl
Deseja continuar? (s/n):
```

## Executar Testes

```bash
# Todos os testes
python test/run_tests.py

# Teste específico
python -m pytest test/lexer_test/
```

## Próximos Passos

- Consulte a [documentação completa](README.md)
- Veja a [especificação da linguagem](docs/especificacao_linguagem/)
- Explore os [exemplos](exemplos/)

## Dicas

- Use `--lex` para debugar problemas de tokenização
- Use `--parse` para ver a estrutura do seu programa
- Os exemplos em `exemplos/` são ótimos pontos de partida
- A AST mostrada é a representação interna do seu código

## Precisa de Ajuda?

```bash
python coral.py --help
```

Ou consulte a documentação em [docs/](docs/)
