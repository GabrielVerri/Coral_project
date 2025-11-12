@echo off
REM Configura o ambiente Coral para a sessão atual
REM Execute: setup_env.bat

set "CORAL_DIR=%~dp0"
set "CORAL_DIR=%CORAL_DIR:~0,-1%"

REM Adiciona a pasta scripts ao PATH da sessão atual
set "PATH=%CORAL_DIR%\scripts;%PATH%"

echo ========================================
echo Coral Language - Ambiente Configurado
echo ========================================
echo.
echo Diretorio: %CORAL_DIR%
echo.
echo Comandos disponiveis:
echo   coral arquivo.crl        - Executa programa
echo   coral --cat arquivo.crl  - Mostra codigo
echo   coral --help             - Ajuda
echo.
echo O ambiente esta configurado para esta sessao.
echo Para usar em outras sessoes, execute novamente este script.
echo.
