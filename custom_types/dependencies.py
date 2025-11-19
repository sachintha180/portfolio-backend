from typing import Annotated
from fastapi import Depends
from sqlmodel import Session

from models.user import User
from services.user import UserService
from services.auth import AuthService
from config.database import get_db_session
from api.dependencies import (
    get_user_service,
    get_auth_service,
    get_authenticated_user,
)


# Type aliases for dependencies
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
DBSessionDep = Annotated[Session, Depends(get_db_session)]
AuthenticatedUserDep = Annotated[User, Depends(get_authenticated_user)]
