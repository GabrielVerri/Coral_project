; Código LLVM IR gerado pelo Coral Compiler
; Linguagem Coral - https://github.com/GabrielVerri/Coral_project

target triple = "x86_64-pc-windows-msvc"

; Strings globais
@.str.0 = private unnamed_addr constant [17 x i8] c"Contando ate 5:\0A\00", align 1
@.str.1 = private unnamed_addr constant [17 x i8] c"Fim da contagem\0A\00", align 1

; Declarações de funções externas
declare i32 @printf(i8*, ...)

define i32 @main() {
  entry:
    %t0 = alloca i32, align 4
    store i32 1, i32* %t0, align 4
    %t1 = getelementptr inbounds [17 x i8], [17 x i8]* @.str.0, i32 0, i32 0
    %t2 = call i32 (i8*, ...) @printf(i8* %t1)
    br label %while_cond0
  while_cond0:
    %t3 = load i32, i32* %t0, align 4
    %t4 = icmp sle i32 %t3, 5
    br i1 %t4, label %while_body1, label %while_end2
  while_body1:
    %t5 = load i32, i32* %t0, align 4
    %t6 = getelementptr inbounds [4 x i8], [4 x i8]* @.str.2, i32 0, i32 0
    %t7 = call i32 (i8*, ...) @printf(i8* %t6, i32 %t5)
    %t8 = load i32, i32* %t0, align 4
    %t9 = add nsw i32 %t8, 1
    store i32 %t9, i32* %t0, align 4
    br label %while_cond0
  while_end2:
    %t10 = getelementptr inbounds [17 x i8], [17 x i8]* @.str.1, i32 0, i32 0
    %t11 = call i32 (i8*, ...) @printf(i8* %t10)
    ret i32 0
}