"""
Parentclass Token

Compilerbau

Constants for Nodetypes of a Syntaxtree
"""


class Token(object):
    TOKEN_TYPES = [
        "INT",
        "FLOAT",
        "STRING",
        "IDENTIFIER",
        "KEYWORD",
        "ADD",  # +
        "SUB",  # -
        "MUL",  # *
        "DIV",  # /
        "ASSIGN",  # =
        "OPEN_PAR",  # (
        "CLOSE_PAR",  # )
        "EQ",  # equal
        "NEQ",  # not equal
        "GT",  # greater than
        "GTE",  # greater than or equal
        "LT",  # less than
        "LTE",  # less than or equal
        "COMMA",  # ,
        "SEMICOLON",  # ;
        "CALL",  # call a function
        "NEWLINE",
        "EOF",
    ]

    KEYWORDS = [
        "and",
        "or",
        "not",
        "if",
        "else",
        "while",
        "def",
    ]

    def __init__(self, type_, value=None):
        if type_ in self.TOKEN_TYPES:
            self.type = type_
        else:
            self.type = None
        self.value = value

    def __repr__(self):
        type_string = f"{self.type}"
        type_value_string = f"{self.type}:{self.value}"
        return type_string if self.value is None else type_value_string

    def matches(self, type_, value):
        return self.type == type_ and self.value == value
