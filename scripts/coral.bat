@echo off
REM Executável Coral para Windows
REM Uso: coral.bat <arquivo.crl> [opções]

REM Detecta o diretório do projeto (um nível acima de scripts)
set "CORAL_ROOT=%~dp0.."

REM Verifica se Python está disponível
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Erro: Python nao encontrado. Instale Python 3.7+ e adicione ao PATH.
    exit /b 1
)

REM Executa o interpretador Coral
python "%CORAL_ROOT%\coral.py" %*
