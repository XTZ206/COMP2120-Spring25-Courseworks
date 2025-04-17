    SUB     R4,R4,R4
    LD      P1,R1
    MOV     R1,R2
    LD      P2,R3
L:  MOV     R1,R10
    CALL    SQ
    ADD     R4,R11,R4
    ADD     R1,R2,R1
    SUB     R3,R1,R5
    BNZ     L
    ST      R4,P
    HLT
SQ: PUSH    R12
    PUSH    R13
    LD      P1,R13
    SUB     R11,R11,R11
    MOV     R10,R12
    AND     R12,R13,R13
    BNZ     L2
    SUB     R11,R12,R12
L2: MOV     R12,R11
    POP     R13
    POP     R12
    RET
P1: .WORD   1
P2: .WORD   A
P:  .WORD
