# Centralized error handling for Enzo

# Base class for all Enzo errors.
class EnzoError(Exception):
    pass

class EnzoParseError(EnzoError):
    def __init__(self, message, line=None, column=None):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column

class EnzoRuntimeError(EnzoError):
    pass

class EnzoTypeError(EnzoError):
    pass

class InterpolationParseError(EnzoError):
    pass

class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value
