from typing import Optional
from pydantic import BaseModel, EmailStr

from custom_types.enums import UserType


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    type: Optional[UserType] = None
