# Desinstalador do Coral Language
# Remove automaticamente o Coral de qualquer localização

$ErrorActionPreference = "Stop"

Write-Host "`n=== Coral Language - Desinstalador ===" -ForegroundColor Cyan

# Detecta onde o Coral está instalado verificando o PATH
$path = [System.Environment]::GetEnvironmentVariable('Path', 'User')
$coralPaths = $path -split ';' | Where-Object { $_ -like '*Coral*' }

if ($coralPaths.Count -eq 0) {
    Write-Host "`nCoral não encontrado no PATH." -ForegroundColor Yellow
    Write-Host "O Coral pode não estar instalado ou já foi removido." -ForegroundColor Yellow
    exit 0
}

Write-Host "`nLocalizações encontradas:" -ForegroundColor Yellow
$coralPaths | ForEach-Object { Write-Host "  - $_" -ForegroundColor Gray }

# Remove todas as entradas do Coral do PATH
Write-Host "`nRemovendo do PATH..." -ForegroundColor Yellow
$newPath = ($path -split ';' | Where-Object { $_ -notlike '*Coral*' }) -join ';'
[System.Environment]::SetEnvironmentVariable('Path', $newPath, 'User')

# Tenta encontrar e deletar os diretórios de instalação
$deleted = $false
foreach ($coralPath in $coralPaths) {
    # Remove '\scripts' do final para pegar o diretório raiz
    $rootDir = $coralPath -replace '\\scripts$', ''
    
    if (Test-Path $rootDir) {
        Write-Host "Removendo diretório: $rootDir" -ForegroundColor Yellow
        try {
            Remove-Item -Recurse -Force $rootDir
            Write-Host "  ✓ Removido com sucesso" -ForegroundColor Green
            $deleted = $true
        } catch {
            Write-Host "  ✗ Erro ao remover: $_" -ForegroundColor Red
            Write-Host "  Tente deletar manualmente: $rootDir" -ForegroundColor Yellow
        }
    }
}

if ($deleted) {
    Write-Host "`n=== Coral desinstalado com sucesso! ===" -ForegroundColor Green
} else {
    Write-Host "`n=== PATH limpo! ===" -ForegroundColor Green
    Write-Host "Se necessário, delete manualmente as pastas listadas acima." -ForegroundColor Yellow
}

Write-Host "`nFeche e reabra o terminal para aplicar as mudanças." -ForegroundColor Cyan
