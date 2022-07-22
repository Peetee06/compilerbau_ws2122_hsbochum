from basiclang.token_ import Token
from basiclang.syntax_tree import SyntaxTree
from basiclang.code_generator import CodeGenerator
from basiclang.abstract_stack_machine import AbstractStackMachine

# create ast with SyntaxTree class
# create ir with CodeGenerator class
# evaluate ir with AbstractStackMachine class


def test_PosNum():
    tree = SyntaxTree(Token("INT", 1))
    intermediate_representation = CodeGenerator(tree).generate_ir()
    result = AbstractStackMachine(intermediate_representation).evaluate()

    assert result == 1


def test_Digit():
    tree = SyntaxTree(Token("INT", 0))
    intermediate_representation = CodeGenerator(tree).generate_ir()
    result = AbstractStackMachine(intermediate_representation).evaluate()

    assert result == 0


def test_Num():
    tree = SyntaxTree(Token("FLOAT", 0.0))
    intermediate_representation = CodeGenerator(tree).generate_ir()
    result = AbstractStackMachine(intermediate_representation).evaluate()

    assert result == 0.0

    tree = SyntaxTree(Token("FLOAT", 0.10))
    intermediate_representation = CodeGenerator(tree).generate_ir()
    result = AbstractStackMachine(intermediate_representation).evaluate()

    assert result == 0.10

    tree = SyntaxTree(Token("FLOAT", 10.0))
    intermediate_representation = CodeGenerator(tree).generate_ir()
    result = AbstractStackMachine(intermediate_representation).evaluate()

    assert result == 10.0


def test_String():
    tree = SyntaxTree(Token("STRING", "TEST"))
    intermediate_representation = CodeGenerator(tree).generate_ir()
    result = AbstractStackMachine(intermediate_representation).evaluate()

    assert result == "TEST"

    tree = SyntaxTree(Token("STRING", ""))
    intermediate_representation = CodeGenerator(tree).generate_ir()
    result = AbstractStackMachine(intermediate_representation).evaluate()

    assert result == ""


def test_Term():
    mul = SyntaxTree(Token("MUL"))
    mul.insert_subtree(SyntaxTree(Token("INT", 3)))
    mul.insert_subtree(SyntaxTree(Token("INT", 5)))
    intermediate_representation = CodeGenerator(mul).generate_ir()
    result = AbstractStackMachine(intermediate_representation).evaluate()

    assert result == 3 * 5

    div = SyntaxTree(Token("DIV"))
    div.insert_subtree(SyntaxTree(Token("INT", 3)))
    div.insert_subtree(SyntaxTree(Token("INT", 5)))
    intermediate_representation = CodeGenerator(div).generate_ir()
    result = AbstractStackMachine(intermediate_representation).evaluate()

    assert result == 3 / 5

    add_ = SyntaxTree(Token("ADD"))
    add_.insert_subtree(SyntaxTree(Token("INT", 3)))
    add_.insert_subtree(SyntaxTree(Token("INT", 5)))
    intermediate_representation = CodeGenerator(add_).generate_ir()
    result = AbstractStackMachine(intermediate_representation).evaluate()

    assert result == 3 + 5

    sub_ = SyntaxTree(Token("SUB"))
    sub_.insert_subtree(SyntaxTree(Token("INT", 3)))
    sub_.insert_subtree(SyntaxTree(Token("INT", 5)))
    intermediate_representation = CodeGenerator(sub_).generate_ir()
    result = AbstractStackMachine(intermediate_representation).evaluate()

    assert result == 3 - 5


def test_Comparison():
    eq = SyntaxTree(Token("EQ"))
    eq.insert_subtree(SyntaxTree(Token("INT", 3)))
    eq.insert_subtree(SyntaxTree(Token("INT", 5)))
    intermediate_representation = CodeGenerator(eq).generate_ir()
    result = AbstractStackMachine(intermediate_representation).evaluate()

    assert result == (3 == 5)

    lte = SyntaxTree(Token("LTE"))
    lte.insert_subtree(SyntaxTree(Token("INT", 3)))
    lte.insert_subtree(SyntaxTree(Token("INT", 5)))
    intermediate_representation = CodeGenerator(lte).generate_ir()
    result = AbstractStackMachine(intermediate_representation).evaluate()

    assert result == (3 <= 5)

    gte = SyntaxTree(Token("GTE"))
    gte.insert_subtree(SyntaxTree(Token("INT", 3)))
    gte.insert_subtree(SyntaxTree(Token("INT", 5)))
    intermediate_representation = CodeGenerator(gte).generate_ir()
    result = AbstractStackMachine(intermediate_representation).evaluate()

    assert result == (3 >= 5)

    lt = SyntaxTree(Token("LT"))
    lt.insert_subtree(SyntaxTree(Token("INT", 3)))
    lt.insert_subtree(SyntaxTree(Token("INT", 5)))
    intermediate_representation = CodeGenerator(lt).generate_ir()
    result = AbstractStackMachine(intermediate_representation).evaluate()

    assert result == (3 < 5)

    gt = SyntaxTree(Token("GT"))
    gt.insert_subtree(SyntaxTree(Token("INT", 3)))
    gt.insert_subtree(SyntaxTree(Token("INT", 5)))
    intermediate_representation = CodeGenerator(gt).generate_ir()
    result = AbstractStackMachine(intermediate_representation).evaluate()

    assert result == (3 > 5)

    ne = SyntaxTree(Token("NEQ"))
    ne.insert_subtree(SyntaxTree(Token("INT", 3)))
    ne.insert_subtree(SyntaxTree(Token("INT", 5)))
    intermediate_representation = CodeGenerator(ne).generate_ir()
    result = AbstractStackMachine(intermediate_representation).evaluate()

    assert result == (3 != 5)


