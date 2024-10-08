
class RuntimeException(Exception):
    def __init__(self, message):
        super().__init__(message)


class ParserException(RuntimeException):
    def __init__(self, message):
        super().__init__(message)

