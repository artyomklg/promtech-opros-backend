from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    fio: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: str
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
