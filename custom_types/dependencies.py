from typing import Annotated
from fastapi import Depends
from sqlmodel import Session

from models import User
from services.user import UserService
from services.auth import AuthService
from services.syllabus import SyllabusService
from config.database import get_db_session
from api.dependencies import (
    get_user_service,
    get_auth_service,
    get_syllabus_service,
    get_authenticated_user,
)


# Type aliases for dependencies
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
SyllabusServiceDep = Annotated[SyllabusService, Depends(get_syllabus_service)]
DBSessionDep = Annotated[Session, Depends(get_db_session)]
AuthenticatedUserDep = Annotated[User, Depends(get_authenticated_user)]
