# this NODE allows +, -, * and / operation
# for; factor  : INT|FLOAT
from syntax_tree import SyntaxTree
from token_ import Token


class BinOpNode:
    # e.g. 1 + 2
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    # return the needed nodes and used operation as, e.g. (INT:1, ADD, INT:2)
    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'

    def conv_to_syntax_tree(self):
        ne = SyntaxTree(self.op_tok)
        ne.insert_subtree(self.left_node.conv_to_syntax_tree())
        ne.insert_subtree(self.right_node.conv_to_syntax_tree())
        return ne
