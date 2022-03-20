class CodeGenerator:

    def __init__(self, ast):
        self.ast = ast
        # the three adress code
        self.tac = None

    def generate_tac(self, tree=None):
        if not tree:
            tree = self.ast
        
        tac = ""
        
        if not tree.children:
            # reached a leaf
            # code to push value to stack
            tac = f"LOAD {tree.token.value}\n"
            return tac

        for child in tree.children:
            tac += self.generate_tac(child)

        tac += f"{tree.token}\n"

        self.tac = tac
        return self.tac
