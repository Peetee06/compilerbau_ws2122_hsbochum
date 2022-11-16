from error_ import Error


# for undefined operator, if used, called in Lexer as last elseif path.
class IllegalOperatorError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Operator', details)
