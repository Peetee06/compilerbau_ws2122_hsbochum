import string
import token_
from lexer_error_illegal_char import IllegalCharError
from lexer_error_illegal_operator import IllegalOperatorError
from token_ import Token
from lexer_position import Position

#######################################
# CONSTANTS

DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS

#######################################
# LEXER

class Lexer:
    def __init__(self, fn, text):  
        self.fn = fn
        self.text = text
        self.position = Position(-1, 0, -1, fn, text) 
        self.current_char = None 
        self.advance()  

    # advance to next character
    def advance(self):
        self.position.advance(self.current_char) 
        self.current_char = self.text[self.position.idx] if self.position.idx < len(
            self.text) else None 

    # create tokens from file
    def make_tokens(self):
        tokens = []  # Token Result

        while self.current_char is not None: 
            if self.current_char in ' \t': 
                self.advance()
            elif self.current_char in ';\n':
                tokens.append(Token(token_.Token.TOKEN_TYPES[21], pos_start=self.position))
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number()) 
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())
            elif self.current_char == '"':
                tokens.append(self.make_string())               
            elif self.current_char in Token.DICT_math_operators:
                tokens.append(self.make_math_op())   
            elif self.current_char in Token.DICT_comp_operators:
                token, error = self.make_compare_op()
                if error: return [], error
                tokens.append(token)

            elif self.current_char == ',':
                tokens.append(Token(token_.Token.TOKEN_TYPES[18], pos_start=self.position))
                self.advance()
            elif self.current_char == ':':
                tokens.append(Token(token_.Token.TOKEN_TYPES[22], pos_start=self.position))
                self.advance()
            else:
                pos_start = self.position.get() 
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.position, "'" + char + "'")

        tokens.append(Token(token_.Token.TOKEN_TYPES[22], pos_start=self.position))
        return tokens, None 

    # make math operators using math dictionary
    def make_math_op(self):
        make_math = ''
        position_start = self.position.get() 
        make_math = Token.DICT_math_operators[self.current_char]      
             
        self.advance()
        return Token(make_math, None, position_start, self.position)

    # make comparison operators using comparison dictionary
    def make_compare_op(self):
        make_comp_op = ''
        position_start = self.position.get()
        while self.current_char != None and self.current_char in Token.DICT_comp_operators:
            make_comp_op += self.current_char
            self.advance()
 
        if make_comp_op in Token.DICT_comp_operators:
            tok = Token.DICT_comp_operators[make_comp_op]
            return Token(tok, None, position_start, self.position), None
        
        return [], IllegalOperatorError(position_start, self.position, "'" + make_comp_op + "'")

    # make numbers + classifying float and int types
    def make_number(self):
        dot_exists = False
        make_number = ''
        position_start = self.position.get()
        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_exists == True: break
                dot_exists = True
                make_number += '.'
            else:
                make_number += self.current_char
            self.advance()

        result = Token(token_.Token.TOKEN_TYPES[1], float(make_number), position_start, self.position) if dot_exists else Token(token_.Token.TOKEN_TYPES[0], int(make_number), position_start, self.position) 
        return result

    # make string checking "" character
    def make_string(self):
        string_ = ""
        pos_start = self.position.get()
        escape_character = False
        self.advance()

        escape_characters = {
            'n': '\n',
            't': '\t'
        }
        while self.current_char != None and (self.current_char != '"' or escape_character):
            if escape_character:
                string_ += escape_characters.get(self.current_char, self.current_char)
            else:
                if self.current_char == '\\':
                    escape_character = True
                else:
                    string_ += self.current_char
            self.advance()
            escape_character = False

        self.advance()
        return Token(Token.TOKEN_TYPES[2], string_, pos_start, self.position)

    # make identifier or keyword depending on keywords existing in Token List
    def make_identifier(self):
        id_str = ''
        pos_start = self.position.get()

        while self.current_char != None and self.current_char in LETTERS_DIGITS + '_':
            id_str += self.current_char
            self.advance()

        # if TRUE it is KEYWORD, else IDENTIFIER
        tok_type = token_.Token.TOKEN_TYPES[4] if id_str in token_.Token.KEYWORDS else token_.Token.TOKEN_TYPES[3]
        return Token(tok_type, id_str, pos_start, self.position)
       