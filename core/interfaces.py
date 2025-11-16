from abc import ABC, abstractmethod
from schemas.user import UserCreate, UserUpdate
from models.user import User
from uuid import UUID


class UserInterface(ABC):
    @abstractmethod
    async def create_user(self, user_data: UserCreate) -> User: ...

    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> User: ...

    @abstractmethod
    async def update_user(self, user_id: UUID, user_data: UserUpdate) -> User: ...

    @abstractmethod
    async def delete_user(self, user_id: UUID) -> bool: ...
