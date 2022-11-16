from error_ import Error


# for undefined char, if used, called in Lexer as last elseif path.
class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)
