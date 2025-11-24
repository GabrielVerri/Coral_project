; Código LLVM IR gerado pelo Coral Compiler
; Linguagem Coral - https://github.com/GabrielVerri/Coral_project

target triple = "x86_64-pc-windows-msvc"

; Strings globais
@.str.0 = private unnamed_addr constant [20 x i8] c"Testando SE/SENAO:\0A\00", align 1
@.str.1 = private unnamed_addr constant [18 x i8] c"x eh maior que y\0A\00", align 1
@.str.2 = private unnamed_addr constant [22 x i8] c"x nao eh maior que y\0A\00", align 1
@.str.3 = private unnamed_addr constant [17 x i8] c"x eh igual a 10\0A\00", align 1
@.str.4 = private unnamed_addr constant [18 x i8] c"y eh menor que 3\0A\00", align 1
@.str.5 = private unnamed_addr constant [22 x i8] c"y nao eh menor que 3\0A\00", align 1

; Declarações de funções externas
declare i32 @printf(i8*, ...)

define i32 @main() {
  entry:
    %t0 = alloca i32, align 4
    store i32 10, i32* %t0, align 4
    %t1 = alloca i32, align 4
    store i32 5, i32* %t1, align 4
    %t2 = getelementptr inbounds [20 x i8], [20 x i8]* @.str.0, i32 0, i32 0
    %t3 = call i32 (i8*, ...) @printf(i8* %t2)
    %t4 = load i32, i32* %t0, align 4
    %t5 = load i32, i32* %t1, align 4
    %t6 = icmp sgt i32 %t4, %t5
    br i1 %t6, label %then0, label %else1
  then0:
    %t7 = getelementptr inbounds [18 x i8], [18 x i8]* @.str.1, i32 0, i32 0
    %t8 = call i32 (i8*, ...) @printf(i8* %t7)
    br label %endif2
  else1:
    %t9 = getelementptr inbounds [22 x i8], [22 x i8]* @.str.2, i32 0, i32 0
    %t10 = call i32 (i8*, ...) @printf(i8* %t9)
    br label %endif2
  endif2:
    %t11 = load i32, i32* %t0, align 4
    %t12 = icmp eq i32 %t11, 10
    br i1 %t12, label %then3, label %endif4
  then3:
    %t13 = getelementptr inbounds [17 x i8], [17 x i8]* @.str.3, i32 0, i32 0
    %t14 = call i32 (i8*, ...) @printf(i8* %t13)
    br label %endif4
  endif4:
    %t15 = load i32, i32* %t1, align 4
    %t16 = icmp slt i32 %t15, 3
    br i1 %t16, label %then5, label %else6
  then5:
    %t17 = getelementptr inbounds [18 x i8], [18 x i8]* @.str.4, i32 0, i32 0
    %t18 = call i32 (i8*, ...) @printf(i8* %t17)
    br label %endif7
  else6:
    %t19 = getelementptr inbounds [22 x i8], [22 x i8]* @.str.5, i32 0, i32 0
    %t20 = call i32 (i8*, ...) @printf(i8* %t19)
    br label %endif7
  endif7:
    ret i32 0
}