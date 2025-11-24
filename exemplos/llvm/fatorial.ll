; Código LLVM IR gerado pelo Coral Compiler
; Linguagem Coral - https://github.com/GabrielVerri/Coral_project

target triple = "x86_64-pc-windows-msvc"

; Strings globais
@.str.0 = private unnamed_addr constant [25 x i8] c"Calculando fatorial de:\0A\00", align 1
@.str.1 = private unnamed_addr constant [12 x i8] c"Resultado:\0A\00", align 1

; Declarações de funções externas
declare i32 @printf(i8*, ...)

define i32 @main() {
  entry:
    %t0 = alloca i32, align 4
    store i32 5, i32* %t0, align 4
    %t1 = alloca i32, align 4
    store i32 1, i32* %t1, align 4
    %t2 = alloca i32, align 4
    store i32 1, i32* %t2, align 4
    %t3 = getelementptr inbounds [25 x i8], [25 x i8]* @.str.0, i32 0, i32 0
    %t4 = call i32 (i8*, ...) @printf(i8* %t3)
    %t5 = load i32, i32* %t0, align 4
    %t6 = getelementptr inbounds [4 x i8], [4 x i8]* @.str.2, i32 0, i32 0
    %t7 = call i32 (i8*, ...) @printf(i8* %t6, i32 %t5)
    br label %while_cond0
  while_cond0:
    %t8 = load i32, i32* %t2, align 4
    %t9 = load i32, i32* %t0, align 4
    %t10 = icmp sle i32 %t8, %t9
    br i1 %t10, label %while_body1, label %while_end2
  while_body1:
    %t11 = load i32, i32* %t1, align 4
    %t12 = load i32, i32* %t2, align 4
    %t13 = mul nsw i32 %t11, %t12
    store i32 %t13, i32* %t1, align 4
    %t14 = load i32, i32* %t2, align 4
    %t15 = add nsw i32 %t14, 1
    store i32 %t15, i32* %t2, align 4
    br label %while_cond0
  while_end2:
    %t16 = getelementptr inbounds [12 x i8], [12 x i8]* @.str.1, i32 0, i32 0
    %t17 = call i32 (i8*, ...) @printf(i8* %t16)
    %t18 = load i32, i32* %t1, align 4
    %t19 = getelementptr inbounds [4 x i8], [4 x i8]* @.str.2, i32 0, i32 0
    %t20 = call i32 (i8*, ...) @printf(i8* %t19, i32 %t18)
    ret i32 0
}