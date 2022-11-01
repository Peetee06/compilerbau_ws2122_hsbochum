from syntax_tree import SyntaxTree
from token_ import Token


class CallNode:
    def __init__(self, call_label_tok, argument_nodes=[]):
        self.call_label_tok = call_label_tok
        self.argument_nodes = argument_nodes

        self.pos_start = self.call_label_tok.pos_start

        if len(self.argument_nodes) > 0:
            self.pos_end = self.argument_nodes[len(self.argument_nodes) - 1].pos_end
        else:
            self.pos_end = self.call_label_tok.pos_end

    def __repr__(self):
        return f'Func_Call({self.call_label_tok}, {self.argument_nodes})'

    def conv_to_syntax_tree(self):
        call_tree = SyntaxTree(Token("CALL"))
        call_tree.insert_subtree(SyntaxTree(self.call_label_tok))
        for argument_node in self.argument_nodes:
            call_tree.insert_subtree(argument_node.conv_to_syntax_tree())
        return call_tree
