; Código LLVM IR gerado pelo Coral Compiler
; Linguagem Coral - https://github.com/GabrielVerri/Coral_project

target triple = "x86_64-pc-windows-msvc"

; Strings globais
@.str.0 = private unnamed_addr constant [20 x i8] c"Contagem de 0 a 4:\0A\00", align 1
@.str.1 = private unnamed_addr constant [20 x i8] c"Contagem de 1 a 5:\0A\00", align 1
@.str.2 = private unnamed_addr constant [21 x i8] c"Contagem de 2 em 2:\0A\00", align 1

; Declarações de funções externas
declare i32 @printf(i8*, ...)

define i32 @main() {
  entry:
    %t0 = getelementptr inbounds [20 x i8], [20 x i8]* @.str.0, i32 0, i32 0
    %t1 = call i32 (i8*, ...) @printf(i8* %t0)
    %t2 = alloca i32, align 4
    store i32 0, i32* %t2, align 4
    br label %for_cond0
  for_cond0:
    %t3 = load i32, i32* %t2, align 4
    %t4 = icmp slt i32 %t3, 5
    br i1 %t4, label %for_body1, label %for_end3
  for_body1:
    br label %for_inc2
  for_inc2:
    %t5 = load i32, i32* %t2, align 4
    %t6 = add nsw i32 %t5, 1
    store i32 %t6, i32* %t2, align 4
    br label %for_cond0
  for_end3:
    %t7 = getelementptr inbounds [20 x i8], [20 x i8]* @.str.1, i32 0, i32 0
    %t8 = call i32 (i8*, ...) @printf(i8* %t7)
    %t9 = alloca i32, align 4
    store i32 1, i32* %t9, align 4
    br label %for_cond4
  for_cond4:
    %t10 = load i32, i32* %t9, align 4
    %t11 = icmp slt i32 %t10, 6
    br i1 %t11, label %for_body5, label %for_end7
  for_body5:
    br label %for_inc6
  for_inc6:
    %t12 = load i32, i32* %t9, align 4
    %t13 = add nsw i32 %t12, 1
    store i32 %t13, i32* %t9, align 4
    br label %for_cond4
  for_end7:
    %t14 = getelementptr inbounds [21 x i8], [21 x i8]* @.str.2, i32 0, i32 0
    %t15 = call i32 (i8*, ...) @printf(i8* %t14)
    %t16 = alloca i32, align 4
    store i32 0, i32* %t16, align 4
    br label %for_cond8
  for_cond8:
    %t17 = load i32, i32* %t16, align 4
    %t18 = icmp slt i32 %t17, 10
    br i1 %t18, label %for_body9, label %for_end11
  for_body9:
    br label %for_inc10
  for_inc10:
    %t19 = load i32, i32* %t16, align 4
    %t20 = add nsw i32 %t19, 2
    store i32 %t20, i32* %t16, align 4
    br label %for_cond8
  for_end11:
    ret i32 0
}