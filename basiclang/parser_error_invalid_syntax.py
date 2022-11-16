from error_ import Error


# ERROR during parsing-process
# for undefined syntax, during parsing process
class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)
