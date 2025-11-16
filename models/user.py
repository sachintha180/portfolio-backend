from uuid import UUID, uuid4
from sqlmodel import Field
from pydantic import EmailStr

from models.base import TimestampedModel
from custom_types.enums import UserType


class User(TimestampedModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    first_name: str = Field(nullable=False, max_length=100)
    last_name: str = Field(nullable=False, max_length=100)
    email: EmailStr = Field(unique=True, index=True)
    password: str = Field(nullable=False)
    type: UserType = Field(nullable=False, index=True)
