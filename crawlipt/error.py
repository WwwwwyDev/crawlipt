class VariableError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class ParamTypeError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
