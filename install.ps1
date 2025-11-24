# Instalador One-Line do Coral Language
# Execute no PowerShell: irm https://raw.githubusercontent.com/GabrielVerri/Coral_project/dev/install.ps1 | iex

$ErrorActionPreference = "Stop"

Write-Host "`n=== Coral Language - Instalador ===" -ForegroundColor Cyan

# Configurações
$repo = "https://github.com/GabrielVerri/Coral_project/archive/refs/heads/dev.zip"
$zip = "$env:TEMP\coral.zip"
$dir = "$env:USERPROFILE\CoralLanguage"
$tmp = "$env:TEMP\Coral_project-dev"

Write-Host "Baixando..." -ForegroundColor Yellow
Invoke-WebRequest -Uri $repo -OutFile $zip -UseBasicParsing

Write-Host "Instalando..." -ForegroundColor Yellow
if (Test-Path $dir) { Remove-Item $dir -Recurse -Force }
if (Test-Path $tmp) { Remove-Item $tmp -Recurse -Force }
Expand-Archive -Path $zip -DestinationPath $env:TEMP -Force
Move-Item $tmp $dir -Force
Remove-Item $zip -Force

Write-Host "Configurando PATH..." -ForegroundColor Yellow
$scripts = "$dir\scripts"
$path = [Environment]::GetEnvironmentVariable("Path", "User")
if ($path -notlike "*$scripts*") {
    [Environment]::SetEnvironmentVariable("Path", "$path;$scripts", "User")
}

Write-Host "`n=== Instalado com sucesso! ===" -ForegroundColor Green
Write-Host "Localização: $dir" -ForegroundColor Cyan
Write-Host "`nFeche e reabra o terminal, depois use:" -ForegroundColor Yellow