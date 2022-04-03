from lexer_error import (IllegalCharError, InvalidOperatorError)
from lexer_token import Token
from lexer_position import Position

# LEXICAL SCANNER
class Tokenizer:
    def __init__(self, filename, input):
        self.filename = filename
        self.input = input
        self.position = Position(-1,0,-1, filename, input)
        self.current_char = None
        self.read_next_char()   
    
    def read_next_char(self):    
        self.position.step(self.current_char) 
        self.current_char = self.input[self.position.index] if self.position.index < len(self.input) else None
       
    def create_tokens_from_input(self):
        token_result = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.read_next_char()
            elif self.current_char in Token.DICT_comp_operators:
                token, error = self.create_token_comp_operator()
                if error: return [], error
                token_result.append(token)
            elif self.current_char in Token.DICT_math_operators:
                token_result.append(self.create_token_math_operator())           
            elif self.current_char in Token.LETTERS:
                token_result.append(self.create_token_identifier())
            elif self.current_char in Token.DIGITS:
                token_result.append(self.create_token_number())  
            elif self.current_char in Token.DICT_special_character:
                token_result.append(self.create_token_special_character())
            else: 
                position_start = self.position.get_current_position()            
                char = self.current_char
                self.read_next_char()
                return [], IllegalCharError(position_start, self.position, "'" + char + "'")
       
        token_result.append(Token('EOF', position_start = self.position))
        return token_result, None

    def create_token_special_character(self):
        make_special_character = ''
        make_special_character = Token.DICT_special_character[self.current_char]          
        position_start = self.position.get_current_position()       
        self.read_next_char()
        return Token(make_special_character, None, position_start, self.position)

    def create_token_math_operator(self):
        make_math = ''
        make_math = Token.DICT_math_operators[self.current_char]      
        position_start = self.position.get_current_position()       
        self.read_next_char()
        return Token(make_math, position_start = position_start, position_end=self.position)

    def create_token_number(self):
        dot_exists = False
        make_number = ''
        position_start = self.position.get_current_position()
        while self.current_char != None and self.current_char in Token.DIGITS + '.':
            if self.current_char == '.':
                if dot_exists == True: break
                dot_exists = True
                make_number += '.'
            else:
                make_number += self.current_char
            self.read_next_char()

        result = Token('FLOAT', float(make_number), position_start, self.position) if dot_exists else Token('INT', int(make_number), position_start, self.position) 
        return result

    def create_token_comp_operator(self):
        make_operator = ''
        position_start = self.position.get_current_position()
        while self.current_char != None and self.current_char in Token.DICT_comp_operators:
            make_operator += self.current_char
            self.read_next_char()
 
        if make_operator in Token.DICT_comp_operators:
            tok = Token.DICT_comp_operators[make_operator]
            return Token(tok, None, position_start, self.position), None
        
        return [], InvalidOperatorError(position_start, self.position, "'" + make_operator + "'")       

    def create_token_identifier(self):
        make_string = ''
        position_start = self.position.get_current_position()
        while self.current_char != None and self.current_char in Token.LETTERS_DIGITS + '_':
            make_string += self.current_char
            self.read_next_char()

        tok_type = 'KEYWORD' if make_string in Token.KEYWORDS else 'IDENTIFIER'

        return Token(tok_type, make_string, position_start, self.position)

    # RUN
    def run(filename, input):
        tokenizer = Tokenizer(filename, input)
        tokens, error = tokenizer.create_tokens_from_input()

        return tokens, error