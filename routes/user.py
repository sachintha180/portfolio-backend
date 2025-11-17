from uuid import UUID
from fastapi import APIRouter, status

from schemas.user import UserUpdate
from models.user import User
from custom_types.dependencies import AuthenticatedContextDep, UserServiceDep

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/get/{user_id}", response_model=User)
def get_user(
    user_id: UUID,
    service: UserServiceDep,
    ctx: AuthenticatedContextDep,
):
    """Get a user by ID."""
    return service.get_user_by_id(ctx.session, user_id)


@router.patch("/update/{user_id}", response_model=User)
def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    service: UserServiceDep,
    ctx: AuthenticatedContextDep,
):
    """Update a user."""
    return service.update_user(ctx.session, user_id, user_data)


@router.delete(
    "/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT
)  # NOTE: Returns 204 because there's no response body
def delete_user(
    user_id: UUID,
    service: UserServiceDep,
    ctx: AuthenticatedContextDep,
):
    """Delete a user."""
    service.delete_user(ctx.session, user_id)
