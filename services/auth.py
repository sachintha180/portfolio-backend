import jwt
from datetime import datetime, timedelta, timezone
from uuid import UUID
from sqlmodel import Session

from models.user import User
from database.user import UserDatabase
from schemas.auth import TokenPayload, AuthRegisterRequest
from services.password import PasswordService
from custom_types.exceptions import (
    UserNotFoundError,
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    InvalidTokenError,
    RegistrationError,
    NotAuthenticatedError,
)
from custom_types.enums import TokenType
from config.auth import (
    JWT_SECRET,
    JWT_ALGORITHM,
    COOKIE_MAX_AGE_ACCESS,
    COOKIE_MAX_AGE_REFRESH,
)


class AuthService:
    """Service for authentication-related business logic."""

    def __init__(self, db: UserDatabase):
        """Initialize AuthService with a database dependency."""
        self.db = db

    def _verify_token(self, token: str) -> TokenPayload:
        """Verify and decode a JWT token."""
        try:
            payload = jwt.decode(
                token,
                JWT_SECRET,
                algorithms=[JWT_ALGORITHM],
            )
            return TokenPayload(**payload)
        except jwt.ExpiredSignatureError:
            raise InvalidTokenError("Token has expired")
        except jwt.InvalidTokenError:
            raise InvalidTokenError("Invalid token")

    def create_token(self, user: User, token_type: TokenType) -> str:
        """Create an access / refresh token for a user."""
        expiration_time = (
            COOKIE_MAX_AGE_ACCESS
            if token_type == TokenType.ACCESS
            else COOKIE_MAX_AGE_REFRESH
        )
        payload = TokenPayload(
            sub=str(user.id),
            email=user.email,
            type=user.type,
            exp=datetime.now(timezone.utc) + timedelta(seconds=expiration_time),
        )
        return jwt.encode(
            payload.model_dump(),
            JWT_SECRET,
            algorithm=JWT_ALGORITHM,
        )

    def register(self, session: Session, user_data: AuthRegisterRequest) -> User:
        """Register a new user."""
        existing_user = self.db.get_user_by_email(session, user_data.email)
        if existing_user:
            raise EmailAlreadyExistsError("Email already in use")

        hashed_password = PasswordService.hash_password(user_data.password)

        try:
            user = self.db.create_user(session, user_data, hashed_password)
        except Exception as e:
            raise RegistrationError("Failed to register user") from e

        return user

    def login(self, session: Session, email: str, password: str) -> User:
        """Authenticate a user."""
        user = self.db.get_user_by_email(session, email)
        if not user:
            raise InvalidCredentialsError("Invalid email or password")

        if not PasswordService.verify_password(password, user.password):
            raise InvalidCredentialsError("Invalid email or password")

        return user

    def verify_authentication(self, session: Session, token: str | None) -> User:
        """Verify authentication token and return the authenticated user."""
        if not token:
            raise NotAuthenticatedError("Not authenticated")

        payload = self._verify_token(token)

        user = self.db.get_user_by_id(session, UUID(payload.sub))
        if not user:
            raise UserNotFoundError("User not found")

        return user
