class FlowException(Exception):
    """Internal exceptions for flow control etc.
    Validation, config errors and such should use standard Python exception types"""
    pass


class StopProcessing(FlowException):
    """Stop processing of single item without too much error logging"""
    pass
