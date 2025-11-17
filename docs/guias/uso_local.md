# Guia de Uso Local - Coral (Windows, Linux e macOS)

Este guia mostra como **rodar o Coral localmente** usando Python.

## Passo 1: Clonar o repositório

```bash
git clone https://github.com/GabrielVerri/Coral_project.git
cd Coral_project
```

## Passo 2: Criar um arquivo `.crl`

### Windows (PowerShell / CMD)

```powershell
notepad meu_programa.crl
```

No arquivo, escreva algo como:

```coral
ESCREVA("Olá, Coral!")
```

Salve e feche o editor.

### Linux / macOS (terminal)

```bash
nano meu_programa.crl
```

No arquivo, escreva algo como:

```coral
ESCREVA("Olá, Coral!")
```

Salve (`Ctrl+O`, `Enter`) e saia (`Ctrl+X`).

## Passo 3: Executar o arquivo

### Windows

```bash
python coral.py meu_programa.crl
```

### Linux / macOS

```bash
python3 coral.py meu_programa.crl
```

