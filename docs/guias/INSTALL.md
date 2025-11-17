# Coral Language - Instalação

## 📦 Instalação Rápida (Recomendado)

### Windows (PowerShell)
```powershell
irm https://raw.githubusercontent.com/GabrielVerri/Coral_project/dev/quick_install.ps1 | iex
```

### Linux / macOS (Bash)
```bash
curl -fsSL https://raw.githubusercontent.com/GabrielVerri/Coral_project/dev/install.sh | bash
```

**O que isso faz:**
- Baixa automaticamente o projeto do GitHub
- Instala em `~/CoralLanguage` (Linux/Mac) ou `%USERPROFILE%\CoralLanguage` (Windows)
- Adiciona o comando `coral` ao PATH

**Após a instalação:**
- **Windows**: Feche e reabra o terminal
- **Linux/macOS**: Execute `source ~/.bashrc` (ou `~/.zshrc`)

## 🛠️ Instalação Manual

### 1. Clonar o Repositório
```bash
git clone https://github.com/GabrielVerri/Coral_project.git
cd Coral_project
```

### 2. Configurar PATH (Opcional)

**Windows:**
```cmd
install.bat
```

**Linux/Mac:**
```bash
chmod +x install.sh
./install.sh
source ~/.bashrc   # ou ~/.zshrc
```

## 🚀 Uso

### Com o comando `coral` (após instalação)
```bash
coral arquivo.crl
coral --lex arquivo.crl    # Ver tokens
coral --parse arquivo.crl  # Ver AST
coral --version            # Ver versão
coral --help               # Ver ajuda
```

### Usando Python diretamente (sem instalação)
```bash
python coral.py arquivo.crl
python coral.py --lex arquivo.crl
python coral.py --parse arquivo.crl
```

## 📝 Primeiro Programa

Crie um arquivo `ola.crl`:
```coral
ESCREVA("Olá, Coral!")
```

Execute:
```bash
coral ola.crl
# ou
python coral.py ola.crl
```

## 📚 Exemplos

```bash
coral exemplos/parser/ola_mundo.crl
coral exemplos/parser/funcoes.crl
coral exemplos/lexer/strings_comentarios.crl
```

## ❓ Requisitos

- **Python**: 3.7 ou superior
- **Windows**: PowerShell 5.1+ (já incluído no Windows 10/11)
- **Linux/macOS**: `curl` e `unzip` (geralmente já instalados)

## 🔧 Problemas Comuns

**`coral` não é reconhecido:**
- Use `python coral.py ...` como alternativa
- Verifique se reabriu o terminal após a instalação

**Python não encontrado:**
- Verifique com `python --version` ou tente `py` / `python3`
- Instale Python 3.7+ se necessário

**Arquivo não encontrado:**
- Verifique o caminho do arquivo `.crl`
- Use caminhos absolutos ou relativos corretos