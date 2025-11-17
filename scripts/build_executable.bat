@echo off
echo ========================================
echo   Coral Language - Build Executable
echo ========================================
echo.

echo Gerando executavel...
pyinstaller --clean coral.spec

echo.
echo ========================================
echo Executavel gerado com sucesso!
echo Local: dist\coral.exe
echo ========================================
echo.
echo Para testar:
echo   dist\coral.exe exemplos\parser\ola_mundo.crl
echo.
pause
