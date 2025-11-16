from typing import Optional
from datetime import datetime
from uuid import UUID
from sqlmodel import Session, select

from models.user import User
from schemas.user import UserCreate, UserUpdate
from core.interfaces import UserInterface


class UserDatabase(UserInterface):
    @staticmethod
    async def create_user(session: Session, user_data: UserCreate) -> User:
        user = User(
            **user_data.model_dump(),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    async def get_user_by_id(session: Session, user_id: UUID) -> Optional[User]:
        statement = select(User).where(User.id == user_id)
        return session.exec(statement).first()

    @staticmethod
    async def get_user_by_email(session: Session, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        return session.exec(statement).first()

    @staticmethod
    async def update_user(session: Session, user: User, user_data: UserUpdate) -> User:
        # NOTE: We use exclude_unset=True to exclude fields that are not set in the user_data,
        #       and setattr() to update the user object with the new values.
        update_dict = user_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(user, key, value)

        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    async def delete_user(session: Session, user: User) -> bool:
        session.delete(user)
        session.commit()
        return True
