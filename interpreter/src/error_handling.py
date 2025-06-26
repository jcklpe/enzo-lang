# Centralized error handling for Enzo

# Base class for all Enzo errors.
class EnzoError(Exception):
    pass

class EnzoParseError(EnzoError):
    pass

class EnzoRuntimeError(EnzoError):
    pass

class EnzoTypeError(EnzoError):
    pass

class InterpolationParseError(EnzoError):
    pass

class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value
