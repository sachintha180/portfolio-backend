from uuid import UUID
from fastapi import APIRouter, Depends, status

from schemas.user import (
    UserUpdateRequest,
    UserGetResponse,
    UserUpdateResponse,
)
from custom_types.dependencies import DBSessionDep, UserServiceDep
from api.dependencies import (
    get_authenticated_user,
    get_user_service,
)

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[
        Depends(get_authenticated_user),  # NOTE: This already gets the db_session
        Depends(get_user_service),
    ],
)


@router.get(
    "/{user_id}",
    response_model=UserGetResponse,
    status_code=status.HTTP_200_OK,
)
def get_user(
    user_id: UUID,
    user_service: UserServiceDep,
    db_session: DBSessionDep,
):
    """Get a user by ID."""
    user = user_service.get_user_by_id(db_session, user_id)

    return UserGetResponse(user=user)


@router.patch(
    "/{user_id}",
    response_model=UserUpdateResponse,
    status_code=status.HTTP_200_OK,
)
def update_user(
    user_id: UUID,
    request_data: UserUpdateRequest,
    user_service: UserServiceDep,
    db_session: DBSessionDep,
):
    """Update a user."""
    user = user_service.update_user(db_session, user_id, request_data)

    return UserUpdateResponse(user=user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(
    user_id: UUID,
    user_service: UserServiceDep,
    db_session: DBSessionDep,
):
    """Delete a user."""
    user_service.delete_user(db_session, user_id)
