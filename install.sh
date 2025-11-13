#!/bin/bash
# Instalador do Coral Language para Linux/Mac
# Adiciona o comando 'coral' ao PATH do sistema

echo "========================================"
echo "  Instalador Coral Language"
echo "========================================"
echo

# Obtém o diretório do projeto
CORAL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CORAL_SCRIPTS="$CORAL_DIR/scripts"

echo "Diretório do Coral: $CORAL_DIR"
echo "Diretório scripts: $CORAL_SCRIPTS"
echo

# Verifica se o script coral existe
if [ ! -f "$CORAL_SCRIPTS/coral" ]; then
    echo "ERRO: Arquivo coral não encontrado em scripts/"
    echo
    exit 1
fi

# Torna o script executável
chmod +x "$CORAL_SCRIPTS/coral"

echo "Deseja adicionar o Coral ao PATH? (s/n)"
read -r RESPOSTA

if [ "$RESPOSTA" != "s" ] && [ "$RESPOSTA" != "S" ]; then
    echo "Instalação cancelada."
    echo
    echo "Você pode executar Coral usando:"
    echo "  python3 coral.py arquivo.crl"
    echo
    exit 0
fi

echo
echo "Adicionando ao PATH..."

# Detecta o shell
if [ -n "$BASH_VERSION" ]; then
    SHELL_RC="$HOME/.bashrc"
elif [ -n "$ZSH_VERSION" ]; then
    SHELL_RC="$HOME/.zshrc"
else
    SHELL_RC="$HOME/.profile"
fi

# Verifica se já está no PATH
if grep -q "CORAL_PROJECT" "$SHELL_RC" 2>/dev/null; then
    echo "Coral já está configurado em $SHELL_RC"
else
    echo >> "$SHELL_RC"
    echo "# Coral Programming Language" >> "$SHELL_RC"
    echo "export PATH=\"\$PATH:$CORAL_SCRIPTS\" # CORAL_PROJECT" >> "$SHELL_RC"
    echo "Adicionado ao $SHELL_RC"
fi

echo
echo "========================================"
echo "  Coral instalado com sucesso!"
echo "========================================"
echo
echo "IMPORTANTE: Execute o comando abaixo ou reabra o terminal:"
echo "  source $SHELL_RC"
echo
echo "Uso:"
echo "  coral arquivo.crl"
echo "  coral --lex arquivo.crl"
echo "  coral --parse arquivo.crl"
echo
