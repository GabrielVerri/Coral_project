# Coral - Instalação Rápida

## Requisitos
Python 3.7+ instalado. Git opcional.

## Clonar
```bash
git clone https://github.com/GabrielVerri/Coral_project.git
cd Coral_project
```

## Executar

**Por padrão, use sempre:**
```bash
python coral.py arquivo.crl
python coral.py --lex arquivo.crl    # tokens
python coral.py --parse arquivo.crl  # AST
python coral.py --version            # versão
```
Funciona em qualquer máquina sem configuração adicional.

## Comando `coral` (instalação opcional)
Se preferir usar apenas `coral` ao invés de `python coral.py`:

**Windows:**
```cmd
install.bat
```
**Linux/Mac:**
```bash
bash install.sh
source ~/.bashrc   # ou ~/.zshrc
```
Depois pode usar:
```bash
coral arquivo.crl
```
**Importante:** Cada máquina nova precisa executar o instalador.

## Primeiro programa
Arquivo `ola.crl`:
```coral
ESCREVA("Olá, Coral!")
```
Executar:
```bash
coral ola.crl
```

## Exemplos
```bash
coral exemplos/parser/ola_mundo.crl
coral exemplos/parser/funcoes.crl
```

## Problemas comuns
PATH: use `python coral.py ...` se `coral` não funcionar.
Python não encontrado: verifique `python --version` ou use `py` / `python3`.
Arquivo não encontrado: confirme caminho relativo.

## Ajuda
```bash
python coral.py --help
```
