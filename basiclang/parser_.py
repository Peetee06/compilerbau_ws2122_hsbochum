import token_
from nodes.bin_op_node import BinOpNode
from nodes.if_node import IfNode
from invalid_syntax_error import InvalidSyntaxError
from nodes.list_node import ListNode
from parse_result import ParseResult
from nodes.unary_op_node import UnaryOpNode
from nodes.var_access_node import VarAccessNode
from nodes.while_node import WhileNode
from nodes.function_node import FuncNode
from lexer_ import Lexer
from nodes.number_node import NumberNode
from nodes.string_node import StringNode
from nodes.var_node import VarNode
from nodes.call_node import CallNode

from token_ import Token
import string

#######################################
# CONSTANTS
#######################################

DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS


#######################################
# PARSER
#######################################

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens  # takes the token-list
        self.tok_idx = -1  # current index
        self.advance()

    def advance(self, ):
        self.tok_idx += 1
        self.update_current_tok()
        # if self.tok_idx < len(self.tokens):  # if it is in the range of the tokens
        #    self.current_tok = self.tokens[self.tok_idx]  # take the current token
        return self.current_tok

    def reverse(self, amount=1):
        self.tok_idx -= amount
        self.update_current_tok()
        return self.current_tok

    # cause of reuse, move the if expr of the advance-method in it owns methode
    def update_current_tok(self):
        if self.tok_idx >= 0 and self.tok_idx < len(self.tokens):  # if it is in the range of the tokens
            self.current_tok = self.tokens[self.tok_idx]  # take the current token

    ###############################

    def parse(self):
        res = self.statement()  # 12.09.2022 grammar changed, before here was  self.expr()
        if not res.error and self.current_tok.type != token_.Token.TOKEN_TYPES[
            21]:  # catching an syntax error,EOF_TOKEN
            return res.failure(InvalidSyntaxError(  # return the syntax error
                self.current_tok.pos_start, self.current_tok.pos_end,
                "FEHLER_1: Expected '+', '-', '*' or '/'"
            ))
        return res

    ###################################
    ###
    # define grammar rules as code
    ###

    # allows multiline statements
    def statement(self):
        res = ParseResult()

        mul_line_statements = []
        pos_start = self.current_tok.pos_start.copy()

        # skip if the first line is a empty line
        while self.current_tok.type == Token.TOKEN_TYPES[20]:  # NEWLINE_TOKEN
            res.register_advancement()
            self.advance()

        # take the first expr and add it to the statement-list
        statement = res.register(self.expr())
        if res.error: return res
        mul_line_statements.append(statement)

        more_statements = True

        # now look for more statements
        while True:
            # count how many NEWLINES we have
            newline_count = 0
            while self.current_tok.type == Token.TOKEN_TYPES[20]:  # NEWLINE_TOKEN
                res.register_advancement()
                self.advance()
                newline_count += 1
            # if there are no newlines than set FALSE
            if newline_count == 0:
                more_statements = False

            if not more_statements: break

            # with try_register, check if the statement .....
            statement = res.try_register(self.expr())
            if not statement:
                self.reverse(res.to_reverse_count)
                more_statements = False
                continue
            mul_line_statements.append(statement)

        return res.success(ListNode(
            mul_line_statements,
            pos_start,
            self.current_tok.pos_end.copy()
        ))

    def func_def(self):
        res = ParseResult()

        if not self.current_tok.matches(Token.TOKEN_TYPES[4], 'def'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'def'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == Token.TOKEN_TYPES[3]:   # TT_IDENTIFIER
            func_name_tok = self.current_tok
            res.register_advancement()
            self.advance()
            if self.current_tok.type != Token.TOKEN_TYPES[10]: # TT_OPEN_PAR
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected '('"
                ))
        else:
            func_name_tok = None
            if self.current_tok.type != Token.TOKEN_TYPES[11]:  # TT_CLOSE_PAR
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected identifier or '('"
                ))

        res.register_advancement()
        self.advance()
        parameter_toks = []

        if self.current_tok.type == Token.TOKEN_TYPES[3]:  # TT_IDENTIFIER
            parameter_toks.append(self.current_tok)
            res.register_advancement()
            self.advance()

            while self.current_tok.type == Token.TOKEN_TYPES[18]:   # TT_COMMA
                res.register_advancement()
                self.advance()

                if self.current_tok.type != Token.TOKEN_TYPES[3]:   # TT_IDENTIFIER
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        f"Expected identifier"
                    ))

                parameter_toks.append(self.current_tok)
                res.register_advancement()
                self.advance()

            if self.current_tok.type != Token.TOKEN_TYPES[11]:  # TT_CLOSE_PAR
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected ',' or ')'"
                ))
        else:
            if self.current_tok.type != Token.TOKEN_TYPES[11]:  # TT_CLOSE_PAR
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected identifier or ')'"
                ))

        res.register_advancement()
        self.advance()
        if self.current_tok.type != Token.TOKEN_TYPES[22]:  # TT_COLON
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected ':'"
            ))
        res.register_advancement()
        self.advance()
        node_to_return = res.register(self.expr())
        '''
        # 25.10.22
        # TODO: MULTILINE
        # check the END statement
        if not self.current_tok.matches(Token.TOKEN_TYPES[4], 'END'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'END'"
            ))
        res.register_advancement()
        self.advance()
        '''
        if res.error: return res
        return res.success(FuncNode(
            func_name_tok,
            parameter_toks,
            node_to_return
        ))

    # 26.10.22
    # call: factor (OPEN_PAR(expr(COMMA expr)*)?CLOSE_PAR)?
    def call(self, call_name_tok):
        res = ParseResult()

        res.register_advancement()
        self.advance()

        if self.current_tok.type == Token.TOKEN_TYPES[11]:  # TT_CLOSE_PAR
            res.register_advancement()
            self.advance()
            return res.success(CallNode(call_name_tok))

        parameter_nodes = []
        while self.current_tok.type != Token.TOKEN_TYPES[11]:  # TT_CLOSE_PAR
            # first we will look for a factor
            factor = res.register(self.factor())
            if res.error: return res
            parameter_nodes.append(factor)

            if self.current_tok.type == Token.TOKEN_TYPES[18]:   # TT_COMMA
                res.register_advancement()
                self.advance()
            elif self.current_tok.type != Token.TOKEN_TYPES[11]:  # TT_CLOSE_PAR
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        f"Expected ',' or ')'"
                    ))

        res.register_advancement()
        self.advance()
        return res.success(CallNode(call_name_tok, parameter_nodes))

    def while_expr(self):
        ############
        # Syntax:    while CONDITION then expr
        # Give-Back: methode WhileNode with  condition and body-expr.
        ############
        res = ParseResult()

        # if not KEYWORD 'while', send back ERROR
        if not self.current_tok.matches(Token.TOKEN_TYPES[4], 'while'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'while'"
            ))

        # otherwise next token
        res.register_advancement()
        self.advance()

        # look for an expr, which will be the while-condition
        condition = res.register(self.expr())
        if res.error: return res

        # next expr will be the action after the then
        if not self.current_tok.matches(Token.TOKEN_TYPES[4], 'then'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'then'"
            ))

        # next token
        res.register_advancement()
        self.advance()

        # 12.09.2022
        # check for multiple line expr in body_expr
        if self.current_tok.type == Token.TOKEN_TYPES[20]:  # NEWLINE_TOKEN
            res.register_advancement()
            self.advance()

            body_expr = res.register(self.statement())
            if res.error: return res

            # TODO: use END Token to mark the end of the while body
            # e.g.:
            if not self.current_tok.matches(Token.TOKEN_TYPES[4], 'END'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected 'END'"
                ))

            res.register_advancement()
            self.advance()
            return res.success(WhileNode(condition, body_expr))

        body_expr = res.register(self.expr())
        if res.error: return res
        return res.success(WhileNode(condition, body_expr))

    def if_expr(self):
        ############
        # Syntax:    if CONDITION then expr else expr
        # Give-Back: IfNode as a list, contains [if-condition, action]
        #            and a optional 'else' as a tuple, if 'else' not given it is None
        ############

        res = ParseResult()
        # using the list cases, if there would be an ELIF implementation
        cases = []
        else_case = None

        # if not KEYWORD 'if', send back ERROR
        if not self.current_tok.matches(Token.TOKEN_TYPES[4], 'if'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'if'"
            ))

        # otherwise next token
        res.register_advancement()
        self.advance()

        # look for an expr, which will be the if-condition
        condition = res.register(self.expr())
        if res.error: return res

        # next expr will be the action after the then
        if not self.current_tok.matches(Token.TOKEN_TYPES[4], 'then'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'then'"
            ))

        # next token
        res.register_advancement()
        self.advance()

        # TODO: multiline
        # 12.09.2022
        # check for multiple line expr in body_expr
        if self.current_tok.type == Token.TOKEN_TYPES[20]:  # NEWLINE_TOKEN
            res.register_advancement()
            self.advance()

            expr = res.register(self.statement())
            if res.error: return res

            # TODO: use END Token to mark the end of the if body
            # e.g.:
            if not self.current_tok.matches(Token.TOKEN_TYPES[4], 'END'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected 'END'"
                ))

            res.register_advancement()
            self.advance()
            cases = (condition, expr)

            #### TODO: else part can be put in a function
            # check for an else-statement
            if self.current_tok.matches(Token.TOKEN_TYPES[4], 'else'):
                res.register_advancement()
                self.advance()

                # TODO: multiline
                # 12.09.2022
                # check for multiple line expr in body_expr
                if self.current_tok.type == Token.TOKEN_TYPES[20]:  # NEWLINE_TOKEN
                    res.register_advancement()
                    self.advance()

                    else_case = res.register(self.statement())
                    if res.error: return res

                    # TODO: use END Token to mark the end of the if body
                    # e.g.:
                    if not self.current_tok.matches(Token.TOKEN_TYPES[4], 'END'):
                        return res.failure(InvalidSyntaxError(
                            self.current_tok.pos_start, self.current_tok.pos_end,
                            f"Expected 'END'"
                        ))
                    res.register_advancement()
                    self.advance()
                    # return with if body and with else body
                    # Syntax: if <condition> then
                    #            expr*
                    #            END else
                    #            expr*
                    #            END
                    return res.success(IfNode(cases, else_case))

                else_case = res.register(self.expr())
                if res.error: return res
                # return with if body and with else one line
                # Syntax: if <condition> then
                #            expr*
                #            END else expr
                return res.success(IfNode(cases, else_case))

            # return with if body without else
            # Syntax: if <condition> then
            #            expr*
            #            END
            return res.success(IfNode(cases, else_case))

        ###########
        expr = res.register(self.expr())
        if res.error: return res
        cases = (condition, expr)  # cases.append((condition, expr))

        # TODO: ELIF,
        #  if ELIF should be implemented, it would be at this position,
        #  maybe with a while loop

        # check for an else-statement
        if self.current_tok.matches(Token.TOKEN_TYPES[4], 'else'):
            res.register_advancement()
            self.advance()

            # TODO: multiline
            # 12.09.2022
            # check for multiple line expr in body_expr
            if self.current_tok.type == Token.TOKEN_TYPES[20]:  # NEWLINE_TOKEN
                res.register_advancement()
                self.advance()

                else_case = res.register(self.statement())
                if res.error: return res

                # TODO: use END Token to mark the end of the if body
                # e.g.:
                if not self.current_tok.matches(Token.TOKEN_TYPES[4], 'END'):
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        f"Expected 'END'"
                    ))
                res.register_advancement()
                self.advance()
                # return without if body with else body
                # Syntax: if <condition> then expr else
                #            expr*
                #            END
                return res.success(IfNode(cases, else_case))

            else_case = res.register(self.expr())
            if res.error: return res
            # return without if body with else
            # Syntax: if <condition> then expr else expr
            return res.success(IfNode(cases, else_case))
        # return without if body, without else
        # Syntax: if <condition> then expr
        return res.success(IfNode(cases, else_case))

    # for; factor  : INT|FLOAT|STRING
    # 			   : (PLUS|MINUS) factor
    # 			   : LPAREN expr RPAREN
    #              : if-expr
    #              : while-expr
    #
    # for; if-expr : KEYWORD: if expr(is the condition) then expr
    #              : (KEYWORD: else expr)"else is optional"
    #
    # for; while-expr: KEYWORD: while expr(is the condition) then expr
    #
    # checking the factor of a term
    def factor(self):
        res = ParseResult()
        tok = self.current_tok  # get token

        # if- block check for; factor: (PLUS|MINUS) factor -> e.g. -5
        if tok.type in (
                token_.Token.TOKEN_TYPES[5], token_.Token.TOKEN_TYPES[6]):  # check if its is one, ADD_TOKEN SUB_TOKEN
            res.register_advancement()  # "E4"
            self.advance()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))

        # elif-block check for; factor  : INT|FLOAT -> e.g. 5
        elif tok.type in (token_.Token.TOKEN_TYPES[0], token_.Token.TOKEN_TYPES[1]):  # INT_TOKEN, FLOAT_TOKEN
            res.register_advancement()  # "E4"
            self.advance()
            return res.success(NumberNode(tok))

        # elif-block check if it is a saved variable
        elif tok.type == token_.Token.TOKEN_TYPES[3]:  # IDENTIFIER_Token
            res.register_advancement()
            self.advance()
            if self.current_tok.type == Token.TOKEN_TYPES[10]: # TT_OPEN_PAR
                call = res.register(self.call(tok))
                if res.error: return res
                return res.success(call)
            return res.success(VarAccessNode(tok))

        # elif-block check for; factor  : STRING -> e.g. "Hallo"
        elif tok.type in (token_.Token.TOKEN_TYPES[2]):  # STRING_Token
            res.register_advancement()
            self.advance()
            return res.success(StringNode(tok))

        # elif-block check for; factor : LPAREN expr RPAREN -> e.g. (5+1)*2
        elif tok.type == token_.Token.TOKEN_TYPES[10]:  # OPEN_PAR_TOKEN
            res.register_advancement()  # "E4"
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_tok.type == token_.Token.TOKEN_TYPES[
                11]:  # after an existing LPAREN, look for an RPAREN. CLOSE_PAR_TOKEN
                res.register_advancement()  # "E4"
                self.advance()
                return res.success(expr)
            else:  # else: return a failure that ")" is not found
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ')'"
                ))

        # elif-block check for; if-statement
        elif tok.matches(token_.Token.TOKEN_TYPES[4], 'if'):
            if_expr = res.register(self.if_expr())
            if res.error: return res
            return res.success(if_expr)

        # elif-block check for; while-statement
        elif tok.matches(token_.Token.TOKEN_TYPES[4], 'while'):
            while_expr = res.register(self.while_expr())
            if res.error: return res
            return res.success(while_expr)

        # elif-block check for; func-statement
        elif tok.matches(token_.Token.TOKEN_TYPES[4], 'def'):
            func_def = res.register(self.func_def())
            if res.error: return res
            return res.success(func_def)

        # if it fails:
        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            "factor failed: Expected..."
        ))

    # for; term    : factor ((MUL|DIV) factor)*
    # 26.10.22 self.factor changed to self.call
    def term(self):
        return self.bin_op(self.factor,
                           (token_.Token.TOKEN_TYPES[7], token_.Token.TOKEN_TYPES[8]))  # MUL_TOKEN DIV_TOKEN

    # for; arith-expr    : term ((PLUS|MINUS) term)*
    def arith_expr(self):
        return self.bin_op(self.term, (token_.Token.TOKEN_TYPES[5], token_.Token.TOKEN_TYPES[6]))

    # for; comp-expr: NOT comp-expr
    #      arith-expr ((EQ|GT|GTE|LT|LTE) arith-expr)*
    def comp_expr(self):
        res = ParseResult()

        # check for:
        # for; comp-expr: NOT comp-expr
        if self.current_tok.matches(token_.Token.TOKEN_TYPES[4], 'not'):
            op_tok = self.current_tok
            # res.register(self.advance())
            res.register_advancement()  # "E4"
            self.advance()
            node = res.register(self.comp_expr())

            if res.error: return res
            return res.success(UnaryOpNode(op_tok, node))

        # for;  arith-expr ((EQ|NEQ|GT|GTE|LT|LTE) arith-expr)*
        node = res.register(self.bin_op(self.arith_expr, (
            Token.TOKEN_TYPES[12], Token.TOKEN_TYPES[13], Token.TOKEN_TYPES[14],
            Token.TOKEN_TYPES[15], Token.TOKEN_TYPES[16], Token.TOKEN_TYPES[17])))

        # TODO here maybe catch an ERROR InvalidSyntaxXError
        # e.g.
        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "FEHLER_2: Expected int, float, identifier, '+', '-', '(' or 'NOT'"
            ))
        return res.success(node)

    # for; expr    : KEYWORD:   VAR  IDENTIFIER EQ expr
    #              : comp-expr: ((KEYWORD:AND|KEYWORD:OR) comp-expr)*
    def expr(self):
        res = ParseResult()

        # if true it is a VAR, else go on with BinarOP
        if self.current_tok.matches(token_.Token.TOKEN_TYPES[4], 'VAR'):
            # for; expr    : KEYWORD: VAR  IDENTIFIER EQ expr
            res.register(self.advance())

            # if not True failure, else it is an IDENTIFIER. go on with the EQ
            if self.current_tok.type != token_.Token.TOKEN_TYPES[3]:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier"))
            var_name = self.current_tok
            res.register(self.advance())

            # if not True failure, else it is EQ. go on with the expr
            if self.current_tok.type != token_.Token.TOKEN_TYPES[12]:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '='"))
            res.register(self.advance())
            expr = res.register(self.expr())
            # if ERROR return the res, else return VAR-Node
            if res.error: return res
            return res.success(VarNode(var_name, expr))

        # elif-block check for; if-statement
        # elif self.current_tok.matches(token_.Token.TOKEN_TYPES[4], 'if'):
        #    if_expr = res.register(self.if_expr())
        #    if res.error: return res
        #    return res.success(if_expr)

        ## OLD ##
        # for; expr    : term ((PLUS|MINUS) term)*
        # return self.bin_op(self.term, (token_.Token.TOKEN_TYPES[5], token_.Token.TOKEN_TYPES[6]))  # ADD_TOKEN SUB_TOKEN
        ## OLD ##

        # for; expr    : comp-expr ((KEYWORD: AND|KEYWORD: OR) comp-expr)*
        node = res.register(self.bin_op(self.comp_expr, ((token_.Token.TOKEN_TYPES[4], 'and'),
                                                         (token_.Token.TOKEN_TYPES[4],
                                                          'or'))))  # KEYWORD_AND, KEYWORD_OR
        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                ("FEHLER_3: Expected 'VAR', int, float, identifier, '+', '-', '(' or 'NOT'"
                 f"\n Token: {self.current_tok}")
            ))
        return res.success(node)

    ###################################

    # function is shared by several rules: def term, def expr etc.
    # parameters:
    #       func -> the rule: term, factor
    #       ops -> operation-token-list: PLUS, MINUS, DIV, MUL
    def bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())  # get the left factor, register gives back only the node
        if res.error: return res  # if there is an error from register

        # do as long a operation-token (+-*/) is inside or values inside
        while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
            op_tok = self.current_tok  # get the factor
            res.register(self.advance())
            right = res.register(func())  # get the next factor
            if res.error: return res
            left = BinOpNode(left, op_tok, right)  # create a new node

        # pass the successful node
        return res.success(left)  # return the BinOpNode, when it is successful


#######################################
# RUN
#######################################

def run(fn, text):  # pass the file-name and the text which need to be processed
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error  # check if there are errors

    # Generate AST (abstract syntax tree)
    parser = Parser(tokens)
    ast = parser.parse()

    return ast.node, ast.error
