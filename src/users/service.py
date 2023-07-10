import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Response, HTTPException, status
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from .utils import get_password_hash, is_valid_password
from .schemas import UserCreate, User, Token, UserCreateDB
from .models import UserModel, RefreshSessionModel
from .exceptions import InvalidTokenException, TokenExpiredException
from .dao import UserDAO, RefreshSessionDAO
from ..config import settings


class AuthService:
    @classmethod
    async def create_token(cls, response: Response, user: UserModel) -> Token:
        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = cls._create_access_token(
            str(user.id), access_token_expires)
        refresh_token_expires = timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        refresh_token = cls._create_refresh_token()
        response.set_cookie(
            'access_token',
            access_token,
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            secure=True,
            httponly=True,
            samesite='lax',
        )
        response.set_cookie(
            'refresh_token',
            refresh_token,
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 30 * 24 * 60,
            secure=True,
            httponly=True,
            samesite='lax',
        )
        #!   доделать
        refresh_session = RefreshSessionModel(user_id=user.id,
                                              refresh_token=refresh_token,
                                              expires_in=refresh_token_expires.total_seconds())
        session.add(refresh_session)
        await session.commit()
        return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

    @classmethod
    async def logout(cls, token: str, session: AsyncSession) -> None:
        res = await session.execute(select(RefreshSessionModel).filter(RefreshSessionModel.refresh_token == token))
        refresh_session = res.scalars().first()
        if refresh_session:
            await session.delete(refresh_session)
            await session.commit()

    @classmethod
    async def refresh_token(cls, token: str, session: AsyncSession) -> Token:
        res = await session.execute(select(RefreshSessionModel).filter(RefreshSessionModel.refresh_token == token))
        refresh_session = res.scalars().first()
        if refresh_session is None:
            raise InvalidTokenException
        if datetime.now(timezone.utc) >= refresh_session.created_at + timedelta(seconds=refresh_session.expires_in):
            await session.delete(refresh_session)
            await session.commit()
            raise TokenExpiredException

        res = await session.execute(select(UserModel).filter(UserModel.id == refresh_session.user_id))
        user = res.scalars().first()
        if user is None:
            raise InvalidTokenException
        await session.delete(refresh_session)
        await session.commit()
        return await cls.create_token(user, session)

    @classmethod
    async def authenticate_user(cls, email: str, password: str) -> Optional[UserModel]:
        db_user = await UserDAO.find_one_or_none(email=email)
        if db_user and is_valid_password(password, db_user.hashed_password):
            return db_user
        return None

    @classmethod
    async def abort_all_sessions(cls, user_id: str, session: AsyncSession):
        await session.execute(delete(RefreshSessionModel).filter(RefreshSessionModel.user_id == user_id))
        await session.commit()

    @classmethod
    def _create_access_token(cls, user_id: uuid.UUID, expires_delta: timedelta) -> str:
        to_encode = {"sub": user_id, "exp": datetime.utcnow() + expires_delta}
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return f'Bearer {encoded_jwt}'

    @classmethod
    def _create_refresh_token(cls) -> str:
        return str(uuid.uuid4())


class UserService:
    @classmethod
    async def register_new_user(cls, user: UserCreate) -> UserModel:
        user_exist = await UserDAO.find_one_or_none(email=user.email)
        # res = await session.execute(select(UserModel).filter(UserModel.email == user.email))
        # db_user = res.scalars().first()
        print(type(user_exist))
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
    async def get_user(cls, user_id: str, session: AsyncSession) -> User:
        res = await session.execute(select(UserModel).filter(UserModel.id == user_id))
        db_user = res.scalars().first()
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return User(id=str(db_user.id), email=db_user.email, fio=db_user.fio, is_active=db_user.is_active, is_superuser=db_user.is_superuser)

    @classmethod
    async def delete_user(cls, user_id: str, session: AsyncSession):
        res = await session.execute(select(UserModel).filter(UserModel.id == user_id))
        db_user = res.scalars().first()
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        db_user.is_active = False
        await session.commit()

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
    async def get_users_list(cls, session: AsyncSession) -> list[User]:
        res = await session.execute(select(UserModel))
        users = res.scalars().all()
        if users is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")
        return [
            User(
                id=str(db_user.id),
                email=db_user.email,
                fio=db_user.fio,
                is_active=db_user.is_active,
                is_superuser=db_user.is_superuser
            ) for db_user in users
        ]
