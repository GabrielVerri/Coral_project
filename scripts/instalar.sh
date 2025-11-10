#!/bin/bash
# Script de Instalação do Coral para Linux/Mac
# Cria um link simbólico em /usr/local/bin para usar 'coral' de qualquer lugar

echo "========================================"
echo "  Instalador Coral Language"
echo "========================================"
echo ""

# Obtém o diretório raiz do projeto (um nível acima de scripts/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CORAL_DIR="$(dirname "$SCRIPT_DIR")"
CORAL_SCRIPT="$SCRIPT_DIR/coral"

echo "Diretório Coral: $CORAL_DIR"
echo ""

# Verifica se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "[ERRO] Python3 não encontrado!"
    echo "Por favor, instale Python 3.7+ antes de continuar."
    echo "Ubuntu/Debian: sudo apt install python3"
    echo "Fedora: sudo dnf install python3"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "[OK] Python encontrado: $PYTHON_VERSION"
echo ""

# Torna o script executável
chmod +x "$CORAL_SCRIPT"
echo "[OK] Script tornado executável"
echo ""

# Verifica se /usr/local/bin existe
if [ ! -d "/usr/local/bin" ]; then
    echo "[ERRO] Diretório /usr/local/bin não existe"
    exit 1
fi

# Cria link simbólico
echo "Criando link simbólico em /usr/local/bin..."
echo "Pode ser necessário senha de administrador (sudo)"
echo ""

sudo ln -sf "$CORAL_SCRIPT" /usr/local/bin/coral

if [ $? -eq 0 ]; then
    echo "[OK] Link simbólico criado com sucesso!"
    echo ""
    echo "========================================"
    echo "  Instalação Concluída!"
    echo "========================================"
    echo ""
    echo "Agora você pode usar 'coral' de qualquer lugar!"
    echo ""
    echo "Exemplos:"
    echo "  coral meu_programa.crl"
    echo "  coral --help"
    echo "  coral --version"
    echo ""
    echo "Para criar um arquivo:"
    echo "  nano meu_programa.crl"
    echo "  coral meu_programa.crl"
    echo ""
else
    echo "[ERRO] Falha ao criar link simbólico"
    echo ""
    echo "Alternativa: Adicione ao PATH manualmente"
    echo "Adicione esta linha ao seu ~/.bashrc ou ~/.zshrc:"
    echo ""
    echo "export PATH=\"\$PATH:$CORAL_DIR\""
    echo ""
    exit 1
fi