def test_Boolexpr():
    # False and True
    and_ = SyntaxTree(Token("KEYWORD", "and"))
    and_.insert_subtree(SyntaxTree(Token("INT", 0)))
    and_.insert_subtree(SyntaxTree(Token("INT", 1)))
    intermediate_representation = CodeGenerator(and_).generate_ir()
    result = AbstractStackMachine(intermediate_representation).evaluate()

    assert result == (False and True)

    # False or True
    or_ = SyntaxTree(Token("KEYWORD", "or"))
    or_.insert_subtree(SyntaxTree(Token("INT", 0)))
    or_.insert_subtree(SyntaxTree(Token("INT", 1)))
    intermediate_representation = CodeGenerator(or_).generate_ir()
    result = AbstractStackMachine(intermediate_representation).evaluate()

    assert result == (False or True)

    # not False
    not_false = SyntaxTree(Token("KEYWORD", "not"))
    not_false.insert_subtree(SyntaxTree(Token("INT", 0)))
    intermediate_representation = CodeGenerator(not_false).generate_ir()
    result = AbstractStackMachine(intermediate_representation).evaluate()

    assert result == (not False)

    # not True
    not_true = SyntaxTree(Token("KEYWORD", "not"))
    not_true.insert_subtree(SyntaxTree(Token("INT", 1)))
    intermediate_representation = CodeGenerator(not_true).generate_ir()
    result = AbstractStackMachine(intermediate_representation).evaluate()

    assert result == (not True)

    # (not (3 != 5))
    not_compared = SyntaxTree(Token("KEYWORD", "not"))
    ne = SyntaxTree(Token("NEQ"))
    ne.insert_subtree(SyntaxTree(Token("INT", 3)))
    ne.insert_subtree(SyntaxTree(Token("INT", 5)))
    not_compared.insert_subtree(ne)
    intermediate_representation = CodeGenerator(not_compared).generate_ir()
    result = AbstractStackMachine(intermediate_representation).evaluate()

    assert result == (not (3 != 5))


def test_Expression():
    string_tree = SyntaxTree(Token("STRING", "Testing"))
    semicolon = SyntaxTree(Token("SEMICOLON"))
    semicolon.insert_subtree(string_tree)
    intermediate_representation = CodeGenerator(semicolon).generate_ir()
    result = AbstractStackMachine(intermediate_representation).evaluate()
    expected = "Testing"
    assert result == expected


def test_Ifelse_If():
    # False or True => True
    or_ = SyntaxTree(Token("KEYWORD", "or"))
    or_.insert_subtree(SyntaxTree(Token("INT", 0)))
    or_.insert_subtree(SyntaxTree(Token("INT", 1)))
    sub_ = SyntaxTree(Token("SUB"))
    sub_.insert_subtree(SyntaxTree(Token("INT", 3)))
    sub_.insert_subtree(SyntaxTree(Token("INT", 5)))

    if_tree = SyntaxTree(Token("KEYWORD", "if"))
    if_tree.insert_subtree(or_)
    if_tree.insert_subtree(sub_)

    intermediate_representation = CodeGenerator(if_tree).generate_ir()
    result = AbstractStackMachine(intermediate_representation).evaluate()

    expected = -2

    assert result == expected


def test_Ifelse_Else():
    # False and True => True
    and_ = SyntaxTree(Token("KEYWORD", "and"))
    and_.insert_subtree(SyntaxTree(Token("INT", 0)))
    and_.insert_subtree(SyntaxTree(Token("INT", 1)))
    sub_ = SyntaxTree(Token("SUB"))
    sub_.insert_subtree(SyntaxTree(Token("INT", 3)))
    sub_.insert_subtree(SyntaxTree(Token("INT", 5)))

    if_tree = SyntaxTree(Token("KEYWORD", "if"))
    if_tree.insert_subtree(and_)
    if_tree.insert_subtree(sub_)

    intermediate_representation = CodeGenerator(if_tree).generate_ir()
    result = AbstractStackMachine(intermediate_representation).evaluate()

    expected = None

    assert result == expected


