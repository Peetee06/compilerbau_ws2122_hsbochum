# NODE-type for the single numbers
from syntax_tree import SyntaxTree
from token_ import Token


class NumberNode:
    def __init__(self, tok):  # for a number as digit
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    # give back token as, e.g. (INT:2)
    def __repr__(self):
        return f'{self.tok}'  # return the digit as token no parenthesis,
        # otherwise it is doubled at the BinopNode

    def conv_to_syntax_tree(self):
        return SyntaxTree(self.tok)
