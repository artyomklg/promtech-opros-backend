import uuid
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from ..database import Base
from ..forms import models as form_m
from ..auth import models as user_m


class Review(Base):
    id: int = sa.Column(sa.Integer, primary_key=True, nullable=False)
    form_id: int = sa.Column(
        sa.Integer, sa.ForeignKey('form.id', ondelete="CASCADE"), nullable=False)
    user_id: uuid.UUID = sa.Column(
        UUID(as_uuid=True), sa.ForeignKey('user.id', ondelete="CASCADE"))
    response_time: datetime = sa.Column(
        sa.DateTime(timezone=True), server_default=func.now())

    user = relationship('user_m.User',
                        uselist=False)
    answers = relationship('Answer', uselist=True, back_populates='review')


class Answer(Base):
    id: int = sa.Column(sa.Integer, primary_key=True, nullable=False)
    item_id: int = sa.Column(
        sa.Integer, sa.ForeignKey('item.id', ondelete="CASCADE"))
    response_id: int = sa.Column(
        sa.Integer, sa.ForeignKey('review.id', ondelete="CASCADE"))
    promt: dict = sa.Column(JSONB)

    item = relationship('form_m.Item', uselist=False)
    review = relationship('Review', uselist=False,
                          back_populates='answers')
