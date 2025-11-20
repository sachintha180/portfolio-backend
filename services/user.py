from uuid import UUID
from sqlmodel import Session

from models import User

from schemas.user import UserUpdateRequest
from database.user import UserDatabase
from custom_types.exceptions import (
    UserNotFoundError,
    EmailAlreadyExistsError,
    DatabaseError,
)


class UserService:
    """Service for user-related business logic."""

    def __init__(self, db: UserDatabase):
        """Initialize UserService with a database dependency."""
        self.db = db

    def get_user_by_id(self, db_session: Session, user_id: UUID) -> User:
        """Get a user by ID."""
        user = self.db.get_user_by_id(db_session, user_id)
        if not user:
            raise UserNotFoundError

        return user

    def update_user(
        self, db_session: Session, user_id: UUID, user_data: UserUpdateRequest
    ) -> User:
        """Update a user with validation."""
        user = self.db.get_user_by_id(db_session, user_id)
        if not user:
            raise UserNotFoundError

        if user_data.email and user_data.email != user.email:
            existing_user = self.db.get_user_by_email(db_session, user_data.email)
            if existing_user:
                raise EmailAlreadyExistsError

        try:
            updated_user = self.db.update_user(db_session, user, user_data)
        except Exception as e:
            raise DatabaseError("Failed to update user") from e

        return updated_user

    def delete_user(self, db_session: Session, user_id: UUID) -> bool:
        """Delete a user."""
        user = self.db.get_user_by_id(db_session, user_id)
        if not user:
            raise UserNotFoundError

        try:
            self.db.delete_user(db_session, user)
        except Exception as e:
            raise DatabaseError("Failed to delete user") from e

        return True
