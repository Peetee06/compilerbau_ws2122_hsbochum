class CodeGenerator:
    def __init__(self, ast):
        self.idx = 0
        self.ast = ast
        # the intermediate representation
        self.ir = None
        self.binary_operators = [
            "ADD",
            "SUB",
            "MUL",
            "DIV",
            "LT",
            "GT",
            "LTE",
            "GTE",
            "EQ",
            "NEQ",
            "and",
            "or",
        ]

    def generate_ir(self, tree=None):

        if not tree:
            # method invoked from root
            tree = self.ast

        ir = ""

        if not tree.children:
            # reached a leaf
            # code to push value to stack
            ir += f"LOAD {tree.token.type}:{tree.token.value}\n"
            return ir

        if tree.token.type == "KEYWORD":
            if tree.token.value == "if":
                # condition
                ir += self.generate_ir(tree.children[0])
                # when computing the result of condition is now on stack top
                # skip if expression if false
                ir += f"GOFALSE false{self.idx}\n"
                ir += self.generate_ir(tree.children[1])
                # skip else expression if true
                ir += f"GOTO true{self.idx}\n"
                ir += f"LABEL false{self.idx}\n"

                if len(tree.children) == 3:
                    # else case exists
                    ir += self.generate_ir(tree.children[2])
                ir += f"LABEL true{self.idx}\n"
                self.idx += 1

            elif tree.token.value == "while":
                # start of while
                ir += f"LABEL while_in{self.idx}\n"
                # condition
                ir += self.generate_ir(tree.children[0])
                # when computing the result of condition is now on stack top
                # leave while loop if expression if false
                ir += f"GOFALSE while_out{self.idx}\n"
                # expression in while loop
                ir += self.generate_ir(tree.children[1])
                # go to start of loop after finishing computation of
                # loop body
                ir += f"GOTO while_in{self.idx}\n"
                # label to get out of while loop
                ir += f"LABEL while_out{self.idx}\n"
                self.idx += 1

            elif (
                tree.token.value == "and"
                or tree.token.value == "or"
                or tree.token.value == "not"
            ):
                # boolean expression
                for child in tree.children[::-1]:
                    ir += self.generate_ir(child)
                ir += f"{tree.token.value}\n"

            elif tree.token.value == "def":
                # function definition
                # tree has children:
                # function identifier, parameter[s], function body

                # marker for AbstractStackMachine to
                # not evaluate function definition
                ir += "FUNCDEF\n"

                # jump in label: "LABEL func_in_IDENTIFIER"
                ir += f"LABEL func_in_{tree.children[0].token.value}\n"

                # iterate over parameters
                for child in tree.children[1:-1]:
                    ir += f"STORE {child.token.value}\n"

                # function body
                ir += self.generate_ir(tree.children[-1])
                # result is now on stack top

                # jump to label on jump stack top
                ir += "GOTOSTACK\n"

        elif tree.token.type == "ASSIGN":
            # evaluate expression to assign to identifier and push to stack
            ir += self.generate_ir(tree.children[1])
            # store result of expression as identifier
            ir += f"STORE {tree.children[0].token.value}\n"

        elif tree.token.type == "CALL":
            # push jump label to jump stack
            ir += f"MOVE func_return{self.idx}\n"

            # iterate over call parameters
            for child in tree.children[-1:0:-1]:
                # push child value to stack to retrieve in function
                ir += f"LOAD {child.token.type}:{child.token.value}\n"

            # jump to function in
            ir += f"GOTO func_in_{tree.children[0].token.value}\n"

            # LABEL to jump back after completing function evaluation
            ir += f"LABEL func_return{self.idx}\n"

            self.idx += 1

        elif tree.token.type in self.binary_operators:
            if tree.token.type == "SUB" and len(tree.children) == 1:
                ir += self.generate_ir(tree.children[0])
                ir += "LOAD INT:0\n"
            else:
                for child in tree.children[::-1]:
                    ir += self.generate_ir(child)

            # write operator
            ir += f"{tree.token}\n"

        else:
            for child in tree.children:
                ir += self.generate_ir(child)

            if tree.token.type == "SEMICOLON":
                # not an operation, just simple program flow
                pass

            else:
                ir += f"{tree.token}\n"

        # TODO: add return to functions
        # does it matter if expressions like "a + b;"
        # leave their result on stack top?

        if tree == self.ast:
            # method invoked from root
            # finished generating ir, write stop Token
            ir += "HALT\n"

        self.ir = ir
        return self.ir
