from typing import Optional
from pydantic import BaseModel, EmailStr

from custom_types.enums import UserType

from models import User


class UserUpdateRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    type: Optional[UserType] = None


class UserGetResponse(BaseModel):
    user: User


class UserUpdateResponse(BaseModel):
    user: User
