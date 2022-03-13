from token_list import TokenList

from semantic import Semantic, 
                     Expression,
                     RightExpression,
                     Term,
                     RightTerm,
                     Num,
                     Operator,
                     Digit

class SyntaxTree(TokenList):
    token = -1


    def __init__(self, token):
        # TODO
        """
        Parameters
        ----------
        tree : SyntaxTree
        

        """
        self._child_nodes = []
        self._character = 0
        self.lexem = ""
        self._token = token
        self.set_semantic_function(token)


    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token):
        self._token = token


    @property
    def character(self):
        return self._character

    @character.setter
    def character(self, char):
        self._character = char


    @lexem.setter
    def lexem(self, lexem):
        self.lexem = lexem


    @property
    def child_nodes(self):
        return self._child_nodes

    def get_child_number(self):
        return len(self.child_nodes)

    def get_child(self, i):
        child = self.child_nodes[i] if i < len(child_nodes) else None
        return child


    def print_syntax_tree(self, depth):
        for i in range(depth):
            print("  ", end="")
        print(self.get_token_string(), end="")
        if self.character != 0:
            print(":", self.character)
        else:
            print("")
        for child in self.child_nodes:
            child.print_syntax_tree(depth+1)


    def get_token_string(self):
        token_dict = TokenList.__dict__
        for key in token_dict:
            if self.token == token_dict[key]:
                # token matched
                return key
        
        # no token or token not in TokenList
        return token_dict["UNDEFINED"]


    def set_semantic_function(self, token_string):
        # TODO insert classes
        mapping = {
                "EXPR": Expression(),
                "RIGHT_EXPR": RightExpression(),
                "TERM": Term(),
                "RIGHT_TERM": RightTerm(),
                "NUM": Num(),
                "OP": Operator(),
                "DIGIT": Digit()
                }

        # matches token_string in the mapping dict
        # if token_string is not in mapping, returns
        # Semantic object instance which has "UNDEFINED"
        # semantic meaning
        self.value = mapping.get(token_string, Semantic())


    def insert_subtree(token):
        node = SyntaxTree(token)
        self.child_nodes.append(node)
        return node




def main():
    t = SyntaxTree()
    print(t.get_token_string())

if __name__ == '__main__':
    main()
