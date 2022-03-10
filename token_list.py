"""
Parentclass TokenList

Compilerbau

Constants for Vertextypes of a Syntaxtree
"""

class TokenList(object):
    NO_TYPE = 0
    NUM = 1
    DIGIT = 2
    INPUT_SIGN = 3
    EPSILON = 4
    START = 5
    NOT_FINAL = 6
    COMMA = 7
    IDENT = 8
    OPEN_PAR = 9
    CLOSE_PAR = 10
    ADD = 11
    SUB = 12
    MUL = 13
    DIV = 14
    EXPR = 15
    RIGHT_EXPR = 16
    TERM = 17
    RIGHT_TERM = 18
    OP = 20
    PROGRAM = 21
    FUNC = 22
    EQ = 23
    GT = 24
    GTE = 25
    LT = 26
    LTE = 27
    ASSIGN = 28
    FACTOR = 29
    STMT = 40
    WHITE_SPACE = 99
    BEGIN = 100
    END = 101
    IF = 102
    THEN = 103
    ELSE = 104
    ELSEIF = 105
    WHILE = 106
    DO = 107
    CONDITION = 108
    WRITE = 110

    # constant that indicates that there is no semantic function for that node
    UNDEFINED = 0x10000001
