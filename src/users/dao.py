from ..dao import BaseDAO
from .models import UserModel, RefreshSessionModel
from .schemas import UserCreateDB, UserUpdateDB, RefreshSessionCreate, RefreshSessionUpdate


class UserDAO(BaseDAO[UserModel, UserCreateDB, UserUpdateDB]):
    model = UserModel


class RefreshSessionDAO(BaseDAO[RefreshSessionModel, RefreshSessionCreate, RefreshSessionUpdate]):  # TODO доделать схемы
    model = RefreshSessionModel
