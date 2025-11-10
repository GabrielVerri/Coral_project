# Guia de Instalação e Uso - Coral no Linux

## Instalação Rápida

### Passo 1: Clone o repositório
```bash
git clone https://github.com/GabrielVerri/Coral_project.git
cd Coral_project
```

### Passo 2: Execute o instalador
```bash
chmod +x instalar.sh
./instalar.sh
```

Pronto! Agora você pode usar `coral` de qualquer lugar.

---

## Como Usar

### 1. Criar um arquivo Coral

```bash
# Usando nano (recomendado para iniciantes)
nano meu_programa.crl
```

Escreva seu código:
```coral
ESCREVA("Olá, Coral!")

x = 10
y = 5
soma = x + y
ESCREVA("A soma é:", soma)
```

**Salvar:** `Ctrl+O` → `Enter`
**Sair:** `Ctrl+X`

### 2. Executar o programa

```bash
coral meu_programa.crl
```

**Saída:**
```
======================================================================
Coral Language Interpreter v0.1.0
======================================================================

Olá, Coral!
A soma é: 15
```

---

## Exemplos Rápidos

### Exemplo 1: Hello World (uma linha)
```bash
echo 'ESCREVA("Olá, Mundo!")' > hello.crl
coral hello.crl
```

### Exemplo 2: Calculadora
```bash
cat > calc.crl << 'EOF'
a = 10
b = 3

ESCREVA("Soma:", a + b)
ESCREVA("Subtração:", a - b)
ESCREVA("Multiplicação:", a * b)
ESCREVA("Divisão:", a / b)
ESCREVA("Potência:", a ** b)
EOF

coral calc.crl
```

### Exemplo 3: Função
```bash
cat > funcao.crl << 'EOF'
FUNCAO dobro(n):
    RETORNAR n * 2

num = 5
resultado = dobro(num)
ESCREVA("O dobro de", num, "é:", resultado)
EOF

coral funcao.crl
```

### Exemplo 4: Condicional
```bash
cat > idade.crl << 'EOF'
idade = 18

SE idade >= 18:
    ESCREVA("Você é maior de idade")
SENAO:
    ESCREVA("Você é menor de idade")
EOF

coral idade.crl
```

### Exemplo 5: Laço
```bash
cat > contador.crl << 'EOF'
ESCREVA("Contando de 1 a 5:")

contador = 1
ENQUANTO contador <= 5:
    ESCREVA("Número:", contador)
    contador = contador + 1

ESCREVA("Fim!")
EOF

coral contador.crl
```

---

## Workflow Típico

```bash
# 1. Criar arquivo
nano meu_programa.crl

# 2. Executar
coral meu_programa.crl

# 3. Ver apenas a AST (estrutura)
coral --ast meu_programa.crl

# 4. Ver apenas tokens
coral --lex meu_programa.crl

# 5. Ver ajuda
coral --help
```

---

## Comandos Úteis

### Executar programa
```bash
coral programa.crl
```

### Ver apenas análise léxica (tokens)
```bash
coral --lex programa.crl
```

### Ver apenas análise sintática (sem executar)
```bash
coral --parse programa.crl
```

### Ver a Árvore Sintática Abstrata (AST)
```bash
coral --ast programa.crl
```

### Ver versão
```bash
coral --version
```

### Ver ajuda
```bash
coral --help
```

---

## Organização Recomendada

```bash
# Criar pasta para seus programas
mkdir ~/meus-programas-coral
cd ~/meus-programas-coral

# Criar e executar
nano teste.crl
coral teste.crl
```

---

## Instalação Manual (sem sudo)

Se você não tem permissão de sudo, adicione ao PATH manualmente:

### Para Bash (~/.bashrc):
```bash
echo 'export PATH="$PATH:/caminho/completo/para/Coral_project"' >> ~/.bashrc
source ~/.bashrc
```

### Para Zsh (~/.zshrc):
```bash
echo 'export PATH="$PATH:/caminho/completo/para/Coral_project"' >> ~/.zshrc
source ~/.zshrc
```

Depois, torne o script executável:
```bash
chmod +x /caminho/para/Coral_project/coral
```

---

## Testar Instalação

```bash
# Verificar se coral está disponível
which coral

# Testar com exemplo
coral exemplos/parser/ola_mundo.crl
```

---

## Solução de Problemas

### "coral: command not found"

**Opção 1:** Recarregue o terminal
```bash
source ~/.bashrc  # ou ~/.zshrc
```

**Opção 2:** Abra um novo terminal

**Opção 3:** Use o caminho completo
```bash
./coral meu_programa.crl  # se estiver na pasta do Coral
```

### "Permission denied"

Torne o script executável:
```bash
chmod +x coral
chmod +x instalar.sh
```

### Python não encontrado

Instale Python 3:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3

# Fedora
sudo dnf install python3

# Arch
sudo pacman -S python
```

---

## Dicas

- Use `nano` para editar (mais simples)
- Use `vim` ou `emacs` se preferir
- VS Code também funciona: `code programa.crl`
- Extensão `.crl` é obrigatória
- Indentação é importante (4 espaços ou tab)
- Use `#` para comentários

---

## Exemplos Prontos

Teste os exemplos incluídos:
```bash
coral exemplos/parser/ola_mundo.crl
coral exemplos/parser/funcoes.crl
coral exemplos/parser/lacos.crl
coral exemplos/parser/estrutura_se.crl
```

---

## Próximos Passos

1. Instale o Coral: `./instalar.sh`
2. Crie seu primeiro programa: `nano hello.crl`
3. Execute: `coral hello.crl`
4. Explore os exemplos
5. Leia a [documentação completa](README.md)

---

## Precisa de Ajuda?

```bash
coral --help
```

Ou visite: [GitHub - Coral Project](https://github.com/GabrielVerri/Coral_project)

