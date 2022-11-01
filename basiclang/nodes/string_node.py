# NODE-types for string
from basiclang.syntax_tree import SyntaxTree
from token_ import Token


class StringNode:
    def __init__(self, tok):
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    # give back token as, e.g. (STRING:XXX)
    def __repr__(self):
        return f'{self.tok}'  # return the string as token no parenthesis,
        # otherwise it is doubled at the BinopNode

    def conv_to_syntax_tree(self):
        return SyntaxTree(Token("STRING", self.tok.value))
