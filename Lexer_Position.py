class Position:
    def __init__(self, index, line, column, filename, input):
        self.index = index
        self.line = line
        self.column = column
        self.filename = filename
        self.input = input

    def step(self, current_char = None):
        self.index += 1
        self.column += 1
        if current_char == '\n':
            self.line += 1
            self.column = 0
        return self

    def get_current_position(self):
        return Position(self.index, self.line, self.column, self.filename, self.input)