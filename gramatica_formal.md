# **CORAL**

# **1\. Gramática formal da linguagem**

## **Alfabetos**

letras \= {a,...,z,A,...Z} (26 x 2 \= 52\)  
numeros \= {0,...,9}  
operador \= {+, −, \*, /, \=, \>, \<,\!}  
especial \= {espaco,newline,tab,underscore,{,},\[,\],%,&,(,),|,;,.,,}

## **Tokens**

Identificadores \= {(letras ∪ ‘\_‘) • (letras ∪ numeros ∪ ’\_’)\* }  
Operadores lógicos={E, OU, NAO}  
Operadores booleanos \= {VERDADE, FALSO}  
Operadores aritméticos relacionais \= (\\+\\+|\\+=|\\+|--|-=|-|\\\*\\\*|\\\*=|\\\*|/=|/|%=|%|==|\!=|\<=|\>=|=|\>|\<|\!)  
Comentários em linha  \= {\# • alfabetoCoral}  
string literal \= {“ • ((alfabetoCoral) \-(” ∪ newline))\* • “ ,’ • ((alfabetoCoral) \- (’ ∪ newline))\* • ‘,””” • ((alfabetoCoral) \-(”””))\* • ””” ,’’’• ((alfabetoCoral) \-(’’’))\* • ’’’,}  
decimal \= {numeros+  ∪ ‘.’ ∪ numeros+}  
Variaveis \= Identificadores

palavras reservadas={FALSO, ESPERA, SENAO, IMPORTAR, PASSAR, VAZIO, QUEBRA, EXCETO, DENTRODE, LANCAR, VERDADE, CLASSE, FINALMENTE, EIGUAL, RETORNAR, E, CONTINUA, PARA, LAMBDA, TENTE, COMO, DEF, DE, NAOLOCAL, ENQUANTO, AFIRMA, DELETAR, GLOBAL, NAO, COM, ASSINCRONO, SENAOSE, SE, OU, ENVIAR}

# **2\. Gramática livre de contexto**

Programa ⇒(Declaracao)\*

Declaracao ⇒ Expressao | EstruturaControle | Funcao | Classe

Expressao ⇒ Termo (OperadorAritimetico Termo)\*   
Termo ⇒ Fator (OperadorRelacional Fator)\*  
Fator ⇒ Identificador | Numero | Booleano | String | ‘(‘ Expressao ‘)’

EstruturaControle ⇒ SE  Expressao  Bloco   
        | SE Expressao’ Bloco SENAO Bloco   
        | Enquanto Expressao  Bloco   
        | PARA Identificador DENTRODE Expressao Bloco

Funcao ⇒Def Identificador ‘(‘ ListaParametros ‘)’ Bloco  
ListaParametros ⇒ Identificador  ( ‘,’ Identificador )\*

Classe ⇒ CLASSE Identificador Bloco

Bloco ⇒ ‘:’ IDENTA Declaracao\* DEDENTA

# **3\. Precedência e Associatividade**

1. OU  
2. E  
3. NAO (unário, mais alto uqe E/OU)  
4. Comparações : \== \!= \< \<= \> \>=  
5. Soma/Subtracao : \+ \- (esquerda)  
6. Produto/Divisao/Módulo \* / % (esquerda)  
7. Exponenciação: \*\* (direita)  
8. Unários: \+x \-x (direita na pratica pela gramatica)  
9. Acesso/Chamada/Indexacao

# **4\. Classificação na hierarquia de chomsky**

* **Léxico:** Linguagem regular (Tipo-3); Reconhecido por autômato finito (regex).Exemplos: identificadores, números, delimitadores, operadores.  
* **Sintaxe frasal:** Livre de contexto (Tipo-2); reconhecível por autômato de pilha. As construções como blocos aninhados e expressões com precedência são naturalmente CFL.

# **5\. Derivacoes**

## **5.1 Expressão aritimetica**

Entrada: a \+ b \* c \*\* d

1. Expressao ⇒ ExprOr ⇒ ExprAnd ⇒ ExprNot ⇒ ExprComparacao ⇒ ExprSoma  
2. ExprSoma ⇒ ExprProduto \+ ExprProduto  
3. O ExprProduto da direita: ⇒ ExprExpon \* ExprExpon  
4. O ExprExpon da direita: ⇒ ExprUnario \*\* ExprUnario ⇒ Primario \*\* Primario ⇒ Identificador \*\* Identificador  
5. Restante reduz a Identificador em cada posição.

A árvore reflete \*\* \> \* \> \+, com \*\* à direita.

## **5.2 Condicional com encadeamento**

Entrada:  
SE x \> 0:  
y \= 1  
SENAOSE x \== 0:  
y \= 0  
SENAO:  
y \= \-1

Derivação (alto nível):

- Comando ⇒ SE  
- Se ⇒ SE Expressao ":" Bloco { SENAOSE ... } \[ SENAO ... \]  
- Cada Bloco ⇒ newline INDENTA { Atribuicao } DEDENTA

A construção { SENAOSE ... } elimina o clássico dangling else.

# **5.3 Laço ENQUANTO**

Entrada:  
Enquanto i \< n:  
i \+= 1

* Comando ⇒ Enquanto  
* Enquanto ⇒ ENQUANTO Expressao ":" Bloco  
* Bloco ⇒ newline INDENTA { Atribuicao } DEDENTA

# **6\. Ambiguidades e estratégias de resolução**

1. **Precedência/associatividade de operadores**  
   Risco: a \+ b \* c ser lido como (a \+ b) \* c.  
   Estratégia: camadas ExprSoma/ExprProduto/ExprExpon já resolvem; teste com árvores.  
     
2. **Dangling else**  
   Risco: SENAO associar ao SE errado.  
   Estratégia: produção única Se com { SENAOSE ... } \[ SENAO ... \] evita ambiguidade.  
     
3. **Chamada/Acesso/Indexação**  
   Risco: colisão entre Identificador, Acesso, Chamada.  
   Estratégia: Primario \+ pós-fixes controlados (Acesso, Chamada, Indexacao) com maior amarração.  
     
4. **Indentação**  
   Risco: contagem de espaços/tabulações. Estratégia: lexer gera INDENTA/DEDENTA consistentes (pilha de níveis). Mistura de TAB/ESPAÇO proibida.  
   