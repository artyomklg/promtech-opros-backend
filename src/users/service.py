import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import HTTPException, status
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from .utils import get_password_hash, is_valid_password
from .schemas import RefreshSessionUpdate, UserCreate, User, Token, UserCreateDB, RefreshSessionCreate, UserUpdateDB
from .models import UserModel, RefreshSessionModel
from .dao import UserDAO, RefreshSessionDAO
from ..exceptions import InvalidTokenException, TokenExpiredException
from ..config import settings


class AuthService:
    @classmethod
    async def create_token(cls, user_id: uuid.UUID) -> Token:
        access_token = cls._create_access_token(user_id)
        refresh_token_expires = timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        refresh_token = cls._create_refresh_token()

        await RefreshSessionDAO.add(
            RefreshSessionCreate(
                user_id=user_id,
                refresh_token=refresh_token,
                expires_in=refresh_token_expires.total_seconds()
            )
        )
        return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

    @classmethod
    async def logout(cls, token: uuid.UUID) -> None:
        refresh_session = await RefreshSessionDAO.find_one_or_none(RefreshSessionModel.refresh_token == token)
        if refresh_session:
            await RefreshSessionDAO.delete(id=refresh_session.id)

    @classmethod
    async def refresh_token(cls, token: uuid.UUID) -> Token:
        refresh_session = await RefreshSessionDAO.find_one_or_none(RefreshSessionModel.refresh_token == token)

        if refresh_session is None:
            raise InvalidTokenException
        if datetime.now(timezone.utc) >= refresh_session.created_at + timedelta(seconds=refresh_session.expires_in):
            await RefreshSessionDAO.delete(id=refresh_session.id)
            raise TokenExpiredException

        user = await UserDAO.find_one_or_none(id=refresh_session.user_id)
        if user is None:
            raise InvalidTokenException

        access_token = cls._create_access_token(user.id)
        refresh_token_expires = timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        refresh_token = cls._create_refresh_token()

        await RefreshSessionDAO.update(
            RefreshSessionModel.id == refresh_session.id,
            obj_in=RefreshSessionUpdate(
                refresh_token=refresh_token,
                expires_in=refresh_token_expires.total_seconds()
            )
        )
        return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

    @classmethod
    async def authenticate_user(cls, email: str, password: str) -> Optional[UserModel]:
        db_user = await UserDAO.find_one_or_none(email=email)
        if db_user and is_valid_password(password, db_user.hashed_password):
            return db_user
        return None

    @classmethod
    async def abort_all_sessions(cls, user_id: uuid.UUID):
        await RefreshSessionDAO.delete(RefreshSessionModel.user_id == user_id)

    @classmethod
    def _create_access_token(cls, user_id: uuid.UUID) -> str:
        to_encode = {
            "sub": str(user_id),
            "exp": datetime.utcnow() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return f'Bearer {encoded_jwt}'

    @classmethod
    def _create_refresh_token(cls) -> str:
        return uuid.uuid4()


class UserService:
    @classmethod
    async def register_new_user(cls, user: UserCreate) -> UserModel:
        user_exist = await UserDAO.find_one_or_none(email=user.email)
        if user_exist:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User already exists")

        user.is_superuser = False
        user.is_verified = False
        db_user = await UserDAO.add(UserCreateDB(
            **user.model_dump(),
            hashed_password=get_password_hash(user.password)))
        print(db_user.__dict__)

        return db_user

    @classmethod
    async def update_user(cls, user_id: str, user: User, session: AsyncSession) -> User:
        res = await session.execute(select(UserModel).filter(UserModel.id == user_id))
        db_user = res.scalars().first()
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        db_user.email = user.email
        db_user.fio = user.fio
        await session.commit()
        return User(id=str(db_user.id), email=db_user.email, fio=db_user.fio, is_active=db_user.is_active, is_superuser=db_user.is_superuser)

    @classmethod
    async def get_user(cls, user_id: uuid.UUID) -> UserModel:
        db_user = await UserDAO.find_one_or_none(id=user_id)
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return db_user

    @classmethod
    async def delete_user(cls, user_id: uuid.UUID):
        db_user = await UserDAO.find_one_or_none(id=user_id)
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        await UserDAO.update(
            UserModel.id == user_id,
            {'is_active': False}
        )

    @classmethod
    async def update_user_from_superuser(cls, user_id: str, user: User, session: AsyncSession) -> User:
        res = await session.execute(select(UserModel).filter(UserModel.id == user_id))
        db_user = res.scalars().first()
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        db_user.email = user.email
        db_user.fio = user.fio
        db_user.is_superuser = user.is_superuser
        await session.commit()
        return User(id=str(db_user.id), email=db_user.email, fio=db_user.fio, is_active=db_user.is_active, is_superuser=db_user.is_superuser)

    @classmethod
    async def get_users_list(cls, *filter, offset: int = 0, limit: int = 100, **filter_by) -> list[UserModel]:
        users = await UserDAO.find_all(*filter, offset=offset, limit=limit, **filter_by)
        if users is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")
        return users
        return [
            User(
                id=str(db_user.id),
                email=db_user.email,
                fio=db_user.fio,
                is_active=db_user.is_active,
                is_superuser=db_user.is_superuser
            ) for db_user in users
        ]
