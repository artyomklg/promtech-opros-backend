from typing import Any
import uuid
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from ...database import Base
# from ...forms import models as form_m
# from ...users import models as user_m


class ReviewModel(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    form_id: Mapped[int] = mapped_column(sa.ForeignKey(
        'form.id', ondelete='CASCADE'), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, sa.ForeignKey(
        'user.id', ondelete='SET NULL'), nullable=False)
    review_time: Mapped[datetime] = mapped_column(sa.TIMESTAMP(timezone=True))

    answers: Mapped['AnswerModel'] = relationship(
        uselist=True, back_populates='review')


class AnswerModel(Base):
    __tablename__ = 'answer'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    item_id: Mapped[int] = mapped_column(
        sa.ForeignKey('item.id', ondelete='CASCADE'))
    review_id: Mapped[int] = mapped_column(
        sa.ForeignKey('review.id', ondelete='CASCADE'))
    promt: Mapped[dict[str, Any]] = mapped_column(JSON)

    review: Mapped[ReviewModel] = relationship(
        uselist=False, back_populates='answers')
