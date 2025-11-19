from typing import Optional
from uuid import UUID
from sqlmodel import Session, select

from models.user import User
from schemas.auth import AuthRegisterRequest
from schemas.user import UserUpdateRequest


class UserDatabase:
    """Database layer for user operations."""

    def create_user(
        self, db_session: Session, user_data: AuthRegisterRequest, hashed_password: str
    ) -> User:
        """Create a new user in the database."""
        user = User(
            **user_data.model_dump(
                exclude={"password"},
            ),
            password=hashed_password,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    def get_user_by_id(self, db_session: Session, user_id: UUID) -> Optional[User]:
        """Get a user by ID."""
        statement = select(User).where(User.id == user_id)
        return db_session.exec(statement).first()

    def get_user_by_email(self, db_session: Session, email: str) -> Optional[User]:
        """Get a user by email."""
        statement = select(User).where(User.email == email)
        return db_session.exec(statement).first()

    def update_user(
        self, db_session: Session, user: User, user_data: UserUpdateRequest
    ) -> User:
        """Update a user in the database."""
        update_dict = user_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(user, key, value)

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    def delete_user(self, db_session: Session, user: User) -> bool:
        """Delete a user from the database."""
        db_session.delete(user)
        db_session.commit()
        return True
