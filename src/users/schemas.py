import uuid
from typing import Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    email: Optional[str] = Field(None)
    fio: Optional[str] = Field(None)
    is_active: bool = Field(True)
    is_verified: bool = Field(False)
    is_superuser: bool = Field(False)


class UserCreate(UserBase):
    email: str
    fio: str
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class User(UserBase):
    id: uuid.UUID
    email: str
    fio: str
    is_active: bool
    is_verified: bool
    is_superuser: bool

    class Config:
        from_attributes = True


class UserCreateDB(UserBase):
    hashed_password: str


class UserUpdateDB(UserBase):
    hashed_password: str


class RefreshSessionCreate(BaseModel):
    refresh_token: uuid.UUID
    expires_in: int
    user_id: uuid.UUID


class RefreshSessionUpdate(BaseModel):
    refresh_token: uuid.UUID
    expires_in: int
    user_id: uuid.UUID


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
