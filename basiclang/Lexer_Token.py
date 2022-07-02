import string
class Token:
    DIGITS = '0123456789'
    LETTERS = string.ascii_letters
    LETTERS_DIGITS = LETTERS + DIGITS

    TOKEN_TYPES = [
        "INT",
        "FLOAT",
        "STRING",
        "IDENTIFIER", # char from LETTERS
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
        "def"
    ]

    DICT_special_character = {
        ','  : 'COMMA',
        ';'  : 'SEMICOLON',
        '\n' : 'NEWLINE' }
    
    DICT_math_operators = {
        '+' : 'ADD',
        '-' : 'SUB',
        '*' : 'MUL',
        '/' : 'DIV',
        '(' : 'OPEN_PAR',
        ')' : 'CLOSE_PAR'}   

    DICT_comp_operators = {
        '=' : 'ASSIGN',
        '<' : 'LT',
        '>' : 'GT',
        '!' : 'NOT',
        '==': 'EQ',
        '!=': 'NEQ',
        '<=': 'LTE',
        '>=': 'GTE'} 


    def __init__(self, _type, _value=None, position_start = None, position_end = None):

        self.type = _type
        self.value = _value
        if position_start:
            self.position_start = position_start.copy()
            self.position_end = position_start.copy()
            self.position_end.step()
        if position_end:
            self.position_end = position_end.copy()

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

    def matches(self, _type, value):
        return self.type == _type and self.value == value