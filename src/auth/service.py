import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import HTTPException, status
import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from .schemas import UserCreate, User, Token
from .models import User as UserModel, RefreshSession
from .exceptions import InvalidTokenException, TokenExpiredException
from ..config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    async def create_token(self, user: User, session: AsyncSession) -> Token:
        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self._create_access_token(
            str(user.id), access_token_expires)
        refresh_token_expires = timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        refresh_token = self._create_refresh_token()
        refresh_session = RefreshSession(user_id=user.id,
                                         refresh_token=refresh_token,
                                         expires_in=refresh_token_expires.total_seconds())
        session.add(refresh_session)
        await session.commit()
        return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

    async def logout(self, token: str, session: AsyncSession) -> None:
        res = await session.execute(select(RefreshSession).filter(RefreshSession.refresh_token == token))
        refresh_session = res.scalars().first()
        if refresh_session:
            await session.delete(refresh_session)
            await session.commit()

    async def refresh_token(self, token: str, session: AsyncSession) -> Token:
        res = await session.execute(select(RefreshSession).filter(RefreshSession.refresh_token == token))
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
        return await self.create_token(user, session)

    async def authenticate_user(self, email: str, password: str, session: AsyncSession) -> Optional[User]:
        res = await session.execute(select(UserModel).filter(UserModel.email == email))
        db_user = res.scalars().first()
        if db_user and pwd_context.verify(password, db_user.hashed_password):
            return User(id=str(db_user.id), email=db_user.email, fio=db_user.fio, is_active=db_user.is_active, is_superuser=db_user.is_superuser)
        return None

    async def abort_all_sessions(self, user_id: str, session: AsyncSession):
        await session.execute(delete(RefreshSession).filter(RefreshSession.user_id == user_id))
        await session.commit()

    def _create_access_token(self, user_id: str, expires_delta: timedelta) -> str:
        to_encode = {"sub": user_id, "exp": datetime.utcnow() + expires_delta}
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET, algorithm=settings.ALGORITM)
        return f'Bearer {encoded_jwt}'

    def _create_refresh_token(self) -> str:
        return str(uuid.uuid4())


class UserService:
    async def register_new_user(self, user: UserCreate, session: AsyncSession) -> User:
        res = await session.execute(select(UserModel).filter(UserModel.email == user.email))
        db_user = res.scalars().first()
        if db_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

        hashed_password = pwd_context.hash(user.password)
        db_user = UserModel(
            email=user.email, hashed_password=hashed_password, fio=user.fio)
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return User(id=str(db_user.id), email=db_user.email, fio=db_user.fio, is_active=db_user.is_active, is_superuser=db_user.is_superuser)

    async def update_user(self, user_id: str, user: User, session: AsyncSession) -> User:
        res = await session.execute(select(UserModel).filter(UserModel.id == user_id))
        db_user = res.scalars().first()
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        db_user.email = user.email
        db_user.fio = user.fio
        await session.commit()
        return User(id=str(db_user.id), email=db_user.email, fio=db_user.fio, is_active=db_user.is_active, is_superuser=db_user.is_superuser)

    async def get_user(self, user_id: str, session: AsyncSession) -> User:
        res = await session.execute(select(UserModel).filter(UserModel.id == user_id))
        db_user = res.scalars().first()
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return User(id=str(db_user.id), email=db_user.email, fio=db_user.fio, is_active=db_user.is_active, is_superuser=db_user.is_superuser)

    async def delete_user(self, user_id: str, session: AsyncSession):
        res = await session.execute(select(UserModel).filter(UserModel.id == user_id))
        db_user = res.scalars().first()
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        db_user.is_active = False
        await session.commit()

    async def update_user_from_superuser(self, user_id: str, user: User, session: AsyncSession) -> User:
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

    async def get_users_list(self, session: AsyncSession) -> list[User]:
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
