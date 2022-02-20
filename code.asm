@255
D = A
@SP
M = D
@RETURN.ADDRESS.0
D = A
@SP
AM = M + 1
M = D
@LCL
D = M
@SP
AM = M + 1
M = D
@ARG
D = M
@SP
AM = M + 1
M = D
@THIS
D = M
@SP
AM = M + 1
M = D
@THAT
D = M
@SP
AM = M + 1
M = D
@5
D = A
@SP
D = M - D
@ARG
M = D + 1
@SP
D = M
@LCL
M = D + 1
@main
0;JMP
(RETURN.ADDRESS.0)
@FUNCTION.main.END
0;JMP
(main)
@20
D = A
@SP
AM = M + 1
M = D
@3
D = A
@SP
AM = M + 1
M = D
@RETURN.ADDRESS.1
D = A
@SP
AM = M + 1
M = D
@LCL
D = M
@SP
AM = M + 1
M = D
@ARG
D = M
@SP
AM = M + 1
M = D
@THIS
D = M
@SP
AM = M + 1
M = D
@THAT
D = M
@SP
AM = M + 1
M = D
@7
D = A
@SP
D = M - D
@ARG
M = D + 1
@SP
D = M
@LCL
M = D + 1
@mult
0;JMP
(RETURN.ADDRESS.1)
@SP
M = M - 1
A = M + 1
D = M
M = 0
@16
M = D
@LCL
D = M
@R14
M = D
@5
D = A
@R14
D = M - D
A = D
D = M
@R15
M = D
@SP
A = M
D = M
@ARG
A = M
M = D
@ARG
D = M
@SP
M = D
@R14
A = M - 1
D = M
@THAT
M = D
@2
D = A
@R14
A = M - D
D = M
@THIS
M = D
@3
D = A
@R14
A = M - D
D = M
@ARG
M = D
@4
D = A
@R14
A = M - D
D = M
@LCL
M = D
@R15
A = M
0;JMP
(FUNCTION.main.END)
@FUNCTION.mult.END
0;JMP
(mult)
@0
D = A
@SP
AM = M + 1
M = D
@0
D = A
@SP
AM = M + 1
M = D
@SP
M = M - 1
A = M + 1
D = M
M = 0
@LCL
A = M
M = D
(loop)
@LCL
D = M
A = D
D = M
@SP
AM = M + 1
M = D
@ARG
D = M
A = D
D = M
@SP
AM = M + 1
M = D
@SP
M = M - 1
A = M + 1
D = M
M = 0
A = A - 1
M = M + D
@SP
M = M - 1
A = M + 1
D = M
M = 0
@LCL
A = M
M = D
@ARG
D = M
D = D + 1
A = D
D = M
@SP
AM = M + 1
M = D
@1
D = A
@SP
AM = M + 1
M = D
@SP
M = M - 1
A = M + 1
D = M
M = 0
A = A - 1
M = M - D
@SP
M = M - 1
A = M + 1
D = M
M = 0
@ARG
A = M + 1
M = D
@ARG
D = M
D = D + 1
A = D
D = M
@SP
AM = M + 1
M = D
@0
D = A
@SP
AM = M + 1
M = D
@SP
M = M - 1
A = M + 1
D = M
M = 0
A = A - 1
D = M - D
@GT.IF.0
D;JGT
@SP
A = M
M = 0
@GT.IF.1
0;JMP
(GT.IF.0)
@SP
A = M
M = -1
(GT.IF.1)
@SP
M = M - 1
A = M + 1
D = M
M = 0
@loop
!D;JEQ
@LCL
D = M
A = D
D = M
@SP
AM = M + 1
M = D
@0
D = A
@SP
AM = M + 1
M = D
@SP
M = M - 1
A = M + 1
D = M
M = 0
A = A - 1
D = M - D
@GT.IF.2
D;JGT
@SP
A = M
M = 0
@GT.IF.3
0;JMP
(GT.IF.2)
@SP
A = M
M = -1
(GT.IF.3)
@LCL
D = M
A = D
D = M
@SP
AM = M + 1
M = D
@LCL
D = M
@R14
M = D
@5
D = A
@R14
D = M - D
A = D
D = M
@R15
M = D
@SP
A = M
D = M
@ARG
A = M
M = D
@ARG
D = M
@SP
M = D
@R14
A = M - 1
D = M
@THAT
M = D
@2
D = A
@R14
A = M - D
D = M
@THIS
M = D
@3
D = A
@R14
A = M - D
D = M
@ARG
M = D
@4
D = A
@R14
A = M - D
D = M
@LCL
M = D
@R15
A = M
0;JMP
(FUNCTION.mult.END)
