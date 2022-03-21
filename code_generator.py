class CodeGenerator:

    def __init__(self, ast):
        self.ast = ast
        # the intermediate representation
        self.ir = None

    def generate_ir(self, tree=None):
        if not tree:
            tree = self.ast
        
        ir = ""
        
        if not tree.children:
            # reached a leaf
            # code to push value to stack
            ir = f"LOAD {tree.token.value}\n"
            return ir

        for child in tree.children:
            ir += self.generate_ir (child)

        ir += f"{tree.token}\n"

        self.ir = ir
        return self.ir
