@echo off
REM Script de instalação do Coral para Windows
REM Adiciona a pasta scripts ao PATH do usuário

echo ========================================
echo Instalador Coral Language
echo ========================================
echo.

REM Obtém o diretório atual (pasta scripts)
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

echo Diretorio de instalacao: %SCRIPT_DIR%
echo.

REM Verifica se o PATH já contém o diretório
echo %PATH% | findstr /C:"%SCRIPT_DIR%" >nul
if %errorlevel% equ 0 (
    echo [OK] O diretorio ja esta no PATH!
    echo.
    goto :test
)

echo Adicionando ao PATH do usuario...
echo.

REM Adiciona ao PATH do usuário (registro)
for /f "skip=2 tokens=3*" %%a in ('reg query HKCU\Environment /v PATH 2^>nul') do set "USER_PATH=%%a %%b"

REM Remove espaços extras
set "USER_PATH=%USER_PATH:  = %"

REM Verifica se já existe no registro
echo %USER_PATH% | findstr /C:"%SCRIPT_DIR%" >nul
if %errorlevel% equ 0 (
    echo [OK] Ja esta configurado no registro!
    echo.
    goto :refresh
)

REM Adiciona ao PATH
if "%USER_PATH%"=="" (
    setx PATH "%SCRIPT_DIR%"
) else (
    setx PATH "%USER_PATH%;%SCRIPT_DIR%"
)

if %errorlevel% equ 0 (
    echo [OK] PATH atualizado com sucesso!
    echo.
) else (
    echo [ERRO] Falha ao atualizar PATH
    echo Tente executar como Administrador
    pause
    exit /b 1
)

:refresh
echo ========================================
echo Instalacao concluida!
echo ========================================
echo.
echo IMPORTANTE: Feche e reabra o terminal para aplicar as mudancas.
echo.
echo Apos reabrir o terminal, voce pode usar:
echo   coral meu_programa.crl
echo.

:test
echo Testando instalacao...
echo.
where coral.bat >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Comando 'coral' encontrado!
    echo.
    echo Teste: coral --version
    call coral.bat --version
) else (
    echo [AVISO] Comando 'coral' ainda nao esta disponivel.
    echo Feche e reabra o terminal para que as mudancas tenham efeito.
)

echo.
pause
