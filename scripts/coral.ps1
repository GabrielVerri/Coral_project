# Executável Coral para Windows (PowerShell)
# Uso: coral <arquivo.crl> [opções]

$ErrorActionPreference = "Stop"

# Detecta o diretório do projeto (um nível acima de scripts)
$CoralRoot = Split-Path -Parent $PSScriptRoot

# Verifica se Python está disponível
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Erro: Python não encontrado. Instale Python 3.7+ e adicione ao PATH." -ForegroundColor Red
    exit 1
}

# Executa o interpretador Coral
& python "$CoralRoot\coral.py" @args
