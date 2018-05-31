"""
Custom Exception handling for Ona app
"""


class ImproperMethod(Exception):
    """
    Custom Exception raised the the request Method is
    not Supported
    """

    message = 'Improper request method passed. Can only make GET or POST'
    'requests'


class InvalidResponse(Exception):
    """
    Custom Exception raised when the response is not
    a JSON
    """

    message = 'Response is not a JSON'
