from typing import Annotated
from fastapi import Depends, Request
from sqlmodel import Session

from database.user import UserDatabase
from services.user import UserService
from services.auth import AuthService
from models.user import User
from config.database import get_db_session
from config.auth import ACCESS_TOKEN_COOKIE_NAME


# Dependency factories
def get_user_db() -> UserDatabase:
    """Dependency factory for user database."""
    return UserDatabase()


def get_user_service(
    db: Annotated[UserDatabase, Depends(get_user_db)],
) -> UserService:
    """Dependency factory for user service."""
    return UserService(db=db)


def get_auth_service(
    db: Annotated[UserDatabase, Depends(get_user_db)],
) -> AuthService:
    """Dependency factory for auth service."""
    return AuthService(db=db)


def get_authenticated_user(
    request: Request,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    db_session: Annotated[Session, Depends(get_db_session)],
) -> User:
    """Dependency that verifies JWT token from HTTP-only cookie and returns the current authenticated user."""
    token = request.cookies.get(ACCESS_TOKEN_COOKIE_NAME)
    return auth_service.verify_authentication(db_session, token)
