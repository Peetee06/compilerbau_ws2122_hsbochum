class AbstractStackMachine:
    def __init__(self, ir):
        # intermediate representation
        self.ir = ir
        self.stack = []
        value = None

    def evaluate(self):
        # create list containing single instructions
        print(repr(self.ir))
        instructions = self.ir.split("\n")[:-1]
        print(instructions)

        def op(operator):
            
            # second operand is on top of stack
            # first operand is just below that
            second = self.stack.pop()
            first = self.stack.pop()
            
            result = str(eval(f"{first} {operator} {second}"))

            self.stack.append(result)
        
        instruction_mapping = {
                "ADD": lambda: op("+"),
                "SUB": lambda: op("-"),
                "MUL": lambda: op("*"),
                "DIV": lambda: op("/")
                }


        for instruction in instructions:
            if "LOAD" in instruction:
                value = instruction.split()[-1]
                self.stack.append(value)

            else:
                instruction_mapping[instruction]()
            print(self.stack)
        
        value = self.stack.pop()
        return value
                
