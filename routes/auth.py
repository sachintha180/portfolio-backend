from fastapi import APIRouter, status

from schemas.auth import AuthLogin, AuthRegister, AuthToken
from custom_types.dependencies import AuthServiceDep, DBSessionDep

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthToken, status_code=status.HTTP_201_CREATED)
def register(
    user_data: AuthRegister,
    auth_service: AuthServiceDep,
    session: DBSessionDep,
):
    """Register a new user and return an access token."""
    user = auth_service.register(session, user_data)
    access_token = auth_service.create_access_token(user)
    return AuthToken(access_token=access_token)


@router.post("/login", response_model=AuthToken, status_code=status.HTTP_200_OK)
def login(
    credentials: AuthLogin,
    auth_service: AuthServiceDep,
    session: DBSessionDep,
):
    """Authenticate a user and return an access token."""
    user = auth_service.login(session, credentials.email, credentials.password)
    access_token = auth_service.create_access_token(user)
    return AuthToken(access_token=access_token)
