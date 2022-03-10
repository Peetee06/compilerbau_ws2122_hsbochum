# TODO 
class Semantic(object):
    UNDEFINED = 0x10000001
    
    def f(t, v):
        """
        Parameters
        ----------
        t : SyntaxTree
            a Subtree of the Syntaxtree
        v : Any
        """
        return UNDEFINED


class Expression(Semantic):

    def f(tree, n):
        term = tree.get_child(0)
        right_expression = tree.get_child(1)
        return right_expression.value.f(right_expression, term.value.f(term, super().UNDEFINED))


class RightExpression(Semantic):
    # TODO def f


class Term(Semantic):
    def f(tree, n):
        term = tree.get_child(0)
        right_term = tree.get_child(1)
        
        return right_term.value.f(right_term, term.value.f(term, super().UNDEFINED))


class RightExpression(Semantic):
        # TODO 


class Num(Semantic):
    def _power(self, value):
        p = 10
        while(v/p != 0):
            p *= 10
        return p


    def f(self, tree, n):
        if tree.get_child_number() == 2:
            digit = tree.get_child(0)
            num = tree.get_child(1)

            v = num.value.f(num, super().UNDEFINED)
            return digit.value.f(digit, super().UNDEFINED)*_power(v)+v
        else:
            digit = tree.get_child(0)
            return digit.value.f(digit, super().UNDEFINED)


class Operator(Semantic):
    def f(self, tree, n):
        if t.get_child_number() == 3:
            expression = tree.get_child(1)
            return expression.value.f(expression, super().UNDEFINED)
        else:
            num = tree.get_child(0)
            return num.value.f(num, super().UNDEFINED)


class Digit(Semantic):
    def f(self, tree, n):
        symbol = tree.get_child(0)
        digits = ['0',
                  '1',
                  '2',
                  '3',
                  '4',
                  '5',
                  '6',
                  '7',
                  '8',
                  '9']

        if symbol in digits:
            return int(symbol)
        else:
            return super().UNDEFINED
            
