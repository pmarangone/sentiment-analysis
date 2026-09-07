class AppError(Exception):
    """Base class for exceptions in this module."""
    pass

class ReviewNotFound(AppError):
    """Raised when a review is not found."""
    pass

class ServiceError(AppError):
    """Raised when a service error occurs."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
