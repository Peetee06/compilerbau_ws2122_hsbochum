# Node for the if-expr
from basiclang.syntax_tree import SyntaxTree
from token_ import Token


class IfNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        # start with the first cases,
        self.pos_start = self.cases[0].pos_start
        # the end is the else or the last element of the list
        self.pos_end = (self.else_case or self.cases[1]).pos_end

    def __repr__(self):
        return f'if({self.cases}, {self.else_case})'

    def conv_to_syntax_tree(self):
        if_tree = SyntaxTree(Token("KEYWORD", "if"))
        # condition
        if_tree.insert_subtree(self.cases[0].conv_to_syntax_tree())
        # expr
        if_tree.insert_subtree(self.cases[1].conv_to_syntax_tree())
        if_tree.insert_subtree(self.else_case.conv_to_syntax_tree())
        return if_tree
