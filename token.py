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

