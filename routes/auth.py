from fastapi import APIRouter, Request, Response, status

from schemas.auth import (
    AuthRegisterRequest,
    AuthRegisterResponse,
    AuthLoginRequest,
    AuthLoginResponse,
    AuthVerifyUser,
    AuthVerifyResponse,
    AuthRefreshResponse,
)
from custom_types.dependencies import AuthServiceDep, DBSessionDep
from custom_types.enums import TokenType
from config.auth import (
    ACCESS_TOKEN_COOKIE_NAME,
    REFRESH_TOKEN_COOKIE_NAME,
    COOKIE_MAX_AGE_ACCESS,
    COOKIE_MAX_AGE_REFRESH,
)
from config.environment import COOKIE_HTTP_ONLY, COOKIE_SECURE, COOKIE_SAME_SITE

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=AuthRegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    request_data: AuthRegisterRequest,
    auth_service: AuthServiceDep,
    db_session: DBSessionDep,
    response: Response,
):
    """Register a new user and set access and refresh tokens as HTTP-only cookies."""
    user = auth_service.register(db_session, request_data)
    access_token = auth_service.create_token(user, TokenType.ACCESS)
    refresh_token = auth_service.create_token(user, TokenType.REFRESH)

    # Set HTTP-only cookies
    response.set_cookie(
        key=ACCESS_TOKEN_COOKIE_NAME,
        value=access_token,
        max_age=COOKIE_MAX_AGE_ACCESS,
        httponly=COOKIE_HTTP_ONLY,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAME_SITE,
        path="/",
    )
    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE_NAME,
        value=refresh_token,
        max_age=COOKIE_MAX_AGE_REFRESH,
        httponly=COOKIE_HTTP_ONLY,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAME_SITE,
        path="/",
    )

    return AuthRegisterResponse(user=user)


@router.post(
    "/login",
    response_model=AuthLoginResponse,
    status_code=status.HTTP_200_OK,
)
def login(
    request_data: AuthLoginRequest,
    auth_service: AuthServiceDep,
    db_session: DBSessionDep,
    response: Response,
):
    """Authenticate a user and set access and refresh tokens as HTTP-only cookies."""
    user = auth_service.login(db_session, request_data.email, request_data.password)
    access_token = auth_service.create_token(user, TokenType.ACCESS)
    refresh_token = auth_service.create_token(user, TokenType.REFRESH)

    # Set HTTP-only cookies
    response.set_cookie(
        key=ACCESS_TOKEN_COOKIE_NAME,
        value=access_token,
        max_age=COOKIE_MAX_AGE_ACCESS,
        httponly=COOKIE_HTTP_ONLY,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAME_SITE,
        path="/",
    )
    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE_NAME,
        value=refresh_token,
        max_age=COOKIE_MAX_AGE_REFRESH,
        httponly=COOKIE_HTTP_ONLY,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAME_SITE,
        path="/",
    )

    return AuthLoginResponse(user=user)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response):
    """Logout user by clearing HTTP-only cookies."""

    # Clear HTTP-only cookies
    response.delete_cookie(
        key=ACCESS_TOKEN_COOKIE_NAME,
        httponly=COOKIE_HTTP_ONLY,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAME_SITE,
        path="/",
    )
    response.delete_cookie(
        key=REFRESH_TOKEN_COOKIE_NAME,
        httponly=COOKIE_HTTP_ONLY,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAME_SITE,
        path="/",
    )


@router.get(
    "/verify",
    response_model=AuthVerifyResponse,
    status_code=status.HTTP_200_OK,
)
def verify(
    request: Request,
    auth_service: AuthServiceDep,
    db_session: DBSessionDep,
):
    """Verify the current user's authentication status from HTTP-only cookie."""

    token = request.cookies.get(ACCESS_TOKEN_COOKIE_NAME)
    user = auth_service.verify_authentication(db_session, token)

    return AuthVerifyResponse(
        authenticated=user is not None,
        user=user
        and AuthVerifyUser(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            type=user.type,
        ),
    )


@router.post(
    "/refresh",
    response_model=AuthRefreshResponse,
    status_code=status.HTTP_200_OK,
)
def refresh(
    request: Request,
    auth_service: AuthServiceDep,
    db_session: DBSessionDep,
    response: Response,
):
    """Refresh the current user's access token using refresh token from HTTP-only cookie."""

    refresh_token = request.cookies.get(REFRESH_TOKEN_COOKIE_NAME)
    user = auth_service.refresh_token(db_session, refresh_token)

    access_token = auth_service.create_token(user, TokenType.ACCESS)

    # Set HTTP-only cookie
    response.set_cookie(
        key=ACCESS_TOKEN_COOKIE_NAME,
        value=access_token,
        max_age=COOKIE_MAX_AGE_ACCESS,
        httponly=COOKIE_HTTP_ONLY,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAME_SITE,
        path="/",
    )

    return AuthRefreshResponse(user=user)
