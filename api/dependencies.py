from typing import Annotated
from fastapi import Depends, Request
from typing import Optional
from sqlmodel import Session

from database.user import UserDatabase
from database.syllabus import SyllabusDatabase
from services.user import UserService
from services.auth import AuthService
from services.syllabus import SyllabusService
from models import User
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


def get_syllabus_db() -> SyllabusDatabase:
    """Dependency factory for syllabus database."""
    return SyllabusDatabase()


def get_syllabus_service(
    db: Annotated[SyllabusDatabase, Depends(get_syllabus_db)],
) -> SyllabusService:
    """Dependency factory for syllabus service."""
    return SyllabusService(db=db)


def get_authenticated_user(
    request: Request,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    db_session: Annotated[Session, Depends(get_db_session)],
) -> Optional[User]:
    """Dependency that verifies JWT token from HTTP-only cookie and returns the current authenticated user."""
    token = request.cookies.get(ACCESS_TOKEN_COOKIE_NAME)
    return auth_service.verify_authentication(db_session, token)
