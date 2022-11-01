import string

import token_
from expected_char_error_ import ExpectedCharError
from illegal_char_error import IllegalCharError
from token_ import Token

#######################################
# CONSTANTS
#######################################

DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS


#######################################
# POSITION
#######################################

# track the line-number, column-number und current index
class Position:
    def __init__(self, idx, ln, col, fn,
                 ftxt):  # fn and ftext for file-name and file-content, to tell the user where the error is
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None):  # move to next index and at new col. and index, if necessary
        self.idx += 1
        self.col += 1

        if current_char == '\n':  # if new line, increment line and reset column.
            self.ln += 1
            self.col = 0

        return self

    def copy(self):  # create copy of the position
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)


#######################################
# LEXER
#######################################

class Lexer:
    def __init__(self, fn, text):  # take the "text" which need to be processed and a file-name fn
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)  # track  the current position, file-name and the text
        self.current_char = None  # track the current character
        self.advance()  # starting the advance methode

    # advance to the next char in the text
    def advance(self):
        self.pos.advance(self.current_char)  # pass the current char
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(
            self.text) else None  # set the new position inside the text

    # creating tokens out of the "text"
    def make_tokens(self):
        tokens = []  # will be the result

        while self.current_char is not None:  # going through all the char. in the text
            if self.current_char in ' \t':  # ignoring spaces and taps
                self.advance()
            # maybe later change [19] to [22]
            elif self.current_char in ';\n':
                tokens.append(Token(token_.Token.TOKEN_TYPES[20], pos_start=self.pos))
                self.advance()
            elif self.current_char in DIGITS:  # check if its a number
                tokens.append(self.make_number())  # make_number(), for numbers with more than one digit
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())
            elif self.current_char == '"':
                tokens.append(self.make_string())
            elif self.current_char == '+':
                tokens.append(Token(token_.Token.TOKEN_TYPES[5], pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(token_.Token.TOKEN_TYPES[6], pos_start=self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(token_.Token.TOKEN_TYPES[7], pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(token_.Token.TOKEN_TYPES[8], pos_start=self.pos))
                self.advance()
            #   elif self.current_char == '=':
            #       tokens.append(Token(token_.Token.TOKEN_TYPES[12], pos_start=self.pos))
            #       self.advance()
            elif self.current_char == '(':
                tokens.append(Token(token_.Token.TOKEN_TYPES[10], pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(token_.Token.TOKEN_TYPES[11], pos_start=self.pos))
                self.advance()
            elif self.current_char == '!':
                tok, error = self.make_not_equals()
                if error: return [], error
                tokens.append(tok)
            elif self.current_char == '=':
                tokens.append(self.make_equals())
            elif self.current_char == '<':
                tokens.append(self.make_less_than())
            elif self.current_char == '>':
                tokens.append(self.make_greater_than())
            elif self.current_char == ',':
                tokens.append(Token(token_.Token.TOKEN_TYPES[18], pos_start=self.pos))
                self.advance()
            elif self.current_char == ':':
                tokens.append(Token(token_.Token.TOKEN_TYPES[22], pos_start=self.pos))
                self.advance()
            else:
                # store the pos. and the char, than return an empty list with the Error
                pos_start = self.pos.copy()  # copy the position where the error accrued
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        tokens.append(Token(token_.Token.TOKEN_TYPES[21], pos_start=self.pos))  # the token EOF shows the end of file.
        return tokens, None  # return of the func. normally the tokens_List and None for the Error

    # for numbers with more than one digit, used inside Lexer
    def make_number(self):
        num_str = ''  # track the numbers
        dot_count = 0  # check if there is dot
        pos_start = self.pos.copy()  # for the position start and end

        # loop start, if it is a digit or dot , for float numbers
        while self.current_char is not None and self.current_char in DIGITS + '.':
            if self.current_char == '.':  # check if there is a dot
                if dot_count == 1: break  # if we already have a dot, break out
                dot_count += 1  # if not, count equal 1
                num_str += '.'  # append a dot to the number
            else:
                num_str += self.current_char
            self.advance()  # go to the next char

        # checking for int-numbers and conversion of the number
        if dot_count == 0:
            return Token(token_.Token.TOKEN_TYPES[0], int(num_str), pos_start, self.pos)  # INT_TOKEN
        else:
            return Token(token_.Token.TOKEN_TYPES[1], float(num_str), pos_start, self.pos)  # FLOAT_TOKEN

    def make_string(self):
        string_ = ""
        pos_start = self.pos.copy()
        escape_character = False
        self.advance()

        escape_characters = {
            'n': '\n',
            't': '\t'
        }
        while self.current_char != None and (self.current_char != '"' or escape_character):
            # check for escaping the char
            if escape_character:
                # set from the dict, if not inside dict use current_char
                string_ += escape_characters.get(self.current_char, self.current_char)
            else:
                # check for '\'
                if self.current_char == '\\':
                    escape_character = True
                else:
                    string_ += self.current_char
            self.advance()
            escape_character = False

        self.advance()
        return Token(Token.TOKEN_TYPES[2], string_, pos_start, self.pos)

    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in LETTERS_DIGITS + '_':
            id_str += self.current_char
            self.advance()

        # if TRUE it is KEYWORD, else IDENTIFIER
        tok_type = token_.Token.TOKEN_TYPES[4] if id_str in token_.Token.KEYWORDS else token_.Token.TOKEN_TYPES[3]
        return Token(tok_type, id_str, pos_start, self.pos)
        # return Token(token_.Token.TOKEN_TYPES[0], int(num_str), pos_start, self.pos)  # INT_TOKEN

    def make_not_equals(self):
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            return Token(Token.TOKEN_TYPES[13], pos_start=pos_start, pos_end=self.pos), None

        self.advance()
        return None, ExpectedCharError(pos_start, self.pos, "'=' (after '!')")

    # check for '='
    def make_equals(self):
        tok_type = Token.TOKEN_TYPES[12]  # token EQ
        pos_start = self.pos.copy()
        self.advance()

        # check for '=='
        if self.current_char == '=':
            self.advance()
            ## for '=='
            tok_type = Token.TOKEN_TYPES[12]  # token EQ

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    # check for '<'
    def make_less_than(self):
        tok_type = Token.TOKEN_TYPES[16]  # Token LT
        pos_start = self.pos.copy()
        self.advance()

        # check for '<='
        if self.current_char == '=':
            self.advance()
            tok_type = Token.TOKEN_TYPES[17]  # token LTE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    # check for '>'
    def make_greater_than(self):
        tok_type = Token.TOKEN_TYPES[14]  # token GT
        pos_start = self.pos.copy()
        self.advance()

        # check for '>='
        if self.current_char == '=':
            self.advance()
            tok_type = Token.TOKEN_TYPES[15]  # token GTE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)
