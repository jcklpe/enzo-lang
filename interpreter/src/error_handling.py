# Centralized error handling for Enzo

# Base class for all Enzo errors.
class EnzoError(Exception):
    pass

class EnzoParseError(EnzoError):
    def __init__(self, message, line=None, column=None, code_line=None):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column
        self.code_line = code_line

class EnzoRuntimeError(EnzoError):
    def __init__(self, message, code_line=None):
        super().__init__(message)
        self.message = message
        self.code_line = code_line

class EnzoTypeError(EnzoRuntimeError):
    pass

class InterpolationParseError(EnzoParseError):
    pass

class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value
