import uuid

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from ..database import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    id: uuid.UUID = sa.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: str = sa.Column(sa.String(length=320), unique=True,
                           index=True, nullable=False)
    hashed_password: str = sa.Column(sa.String(length=1024), nullable=False)
    is_active: bool = sa.Column(sa.Boolean, default=True, nullable=False)
    is_superuser: bool = sa.Column(sa.Boolean, default=False, nullable=False)
    is_verified: bool = sa.Column(sa.Boolean, default=False, nullable=False)
