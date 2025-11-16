class BaseAppException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class UserNotFoundError(BaseAppException):
    def __init__(self, user_id: str | None = None):
        message = "User not found"
        if user_id:
            message = f"User with ID '{user_id}' not found"
        super().__init__(message)


class DuplicateEmailError(BaseAppException):
    def __init__(self, email: str):
        message = f"User with email '{email}' already exists"
        super().__init__(message)
