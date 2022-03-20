from LexerError import (Error, IllegalCharError)
from LexerToken import Token
from LexerPosition import Position

# DIGITS + TOKEN DICTIONARY
DIGITS = '0123456789'
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
        self.currentChar = None
        self.LastChar = None
        self.stepToNextChar()   
    
    def stepToNextChar(self):  
        self.LastChar = self.currentChar      
        self.pos.advance(self.currentChar)            
        self.currentChar = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def createTokensFromText(self):
        lexerResult = []

        while self.currentChar != None:
            if self.currentChar in ' \t':
                self.stepToNextChar()
            elif self.currentChar in DIGITS:
                lexerResult.append(self.detectIntOrFloatFromNumber())
            elif self.currentChar in tokenDict:               
                tok = tokenDict[self.currentChar]
                lexerResult.append(tok)             
                self.stepToNextChar()
            else:               
                pos_start = self.pos.copy()
                char = self.currentChar
                self.stepToNextChar()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")
       
        return lexerResult, None

    def detectIntOrFloatFromNumber(self):
        compositeNumber = ''
        dotExists = False

        while self.currentChar != None and self.currentChar in DIGITS + '.':
            if self.currentChar == '.':
                if dotExists == True: break
                dotExists = True
                compositeNumber += '.'
            else:
                compositeNumber += self.currentChar
            self.stepToNextChar()

        if dotExists == False:
            return Token('INT', int(compositeNumber))
        else:
            return Token('FLOAT', float(compositeNumber))


    # RUN
    def run(filename, text):
        tokenizer = Tokenizer(filename, text)
        tokens, error = tokenizer.createTokensFromText()

        return tokens, error