class AbstractStackMachine:
    def __init__(self, ir):
        # intermediate representation
        self.ir = ir
        self.stack = []
        self.value = None
        self.symbol_table = {}


    def evaluate(self):
        # create list containing single instructions
        print(repr(self.ir))
        instructions = self.ir.split("\n")[:-1]
        print(instructions)

        def op(operator):
            
            if operator == "not":
                # unary operator just pop one element
                el = self.stack.pop()
                result = eval(f"int({operator} {el})")

            else:
                # second operand is on top of stack
                # first operand is just below that
                second = self.stack.pop()
                first = self.stack.pop()
                
                print(f"evaluating: {first} {operator} {second}")
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
                "not": lambda: op("not")
                }

        jump = False
        jump_to = ""

        # pairs of label and idx to jump to
        jumps = {}
        
        # TODO testcode
        w_counter = 0
        # position in input
        pos = 0
        while pos < len(instructions) and w_counter < 5:
            current = instructions[pos]
            print(f"current instruction: {current}")
            if "LABEL" in current:
                # store labels position in inputstream
                label = current.split()[-1]
                jumps[label] = pos
                # check if actually jumping
                if jump:
                    # skip instructions until at jump label
                    if jump_to in current:
                        # found jump label, stop jump
                        jump = False

                    else: 
                        # not the label we are looking for
                        pass

                else:
                    # not jumping, can skip label 
                    pass

            elif jump:
                # did not find label to jump to
                # skip current instruction
                print("still jumping, skipping current instruction")
                pass

            elif "LOAD" in current:
                # receives string in the form of
                # LOAD X
                # where X is a value
                # extract the value from that string
                type_, value = current.split()[-1].split(":")
                if type_ == "INT":
                    value = int(value)
                elif type_ == "FLOAT":
                    value = float(value)
                elif type_ == "IDENTIFIER":
                    try:
                        value = self.symbol_table[value]
                    except KeyError:
                        print(f"the identifier {value} is not initialized yet")
                else:
                    # type is string
                    # no typecasting necessary
                    pass

                self.stack.append(value)

            elif "STORE" in current:
                # retrieve evaluated expression from stack
                value = self.stack.pop()
                # get identifier
                identifier = current.split()[-1]
                # add to symbol table
                self.symbol_table[identifier] = value

            elif "GOFALSE" in current:
                if not self.stack.pop():
                    # condition is false
                    # get label to jump to
                    jump_to = current.split()[-1]
                    if jump_to in jumps:
                        # already stored position of this label
                        # jump immediately
                        pos = jumps[jump_to]
                        # TODO
                        w_counter += 1
                    else:
                        # didn't store position of this label yet
                        # have to advance to find it
                        jump = True
                    print(f"jumping to {jump_to}")

            elif "GOTRUE" in current:
                if self.stack.pop():
                    # condition is true
                    # get label to jump to
                    jump_to = current.split()[-1]
                    if jump_to in jumps:
                        # already stored position of this label
                        # jump immediately
                        pos = jumps[jump_to]
                        # TODO
                        w_counter += 1
                    else:
                        # didn't store position of this label yet
                        # have to advance to find it
                        jump = True
                    print(f"jumping to {jump_to}")

            elif "GOTO" in current:
                # get label to jump to
                jump_to = current.split()[-1]
                if jump_to in jumps:
                    # already stored position of this label
                    # jump immediately
                    pos = jumps[jump_to]
                    # TODO
                    w_counter += 1
                else:
                    # didn't store position of this label yet
                    # have to advance to find it
                    jump = True
                print(f"jumping to {jump_to}")

            else:

                instruction_mapping[current]()
            
            print(self.stack)
            pos += 1
        
        self.value = self.stack.pop()
        return self.value
                
