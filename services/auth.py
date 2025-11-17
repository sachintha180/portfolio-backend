import os
import jwt
from datetime import datetime, timedelta, timezone
from uuid import UUID
from sqlmodel import Session

from models.user import User
from database.user import UserDatabase
from schemas.auth import AuthPayload, AuthRegister
from services.password import PasswordService
from custom_types.exceptions import (
    UserNotFoundError,
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    InvalidTokenError,
    RegistrationError,
)

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRATION = int(os.getenv("JWT_EXPIRATION", "3600"))


if not JWT_SECRET:
    raise ValueError("JWT_SECRET environment variable is not set")


class AuthService:
    """Service for authentication-related business logic."""

    def __init__(self, db: UserDatabase):
        """Initialize AuthService with a database dependency."""
        self.db = db

    def _verify_token(self, token: str) -> AuthPayload:
        """Verify and decode a JWT token."""
        try:
            payload = jwt.decode(
                token,
                JWT_SECRET,
                algorithms=[JWT_ALGORITHM],
            )
            return AuthPayload(**payload)
        except jwt.ExpiredSignatureError:
            raise InvalidTokenError("Token has expired")
        except jwt.InvalidTokenError:
            raise InvalidTokenError("Invalid token")

    def create_access_token(self, user: User) -> str:
        """Create an access token for a user."""
        payload = AuthPayload(
            sub=str(user.id),
            email=user.email,
            type=user.type,
            exp=datetime.now(timezone.utc) + timedelta(seconds=JWT_EXPIRATION),
        )
        return jwt.encode(
            payload.model_dump(),
            JWT_SECRET,
            algorithm=JWT_ALGORITHM,
        )

    def register(self, session: Session, user_data: AuthRegister) -> User:
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

    def get_current_user(self, session: Session, token: str) -> User:
        """Get the current user from a JWT token."""
        payload = self._verify_token(token)

        user = self.db.get_user_by_id(session, UUID(payload.sub))
        if not user:
            raise UserNotFoundError("User not found")

        return user
