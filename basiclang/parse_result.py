#######################################
# PARSE RESULT
#######################################

# here we check if there are any errors
class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0  ### NEW 06.09.2022
        self.to_reverse_count = 0  # NEW 12.09.2022

    def register_advancement(self):  ### NEW 06.09.2022
        self.advance_count += 1  ### NEW 06.09.2022

    def register(self, res):  # take another parser result or node
        if isinstance(res, ParseResult):
            if res.error: self.error = res.error
            return res.node
        return res

    def try_register(self, res):
        # this method checks if there is a failure,
        # if yes set to_reverse_count
        # else call the real register-methode
        if res.error:
            self.to_reverse_count = res.advance_count
            return None
        return self.register(res)

    # if success take the node
    def success(self, node):
        self.node = node
        return self

    # if error take the error
    def failure(self, error):
        if not self.error or self.advance_count == 0:  ### NEW 06.09.2022
            self.error = error
        return self
