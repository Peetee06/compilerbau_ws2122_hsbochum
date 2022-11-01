# NEW 12.09.2022
# used for multiple statements
# can be used later for lists
from basiclang.syntax_tree import SyntaxTree
from token_ import Token


class ListNode:
    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes

        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f'Statement_List({self.element_nodes})'

    def conv_to_syntax_tree(self):
        if len(self.element_nodes) == 1:
            return self.element_nodes[0].conv_to_syntax_tree()
        result = SyntaxTree(Token("SEMICOLON"))
        for node in self.element_nodes:
            result.insert_subtree(node.conv_to_syntax_tree())
        return result
