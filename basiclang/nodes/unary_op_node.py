# for; factor
# 			   : (PLUS|MINUS) factor -> e.g. -5
# 			   : LPAREN expr RPAREN
from syntax_tree import SyntaxTree
from token_ import Token


class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

        self.pos_start = self.op_tok.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f'({self.op_tok}, {self.node})'

    def conv_to_syntax_tree(self):
        unary_op_tree = SyntaxTree(self.op_tok)
        unary_op_tree.insert_subtree(self.node.conv_to_syntax_tree())
        return unary_op_tree
