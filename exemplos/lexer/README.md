# Exemplos para Análise Léxica

Este diretório contém exemplos de código Coral para testar o analisador léxico.

## Arquivos

- `ola_mundo.crl`: Exemplo simples para testar reconhecimento básico de comandos
- `numeros_operacoes.crl`: Teste de números (inteiros/decimais) e operadores aritméticos
- `strings_comentarios.crl`: Teste de strings e comentários
- `operadores_logicos.crl`: Teste de operadores lógicos
- `operadores_relacionais.crl`: Teste de operadores de comparação
- `codigo.crl`: Exemplo completo com múltiplos tipos de tokens

## Casos de Teste

Cada arquivo foi criado para testar aspectos específicos do analisador léxico:

1. **Identificadores e Palavras Reservadas**
   - Uso de palavras reservadas (SE, ENTAO, SENAO, etc)
   - Identificadores válidos para variáveis

2. **Números**
   - Inteiros
   - Decimais
   - Operações matemáticas

3. **Strings e Comentários**
   - Strings com aspas simples e duplas
   - Comentários de linha
   - Strings com caracteres especiais

4. **Operadores**
   - Operadores aritméticos (+, -, *, /)
   - Operadores relacionais (>, <, >=, <=, ==)
   - Operadores lógicos (E, OU, NAO)

5. **Casos de Erro**
   - Tokens inválidos
   - Comandos não reconhecidos
   - Caracteres inválidos

## Como Usar

Execute o analisador léxico com qualquer um destes arquivos:

```bash
python src/lexer/main.py exemplos/lexer/nome_do_arquivo.crl
```