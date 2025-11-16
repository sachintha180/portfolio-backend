from typing import Optional
from uuid import UUID
from sqlmodel import Session
from passlib.context import CryptContext

from models.user import User
from schemas.user import UserCreate, UserUpdate
from custom_types.exceptions import UserNotFoundError, DuplicateEmailError
from database.user import UserDatabase
from core.interfaces import UserInterface

# Initialize passlib context with default settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService(UserInterface):
    @staticmethod
    def _hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def _verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    async def _check_if_user_exists_by_email(
        session: Session, email: str
    ) -> Optional[User]:
        existing_user = await UserDatabase.get_user_by_email(session, email)
        if existing_user:
            raise DuplicateEmailError(email)
        return existing_user

    @staticmethod
    async def create_user(session: Session, user_data: UserCreate) -> User:
        await UserService._check_if_user_exists_by_email(session, user_data.email)
        user_data.password = UserService._hash_password(user_data.password)
        user = await UserDatabase.create_user(session, user_data)
        return user

    @staticmethod
    async def _check_if_user_exists_by_id(
        session: Session, user_id: UUID
    ) -> Optional[User]:
        existing_user = await UserDatabase.get_user_by_id(session, user_id)
        if existing_user:
            raise UserNotFoundError(str(user_id))
        return existing_user

    @staticmethod
    async def update_user(
        session: Session, user_id: UUID, user_data: UserUpdate
    ) -> User:
        user = await UserService._check_if_user_exists_by_id(session, user_id)
        assert (
            user is not None
        ), "Cannot update user, user not found."  # NOTE: To keep the type checker happy.
        if user_data.email:
            await UserService._check_if_user_exists_by_email(session, user_data.email)
        updated_user = await UserDatabase.update_user(session, user, user_data)
        return updated_user

    @staticmethod
    async def delete_user(session: Session, user_id: UUID) -> bool:
        user = await UserService._check_if_user_exists_by_id(session, user_id)
        if not user:
            return False
        await UserDatabase.delete_user(session, user)
        return True

    @staticmethod
    async def login(session: Session, email: str, password: str) -> Optional[User]:
        user = await UserDatabase.get_user_by_email(session, email)
        if not user:
            return None
        if not UserService._verify_password(password, user.password):
            return None
        return user
