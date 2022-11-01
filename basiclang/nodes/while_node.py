# Node for the while-expr
from basiclang.syntax_tree import SyntaxTree
from token_ import Token


class WhileNode:
    def __init__(self, condition_node, body_node):
        self.condition_node = condition_node
        self.body_node = body_node

        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end

    def __repr__(self):
        return f'while({self.condition_node}, {self.body_node})'

    def conv_to_syntax_tree(self):
        while_ = SyntaxTree(Token("KEYWORD", "while"))
        while_.insert_subtree(self.condition_node.conv_to_syntax_tree())
        while_.insert_subtree(self.body_node.conv_to_syntax_tree())
        return while_
