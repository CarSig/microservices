# app/exceptions.py
class AppException(Exception):
    status_code: int = 500
    error_code: str = "INTERNAL_ERROR"

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFound(AppException):
    status_code = 404
    error_code = "NOT_FOUND"


class Conflict(AppException):
    status_code = 409
    error_code = "CONFLICT"
