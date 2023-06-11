import uuid
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from ..database import Base


class User(Base):
    __tablename__ = "user"

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = sa.Column(sa.String, unique=True, index=True)
    hashed_password = sa.Column(sa.String)
    fio = sa.Column(sa.String)
    is_active = sa.Column(sa.Boolean, default=True)
    is_superuser = sa.Column(sa.Boolean, default=False)


class RefreshSession(Base):
    __tablename__ = "refresh_session"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    user_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("user.id", ondelete="CASCADE"))
    refresh_token = sa.Column(UUID(as_uuid=True), unique=True)
    expires_in = sa.Column(sa.Integer)
    created_at: datetime = sa.Column(sa.DateTime(timezone=True), server_default=func.now())
