"""
This module contains the error types for both schema processing and validation.
"""


class SchemaError(Exception):
    """
    This class represents error occurring during schema processing.
    """
    def __init__(self,
                 path: str,
                 msg: str):
        super().__init__()
        self.path = path
        self.msg = msg

    def __str__(self):
        return 'SchemaError - Path: {0} - {1}'.format(self.path, self.msg)


class ValidationError(Exception):
    """
    This class represents validation errors.
    """
    def __init__(self,
                 path: str,
                 msg: str):
        super().__init__()
        self.path = path
        self.msg = msg

    def __str__(self):
        return 'ValidationError - Path: {0} - {1}'.format(self.path, self.msg)
