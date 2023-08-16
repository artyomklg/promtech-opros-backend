from ..dao import BaseDAO
from .models import RefreshSessionModel, UserModel
from .schemas import (
    RefreshSessionCreate,
    RefreshSessionUpdate,
    UserCreateDB,
    UserUpdateDB,
)


class UserDAO(BaseDAO[UserModel, UserCreateDB, UserUpdateDB]):
    model = UserModel


class RefreshSessionDAO(
    BaseDAO[RefreshSessionModel, RefreshSessionCreate, RefreshSessionUpdate]
):
    model = RefreshSessionModel
