from Lexer_Error import (Error, IllegalCharError)
from Lexer_Token import Token
from Lexer_Position import Position
import string


# DIGITS + TOKEN DICTIONARY
DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS

tokenDict = {
        '+' : 'ADD',
        '-' : 'SUB',
        '*' : 'MUL',
        '/' : 'DIV',
        '=' : 'ASSIGN',
        '(' : 'OPEN_PAR',
        ')' : 'CLOSE_PAR',
        ',' : 'COMMA',
        '<' : 'LT',
        '>' : 'GT'}      


# LEXICAL SCANNER
class Tokenizer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.step_to_nect_char()   
    
    def step_to_nect_char(self):  
     
        self.pos.advance(self.current_char)            
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def create_tokens_from_text(self):
        lexer_result = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.step_to_nect_char()
            elif self.current_char in DIGITS:
                lexer_result.append(self.get_numbertype())
            elif self.current_char in tokenDict:               
                tok = tokenDict[self.current_char]
                lexer_result.append(tok)             
                self.step_to_nect_char()
            else:               
                pos_start = self.pos.copy()
                char = self.current_char
                self.step_to_nect_char()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")
       
        return lexer_result, None

    def get_numbertype(self):
        composite_number = ''
        dot_exists = False

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_exists == True: break
                dot_exists = True
                composite_number += '.'
            else:
                composite_number += self.current_char
            self.step_to_nect_char()

        if dot_exists == False:
            return Token('INT', int(composite_number))
        else:
            return Token('FLOAT', float(composite_number))


    # RUN
    def run(filename, text):
        tokenizer = Tokenizer(filename, text)
        tokens, error = tokenizer.create_tokens_from_text()

        return tokens, error