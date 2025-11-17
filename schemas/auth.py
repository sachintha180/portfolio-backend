from pydantic import BaseModel, EmailStr
from datetime import datetime

from custom_types.enums import UserType


class AuthLogin(BaseModel):
    email: EmailStr
    password: str


class AuthRegister(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    type: UserType


class AuthPayload(BaseModel):
    sub: str
    email: EmailStr
    type: UserType
    exp: datetime


class AuthToken(BaseModel):
    access_token: str
