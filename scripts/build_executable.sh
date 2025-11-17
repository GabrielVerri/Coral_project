#!/bin/bash

echo "========================================"
echo "  Coral Language - Build Executable"
echo "========================================"
echo ""

echo "Gerando executável..."
pyinstaller --clean coral.spec

echo ""
echo "========================================"
echo "Executável gerado com sucesso!"
echo "Local: dist/coral"
echo "========================================"
echo ""
echo "Para testar:"
echo "  ./dist/coral exemplos/parser/ola_mundo.crl"
echo ""
