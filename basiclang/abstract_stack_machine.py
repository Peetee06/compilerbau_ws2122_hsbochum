class AbstractStackMachine:
    def __init__(self, ir):
        # intermediate representation
        self.ir = ir
        self.stack = []
        self.tmp_stack = []
        self.jump_stack = []
        self.value = None
        global_symbol_table = {}
        self.symbol_tables = [global_symbol_table]

    def evaluate(self):
        # create list containing single instructions
        instructions = self.ir.split("\n")[:-1]

        def op(operator):
            binary_bool_operators = [
                "<",
                ">",
                "<=",
                ">=",
                "==",
                "!=",
                "and",
                "or",
            ]

            if operator == "not":
                # unary operator just pop one element
                el = self.stack.pop()
                result = eval(f"int({operator} {el})")

            else:
                first = self.stack.pop()
                second = self.stack.pop()

                if operator in binary_bool_operators:
                    result = eval(f"int({first} {operator} {second})")
                else:
                    result = eval(f"{first} {operator} {second}")

            self.stack.append(result)

        instruction_mapping = {
            "ADD": lambda: op("+"),
            "SUB": lambda: op("-"),
            "MUL": lambda: op("*"),
            "DIV": lambda: op("/"),
            "LT": lambda: op("<"),
            "GT": lambda: op(">"),
            "LTE": lambda: op("<="),
            "GTE": lambda: op(">="),
            "EQ": lambda: op("=="),
            "NE": lambda: op("!="),
            "and": lambda: op("and"),
            "or": lambda: op("or"),
            "not": lambda: op("not"),
        }

        label_new = False
        func_def = False
        jump_to = ""

        # pairs of label and idx to jump to
        jumps = {}

        # position in input
        pos = 0
        while pos < len(instructions):
            current = instructions[pos]
            if "FUNCDEF" in current:
                # function definition follow, skip to end of it
                func_def = True

            elif "LABEL" in current:
                # store labels inputstream position
                label = current.split()[-1]
                jumps[label] = pos
                # check if we are looking for a not yet stored label
                if label_new:
                    # skip instructions until at new label
                    if jump_to in current:
                        # found new jump label, stop jump
                        label_new = False

                    else:
                        # not the label we are looking for
                        pass

                else:
                    # not jumping, can skip label
                    pass

            elif func_def:
                if "GOTOSTACK" in current:
                    # end of function definition
                    func_def = False

                else:
                    # still in function definition, skip this instruction
                    pass

            elif label_new:
                # did not find new label to jump to
                # skip current instruction
                pass

            elif "LOAD" in current:
                # receives string in the form of
                # LOAD X
                # where X is a value
                # extract the value from that string
                type_, t_value = current.split()[-1].split(":")
                if type_ == "INT":
                    value = int(t_value)
                elif type_ == "FLOAT":
                    value = float(t_value)
                elif type_ == "IDENTIFIER":
                    try:
                        value = self.symbol_tables[-1][t_value]
                    except KeyError:
                        raise NameError(f"Symbol {t_value} not defined yet")
                else:
                    # type is string
                    # no typecasting necessary
                    value = t_value

                self.stack.append(value)

            elif "STORE" in current:
                # retrieve evaluated expression from stack
                value = self.stack.pop()
                # get identifier
                identifier = current.split()[-1]
                # add to symbol table
                self.symbol_tables[-1][identifier] = value

            elif "GOFALSE" in current:
                if not self.stack.pop():
                    # condition is false
                    # get label to jump to
                    jump_to = current.split()[-1]
                    if jump_to in jumps:
                        # already stored position of this label
                        # jump immediately
                        pos = jumps[jump_to]
                    else:
                        # didn't store position of this label yet
                        # have to advance to find it
                        label_new = True

            elif "GOTRUE" in current:
                if self.stack.pop():
                    # condition is true
                    # get label to jump to
                    jump_to = current.split()[-1]
                    if jump_to in jumps:
                        # already stored position of this label
                        # jump immediately
                        pos = jumps[jump_to]
                    else:
                        # didn't store position of this label yet
                        # have to advance to find it
                        label_new = True

            elif "GOTO" in current:
                # get label to jump to
                if "GOTOSTACK" in current:
                    # label is on jump stack
                    jump_to = self.jump_stack.pop()
                    if "func_return" in jump_to:
                        # finished computing function
                        # drop local symbol table
                        self.symbol_tables.pop()
                        function_result = self.stack.pop()
                        # restore main stack
                        self.stack = self.tmp_stack
                        # push function result to main tmp_stack
                        self.stack.append(function_result)

                else:
                    # label is in current string
                    jump_to = current.split()[-1]

                if "func_in" in jump_to:
                    # store stack to tmp stack for function calculations
                    self.tmp_stack = self.stack.copy()

                    # jumping to function, have to create symbol table
                    local_symbol_table = self.symbol_tables[-1].copy()
                    self.symbol_tables.append(local_symbol_table)

                if jump_to in jumps:
                    # already stored position of this label
                    # jump immediately
                    pos = jumps[jump_to]
                else:
                    # didn't store position of this label yet
                    # have to advance to find it
                    label_new = True

            elif "MOVE" in current:
                # extract jump label
                label = current.split()[-1]

                # write jump address to jump stack
                self.jump_stack.append(label)

            elif "HALT" in current:
                # program finished
                break

            else:

                instruction_mapping[current]()

            pos += 1

        try:
            self.value = self.stack.pop()
        except IndexError:
            # nothing to return
            self.value = None

        return self.value
