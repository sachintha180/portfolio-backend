from typing import Annotated, NamedTuple
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session

from database.user import UserDatabase
from services.user import UserService
from services.auth import AuthService
from models.user import User
from config.database import get_db_session

security = HTTPBearer()


# Dependency context types
class AuthenticatedContext(NamedTuple):
    """Bundled dependencies for authenticated routes."""

    current_user: User
    session: Session


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


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    session: Annotated[Session, Depends(get_db_session)],
) -> User:
    """Dependency that verifies JWT token and returns the current authenticated user."""
    token = credentials.credentials
    return auth_service.get_current_user(session, token)


# Bundled dependency factories
def get_authenticated_context(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_db_session)],
) -> AuthenticatedContext:
    """Bundled dependency for authenticated routes that need user and session."""
    return AuthenticatedContext(
        current_user=current_user,
        session=session,
    )
