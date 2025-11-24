; Código LLVM IR gerado pelo Coral Compiler
; Linguagem Coral - https://github.com/GabrielVerri/Coral_project

target triple = "x86_64-pc-windows-msvc"

; Strings globais
@.str.0 = private unnamed_addr constant [20 x i8] c"Resultado da soma:\0A\00", align 1
@.str.1 = private unnamed_addr constant [21 x i8] c"Dobro do resultado:\0A\00", align 1
@.str.2 = private unnamed_addr constant [16 x i8] c"Subtraindo 15:\0A\00", align 1

; Declarações de funções externas
declare i32 @printf(i8*, ...)

define i32 @main() {
  entry:
    %t0 = alloca i32, align 4
    store i32 10, i32* %t0, align 4
    %t1 = alloca i32, align 4
    store i32 20, i32* %t1, align 4
    %t2 = load i32, i32* %t0, align 4
    %t3 = load i32, i32* %t1, align 4
    %t4 = add nsw i32 %t2, %t3
    %t5 = alloca i32, align 4
    store i32 %t4, i32* %t5, align 4
    %t6 = getelementptr inbounds [20 x i8], [20 x i8]* @.str.0, i32 0, i32 0
    %t7 = call i32 (i8*, ...) @printf(i8* %t6)
    %t8 = load i32, i32* %t5, align 4
    %t9 = getelementptr inbounds [4 x i8], [4 x i8]* @.str.3, i32 0, i32 0
    %t10 = call i32 (i8*, ...) @printf(i8* %t9, i32 %t8)
    %t11 = load i32, i32* %t5, align 4
    %t12 = mul nsw i32 %t11, 2
    %t13 = alloca i32, align 4
    store i32 %t12, i32* %t13, align 4
    %t14 = getelementptr inbounds [21 x i8], [21 x i8]* @.str.1, i32 0, i32 0
    %t15 = call i32 (i8*, ...) @printf(i8* %t14)
    %t16 = load i32, i32* %t13, align 4
    %t17 = getelementptr inbounds [4 x i8], [4 x i8]* @.str.3, i32 0, i32 0
    %t18 = call i32 (i8*, ...) @printf(i8* %t17, i32 %t16)
    %t19 = load i32, i32* %t13, align 4
    %t20 = sub nsw i32 %t19, 15
    %t21 = alloca i32, align 4
    store i32 %t20, i32* %t21, align 4
    %t22 = getelementptr inbounds [16 x i8], [16 x i8]* @.str.2, i32 0, i32 0
    %t23 = call i32 (i8*, ...) @printf(i8* %t22)
    %t24 = load i32, i32* %t21, align 4
    %t25 = getelementptr inbounds [4 x i8], [4 x i8]* @.str.3, i32 0, i32 0
    %t26 = call i32 (i8*, ...) @printf(i8* %t25, i32 %t24)
    ret i32 0
}