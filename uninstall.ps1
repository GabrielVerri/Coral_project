# Desinstalador do Coral Language
# Remove automaticamente o Coral de qualquer localizacao

$ErrorActionPreference = "Stop"

Write-Host "
=== Coral Language - Desinstalador ===" -ForegroundColor Cyan

# Detecta onde o Coral esta instalado verificando o PATH
$path = [System.Environment]::GetEnvironmentVariable('Path', 'User')
$coralPaths = $path -split ';' | Where-Object { $_ -like '*Coral*' }

if ($coralPaths.Count -eq 0) {
    Write-Host "
Coral nao encontrado no PATH." -ForegroundColor Yellow
    Write-Host "O Coral pode nao estar instalado ou ja foi removido." -ForegroundColor Yellow
    exit 0
}

Write-Host "
Localizacoes encontradas:" -ForegroundColor Yellow
$coralPaths | ForEach-Object { Write-Host "  - $_" -ForegroundColor Gray }

# Remove todas as entradas do Coral do PATH
Write-Host "
Removendo do PATH..." -ForegroundColor Yellow
$newPath = ($path -split ';' | Where-Object { $_ -notlike '*Coral*' }) -join ';'
[System.Environment]::SetEnvironmentVariable('Path', $newPath, 'User')

# Tenta encontrar e deletar os diretorios de instalacao
$deleted = $false
foreach ($coralPath in $coralPaths) {
    # Remove '\scripts' do final para pegar o diretorio raiz
    $rootDir = $coralPath -replace '\\scripts$', ''
    
    if (Test-Path $rootDir) {
        Write-Host "Removendo diretorio: $rootDir" -ForegroundColor Yellow
        try {
            Remove-Item -Recurse -Force $rootDir
            Write-Host "  OK Removido com sucesso" -ForegroundColor Green
            $deleted = $true
        } catch {
            Write-Host "  ERRO ao remover: $_" -ForegroundColor Red
            Write-Host "  Tente deletar manualmente: $rootDir" -ForegroundColor Yellow
        }
    }
}

if ($deleted) {
    Write-Host "
=== Coral desinstalado com sucesso! ===" -ForegroundColor Green
} else {
    Write-Host "
=== PATH limpo! ===" -ForegroundColor Green
    Write-Host "Se necessario, delete manualmente as pastas listadas acima." -ForegroundColor Yellow
}

Write-Host "
Feche e reabra o terminal para aplicar as mudancas." -ForegroundColor Cyan
