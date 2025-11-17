# Scripts do Coral Language

Esta pasta contém scripts auxiliares para instalação e build do projeto.

## Arquivos

### Instalação e Execução

- **`coral`** - Script shell para executar Coral no Linux/Mac
- **`coral.bat`** - Script batch para executar Coral no Windows
- **`../install.sh`** - Script de instalação automática para Linux/Mac (na raiz do projeto)

### Build de Executável

- **`build_executable.sh`** - Gera executável standalone no Linux/Mac
- **`build_executable.bat`** - Gera executável standalone no Windows

## Como Usar

### Linux/Mac

```bash
# Instalar (adiciona 'coral' ao PATH)
cd Coral_project
chmod +x install.sh
./install.sh

# Depois pode usar de qualquer lugar:
coral meu_programa.crl
```

### Windows

```bash
# Executar diretamente
scripts\coral.bat meu_programa.crl

# Ou adicionar a pasta scripts ao PATH do Windows
```

### Gerar Executável Standalone

```bash
# Linux/Mac
chmod +x scripts/build_executable.sh
./scripts/build_executable.sh

# Windows
scripts\build_executable.bat
```

O executável será gerado em `dist/coral.exe` (Windows) ou `dist/coral` (Linux/Mac).
