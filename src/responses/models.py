import uuid

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..database import Base
from ..forms import models as form_m
from ..auth import models as user_m


class Response(Base):
    id: int = sa.Column(sa.Integer, primary_key=True, nullable=False)
    form_id: int = sa.Column(
        sa.Integer, sa.ForeignKey('form.id'), nullable=False)
    user_id: uuid.UUID = sa.Column(
        UUID(as_uuid=True), sa.ForeignKey('user.id'))

    user = relationship('user_m.User',
                        uselist=False)
    answers = relationship('Answer', uselist=True, back_populates='response')


class Answer(Base):
    id: int = sa.Column(sa.Integer, primary_key=True, nullable=False)
    item_id: int = sa.Column(sa.Integer, sa.ForeignKey('item.id'))

    response = relationship('Response', uselist=False, back_populates='answers')