def test_Ifelse_If_Else():
    # False and True => True
    and_ = SyntaxTree(Token("KEYWORD", "and"))
    and_.insert_subtree(SyntaxTree(Token("INT", 0)))
    and_.insert_subtree(SyntaxTree(Token("INT", 1)))
    sub_ = SyntaxTree(Token("SUB"))
    sub_.insert_subtree(SyntaxTree(Token("INT", 3)))
    sub_.insert_subtree(SyntaxTree(Token("INT", 5)))
    add_ = SyntaxTree(Token("ADD"))
    add_.insert_subtree(SyntaxTree(Token("INT", 3)))
    add_.insert_subtree(SyntaxTree(Token("INT", 5)))

    if_tree = SyntaxTree(Token("KEYWORD", "if"))
    if_tree.insert_subtree(and_)
    if_tree.insert_subtree(sub_)
    if_tree.insert_subtree(add_)

    intermediate_representation = CodeGenerator(if_tree).generate_ir()
    result = AbstractStackMachine(intermediate_representation).evaluate()

    expected = 8

    assert result == expected


def test_While():
    # i = 0
    identifier = SyntaxTree(Token("IDENTIFIER", "i"))
    value = SyntaxTree(Token("INT", 0))
    assign = SyntaxTree(Token("ASSIGN"))
    assign.insert_subtree(identifier)
    assign.insert_subtree(value)

    # i <= 3
    lte = SyntaxTree(Token("LTE"))
    limit = SyntaxTree(Token("INT", 3))
    lte.insert_subtree(identifier)
    lte.insert_subtree(limit)

    # result = 0
    result_id = SyntaxTree(Token("IDENTIFIER", "result"))
    zero = SyntaxTree(Token("INT", 0))
    result_assign1 = SyntaxTree(Token("ASSIGN"))
    result_assign1.insert_subtree(result_id)
    result_assign1.insert_subtree(zero)

    # result = result + 2
    two = SyntaxTree(Token("INT", 2))
    add1 = SyntaxTree(Token("ADD"))
    add1.insert_subtree(result_id)
    add1.insert_subtree(two)
    result_assign2 = SyntaxTree(Token("ASSIGN"))
    result_assign2.insert_subtree(result_id)
    result_assign2.insert_subtree(add1)

    # i = i + 1
    one = SyntaxTree(Token("INT", 1))
    add2 = SyntaxTree(Token("ADD"))
    add2.insert_subtree(identifier)
    add2.insert_subtree(one)
    increment = SyntaxTree(Token("ASSIGN"))
    increment.insert_subtree(identifier)
    increment.insert_subtree(add2)

    initializations = SyntaxTree(Token("SEMICOLON"))
    initializations.insert_subtree(result_assign1)
    initializations.insert_subtree(assign)

    loop_body = SyntaxTree(Token("SEMICOLON"))
    loop_body.insert_subtree(result_assign2)
    loop_body.insert_subtree(increment)

    while_ = SyntaxTree(Token("KEYWORD", "while"))
    while_.insert_subtree(lte)
    while_.insert_subtree(loop_body)

    program = SyntaxTree(Token("SEMICOLON"))
    program.insert_subtree(initializations)
    program.insert_subtree(while_)
    program.insert_subtree(result_id)

    intermediate_representation = CodeGenerator(program).generate_ir()
    print(intermediate_representation)

    result = AbstractStackMachine(intermediate_representation).evaluate()

    expected = 8

    assert result == expected


def test_Function():
    # def test(a, b) { a + b }
    a = SyntaxTree(Token("IDENTIFIER", "a"))
    b = SyntaxTree(Token("IDENTIFIER", "b"))
    test_label = SyntaxTree(Token("IDENTIFIER", "test"))
    test_tree = SyntaxTree(Token("KEYWORD", "def"))
    add_ = SyntaxTree(Token("ADD"))
    add_.insert_subtree(a)
    add_.insert_subtree(b)

    # identifier of function
    test_tree.insert_subtree(test_label)
    # parameter a
    test_tree.insert_subtree(a)
    # parameter b
    test_tree.insert_subtree(b)
    # body of function:  a + b
    test_tree.insert_subtree(add_)

    call_tree = SyntaxTree(Token("CALL"))
    call_tree.insert_subtree(test_label)
    call_tree.insert_subtree(SyntaxTree(Token("INT", 5)))
    call_tree.insert_subtree(SyntaxTree(Token("INT", 3)))

    program = SyntaxTree(Token("SEMICOLON"))
    program.insert_subtree(test_tree)
    program.insert_subtree(call_tree)

    intermediate_representation = CodeGenerator(program).generate_ir()

    print(intermediate_representation)

    result = AbstractStackMachine(intermediate_representation).evaluate()

    expected = 8

    assert result == expected


def test_Instruction():
    # TODO:
    pass


def test_Program():
    # TODO:
    pass
