from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID
from typing import Optional

from custom_types.enums import UserType

from models import User


class TokenPayload(BaseModel):
    sub: str
    email: EmailStr
    type: UserType
    exp: datetime


class AuthLoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthLoginResponse(BaseModel):
    user: User


class AuthRegisterRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    type: UserType


class AuthRegisterResponse(BaseModel):
    user: User


class AuthVerifyUser(BaseModel):
    id: UUID
    email: EmailStr
    first_name: str
    last_name: str
    type: UserType


class AuthVerifyResponse(BaseModel):
    authenticated: bool
    user: Optional[AuthVerifyUser]
