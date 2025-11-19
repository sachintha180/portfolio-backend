from uuid import UUID
from sqlmodel import Session

from models.user import User
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

    def get_user_by_id(self, session: Session, user_id: UUID) -> User:
        """Get a user by ID."""
        user = self.db.get_user_by_id(session, user_id)
        if not user:
            raise UserNotFoundError("User not found")

        return user

    def update_user(
        self, session: Session, user_id: UUID, user_data: UserUpdateRequest
    ) -> User:
        """Update a user with validation."""
        user = self.db.get_user_by_id(session, user_id)
        if not user:
            raise UserNotFoundError("User not found")

        if user_data.email and user_data.email != user.email:
            existing_user = self.db.get_user_by_email(session, user_data.email)
            if existing_user:
                raise EmailAlreadyExistsError("Email already in use")

        try:
            updated_user = self.db.update_user(session, user, user_data)
        except Exception as e:
            raise DatabaseError("Failed to update user") from e

        return updated_user

    def delete_user(self, session: Session, user_id: UUID) -> bool:
        """Delete a user."""
        user = self.db.get_user_by_id(session, user_id)
        if not user:
            raise UserNotFoundError("User not found")

        try:
            self.db.delete_user(session, user)
        except Exception as e:
            raise DatabaseError("Failed to delete user") from e

        return True
