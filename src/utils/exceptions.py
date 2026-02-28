"""
Custom exceptions
"""


class SMHuntException(Exception):
    """Base exception for SMHunt application"""
    pass


class BusinessNotFoundException(SMHuntException):
    """Raised when business is not found"""
    pass


class InvalidBusinessDataException(SMHuntException):
    """Raised when business data is invalid"""
    pass


class EmailSendingException(SMHuntException):
    """Raised when email sending fails"""
    pass
