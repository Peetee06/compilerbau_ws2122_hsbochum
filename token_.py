"""
Parentclass Token

Compilerbau

Constants for Nodetypes of a Syntaxtree
"""

class Token(object):
    TOKEN_TYPES = ['INT',
                   'FLOAT',
                   'STRING',
                   'IDENTIFIER',
                   'KEYWORD',
                   'ADD',           # +
                   'SUB',           # -
                   'MUL',           # *
                   'DIV',           # /
                   'ASSIGN',        # =
                   'OPEN_PAR',      # (
                   'CLOSE_PAR',     # )
                   'EQ',            # equal
                   'NEQ',           # not equal
                   'GT',            # greater than
                   'GTE',           # greater than or equal
                   'LT',            # less than
                   'LTE',           # less than or equal
                   'COMMA',         # ,
                   'SEMICOLON',     # ;
                   'NEWLINE',
                   'EOF'
                  ]

    KEYWORDS = ['and',
                'or',
                'not',
                'if',
                'else',
                'while',
                'def',
                ]

    def __init__(self, type_, value=None):
        if type_ in self.TOKEN_TYPES:
            self.type = type_
        else:
            self.type = None
        self.value = value

    def __repr__(self):
        return f"{self.type}:{self.value}" if self.value else f"{self.type}"

    def matches(self, type_, value):
        return self.type == type_ and self.value == value
