#######################################
# POSITION
#######################################

# track the line-number, column-number und current index
class Position:
    def __init__(self, idx, ln, col, fn,
                 ftxt):  # fn and ftext for file-name and file-content, to tell the user where the error is
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None):  # move to next index and at new col. and index, if necessary
        self.idx += 1
        self.col += 1

        if current_char == '\n':  # if new line, increment line and reset column.
            self.ln += 1
            self.col = 0

        return self

    def get(self):  # create copy of the position
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)