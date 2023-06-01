import uuid

from fastapi import Depends
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.db import SQLAlchemyUserDatabase

from .models import User
from .utils import get_user_db
from ..config import settings


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.SECRET
    verification_token_secret = settings.SECRET


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)
