class CodeGenerator:

    def __init__(self, ast):
        self.ast = ast
        # the intermediate representation
        self.ir = None
        # index for incrementing labels
        self.idx = 0

    def generate_ir(self, tree=None, idx=0):
        if not tree:
            # method invoked from root
            tree = self.ast
        
        ir = ""
        
        if not tree.children:
            # reached a leaf
            # code to push value to stack
            ir = f"LOAD {tree.token.type}:{tree.token.value}\n"
            return ir
        
        if tree.token.type == "KEYWORD":
            if tree.token.value == "if":
                idx = self.idx
                # condition
                ir += self.generate_ir(tree.children[0])
                # when computing the result of condition is now on stack top
                # skip if expression if false
                ir += f"GOFALSE false{idx}\n"
                ir += self.generate_ir(tree.children[1])
                # skip else expression if true
                ir += f"GOTO true{idx}\n"
                ir += f"LABEL false{idx}\n"

                if len(tree.children) == 3:
                    # else case exists
                    ir += self.generate_ir(tree.children[2])
                ir += f"LABEL true{idx}\n"

            elif tree.token.value == "while":
                idx = self.idx
                # start of while
                ir += f"LABEL while_in{idx}\n"
                # condition
                ir += self.generate_ir(tree.children[0])
                # when computing the result of condition is now on stack top
                # leave while loop if expression if false
                ir += f"GOFALSE while_out{idx}\n"
                # expression in while loop
                ir += self.generate_ir(tree.children[1])
                # go to start of loop after finishing computation of
                # loop body
                ir += f"GOTO while_in{idx}\n"
                # label to get out of while loop
                ir += f"LABEL while_out{idx}\n"

        elif tree.token.type == "ASSIGN":
            # evaluate expression to assign to identifier
            ir += self.generate_ir(tree.children[1])
            # store result of expression as identifier
            ir += f"STORE {tree.children[0].token.value}\n"
        
        else:
            for child in tree.children:
                ir += self.generate_ir(child)
            
            if tree.token.type == "SEMICOLON":
                # not an operation, just simple program flow
                pass
            else:
                ir += f"{tree.token}\n"

        self.ir = ir
        return self.ir
