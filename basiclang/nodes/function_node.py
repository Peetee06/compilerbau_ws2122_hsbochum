from syntax_tree import SyntaxTree
from token_ import Token


class FuncNode:
    def __init__(self, func_name_tok, parameter_toks, func_body):
        self.func_name_tok = func_name_tok
        self.parameter_toks = parameter_toks
        self.func_body = func_body

        if self.func_name_tok:
            self.pos_start = self.func_name_tok.pos_start
        elif len(self.parameter_toks) > 0:
            self.pos_start = self.parameter_toks[0].pos_start
        else:
            self.pos_start = self.func_body.pos_start

        self.pos_end = self.func_body.pos_end

    def __repr__(self):
        return f'Func({self.func_name_tok}, {self.parameter_toks}, {self.func_body})'

    def conv_to_syntax_tree(self):
        func_label = SyntaxTree(self.func_name_tok)
        func_tree = SyntaxTree(Token("KEYWORD", "def"))
        # identifier of function
        func_tree.insert_subtree(func_label)
        for parameter_tok in self.parameter_toks:
            func_tree.insert_subtree(SyntaxTree(parameter_tok))
        # body of function
        func_tree.insert_subtree(self.func_body.conv_to_syntax_tree())
        return func_tree
