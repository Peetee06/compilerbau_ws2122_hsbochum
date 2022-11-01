#######################################
# ERRORS
#######################################

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    # show the Error
    def as_string(self):
        result = f'{self.error_name}: {self.details}\n'  # display the error
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'  # display the file-name and the line-number
        return result
