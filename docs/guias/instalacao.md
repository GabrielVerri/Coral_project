# Coral Language - Instalação

Este guia mostra como **instalar o comando `coral`** no seu sistema.
Para aprender a rodar exemplos, criar arquivos `.crl` ou executar o
projeto localmente com Python, veja `docs/guias/uso_local.md`.

## Instalação Rápida (Recomendado)

### Windows (PowerShell)
```powershell
irm https://raw.githubusercontent.com/GabrielVerri/Coral_project/dev/install.ps1 | iex
```

### Windows (CMD)
```cmd
powershell -ExecutionPolicy Bypass -Command "irm https://raw.githubusercontent.com/GabrielVerri/Coral_project/dev/install.ps1 | iex"
```

### Linux / macOS (Bash)
```bash
curl -fsSL https://raw.githubusercontent.com/GabrielVerri/Coral_project/dev/install.sh | bash
```

**O que isso faz (fluxo recomendado):**
- Baixa automaticamente o projeto do GitHub
- Instala em `~/CoralLanguage` (Linux/Mac) ou `%USERPROFILE%\CoralLanguage` (Windows)
- Adiciona o comando `coral` ao PATH

> Esta é a forma recomendada para quem quer **usar a linguagem Coral**.
> Não é necessário clonar o repositório para programar em Coral.

**Após a instalação:**
- **Windows**: Feche e reabra o terminal
- **Linux/macOS**: Execute `source ~/.bashrc` (ou `~/.zshrc`)

## Desinstalação

### Windows (PowerShell)
```powershell
irm https://raw.githubusercontent.com/GabrielVerri/Coral_project/dev/uninstall.ps1 | iex
```

### Linux / macOS
```bash
# Remove do PATH (edite ~/.bashrc ou ~/.zshrc)
sed -i '/CoralLanguage/d' ~/.bashrc  # ou ~/.zshrc
source ~/.bashrc

# Delete a pasta
rm -rf ~/CoralLanguage
```

**Após desinstalar:** Feche e reabra o terminal. O comando `coral` não funcionará mais.

## Requisitos

- **Python**: 3.7 ou superior
- **Windows**: PowerShell 5.1+ (já incluído no Windows 10/11)
- **Linux/macOS**: `curl` e `unzip` (geralmente já instalados)

Se, após a instalação, o comando `coral` não for reconhecido, feche e
reabra o terminal. Para exemplos de uso e execução local com Python,
consulte `docs/guias/uso_local.md`.