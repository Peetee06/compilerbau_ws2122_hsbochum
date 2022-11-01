# allows variables
# for; expr    : KEYWORD: VAR  IDENTIFIER EQ expr
from syntax_tree import SyntaxTree
from token_ import Token


class VarNode:
    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end

        # return the identifier and the value as, e.g (IDENTIFIER: a, VALUE: 5)
    def __repr__(self):
        return f'({self.var_name_tok}, {self.value_node})'

    def conv_to_syntax_tree(self):
        identifier = SyntaxTree(self.var_name_tok)
        value = self.value_node.conv_to_syntax_tree()
        assign = SyntaxTree(Token("ASSIGN"))
        assign.insert_subtree(identifier)
        assign.insert_subtree(value)
        return assign
