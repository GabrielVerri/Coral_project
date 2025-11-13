@echo off
REM Instalador do Coral Language para Windows
REM Adiciona o comando 'coral' ao PATH do sistema

echo ========================================
echo   Instalador Coral Language
echo ========================================
echo.

REM Obtém o diretório atual (onde está o projeto)
set CORAL_DIR=%~dp0
set CORAL_SCRIPTS=%CORAL_DIR%scripts

echo Diretorio do Coral: %CORAL_DIR%
echo Diretorio scripts: %CORAL_SCRIPTS%
echo.

REM Verifica se coral.bat existe
if not exist "%CORAL_SCRIPTS%\coral.bat" (
    echo ERRO: Arquivo coral.bat nao encontrado em scripts/
    echo.
    pause
    exit /b 1
)

echo Deseja adicionar o Coral ao PATH do usuario? (S/N)
set /p RESPOSTA=

if /i "%RESPOSTA%" NEQ "S" (
    echo Instalacao cancelada.
    echo.
    echo Voce pode executar Coral usando:
    echo   python coral.py arquivo.crl
    echo.
    pause
    exit /b 0
)

echo.
echo Adicionando %CORAL_SCRIPTS% ao PATH...

REM Adiciona ao PATH do usuário usando PowerShell
powershell -Command "[Environment]::SetEnvironmentVariable('Path', [Environment]::GetEnvironmentVariable('Path', 'User') + ';%CORAL_SCRIPTS%', 'User')"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   Coral instalado com sucesso!
    echo ========================================
    echo.
    echo IMPORTANTE: Feche e reabra o terminal para usar o comando 'coral'
    echo.
    echo Uso:
    echo   coral arquivo.crl
    echo   coral --lex arquivo.crl
    echo   coral --parse arquivo.crl
    echo.
) else (
    echo.
    echo ERRO: Falha ao adicionar ao PATH
    echo Tente executar este script como Administrador
    echo.
)

pause
