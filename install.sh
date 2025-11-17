#!/bin/bash
# Instalador do Coral Language para Linux/macOS
# Execute: curl -fsSL https://raw.githubusercontent.com/GabrielVerri/Coral_project/dev/install.sh | bash

set -e

echo ""
echo "=== Coral Language - Instalador ==="
echo ""

# Configurações
REPO="https://github.com/GabrielVerri/Coral_project/archive/refs/heads/dev.zip"
ZIP="/tmp/coral.zip"
DIR="$HOME/CoralLanguage"
TMP="/tmp/Coral_project-dev"

# Detectar SO
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
    UNZIP_CMD="unzip"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
    UNZIP_CMD="unzip"
else
    echo "Sistema operacional não suportado: $OSTYPE"
    exit 1
fi

echo "Sistema detectado: $OS"

# Verificar dependências
if ! command -v curl &> /dev/null; then
    echo "ERRO: curl não encontrado. Instale com:"
    echo "  sudo apt install curl  # Ubuntu/Debian"
    echo "  sudo yum install curl  # CentOS/RHEL"
    echo "  brew install curl      # macOS"
    exit 1
fi

if ! command -v unzip &> /dev/null; then
    echo "ERRO: unzip não encontrado. Instale com:"
    echo "  sudo apt install unzip  # Ubuntu/Debian"
    echo "  sudo yum install unzip  # CentOS/RHEL"
    echo "  brew install unzip      # macOS"
    exit 1
fi

echo "Baixando..."
curl -fsSL "$REPO" -o "$ZIP"

echo "Instalando..."
[ -d "$DIR" ] && rm -rf "$DIR"
[ -d "$TMP" ] && rm -rf "$TMP"
unzip -q "$ZIP" -d /tmp
mv "$TMP" "$DIR"
rm -f "$ZIP"

echo "Configurando PATH..."
SCRIPTS_DIR="$DIR/scripts"

# Detecta o shell
SHELL_RC=""
if [ -n "$BASH_VERSION" ]; then
    SHELL_RC="$HOME/.bashrc"
elif [ -n "$ZSH_VERSION" ]; then
    SHELL_RC="$HOME/.zshrc"
else
    SHELL_RC="$HOME/.profile"
fi

# Verifica se já está no PATH
if ! grep -q "CoralLanguage/scripts" "$SHELL_RC" 2>/dev/null; then
    echo "" >> "$SHELL_RC"
    echo "# Coral Language" >> "$SHELL_RC"
    echo "export PATH=\"\$PATH:$SCRIPTS_DIR\"" >> "$SHELL_RC"
fi

# Tornar scripts executáveis
chmod +x "$SCRIPTS_DIR/coral"
chmod +x "$SCRIPTS_DIR/coral.sh" 2>/dev/null || true

echo ""
echo "=== Instalado com sucesso! ==="
echo "Localização: $DIR"
echo ""
echo "Recarregue o terminal ou execute:"
echo "  source $SHELL_RC"
echo ""