from token_ import Token


class SyntaxTree:
    def __init__(self, token):
        """
        Parameters
        ----------
        token : Token
        children : List of SyntaxTree

        """

        self._token = token  # Token("ADD")
        # children of the SyntaxTree
        # list of SyntaxTree
        # e.g. [SyntaxTree(Token("INT", 3)), mul_tree]
        self._children = []

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token):
        self._token = token

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, children):
        self._children = children

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __repr__(self, depth=0):
        offset = "| " * depth
        repr_ = f"{offset}{self.token}\n"
        for child in self.children:
            repr_ += child.__repr__(depth + 1)
        return repr_

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def insert_subtree(self, tree):
        self.children.append(tree)


def main():

    expr = "3 + 5 * 10 - 9"
    print(f"printing tree for expression: {expr}")
    mul = Token("MUL")
    sub = Token("SUB")
    add = Token("ADD")
    three = Token("INT", 3)
    five = Token("INT", 5)
    nine = Token("INT", 9)
    ten = Token("INT", 10)

    sub_t = SyntaxTree(sub)
    add_t = SyntaxTree(add)
    mul_t = SyntaxTree(mul)

    three_t = SyntaxTree(three)
    five_t = SyntaxTree(five)
    nine_t = SyntaxTree(nine)
    ten_t = SyntaxTree(ten)

    mul_t.insert_subtree(five_t)
    mul_t.insert_subtree(ten_t)

    add_t.insert_subtree(three_t)
    add_t.insert_subtree(mul_t)

    sub_t.insert_subtree(add_t)
    sub_t.insert_subtree(nine_t)

    print(sub_t)


if __name__ == "__main__":
    main()
