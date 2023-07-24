import uuid
from datetime import datetime
from typing import Any, Optional

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ...database import Base


class ReviewModel(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    form_id: Mapped[int] = mapped_column(sa.ForeignKey(
        'form.id', ondelete='CASCADE'), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, sa.ForeignKey(
        'user.id', ondelete='SET NULL'), nullable=False)
    review_time: Mapped[Optional[datetime]] = mapped_column(
        sa.TIMESTAMP(timezone=True))
    is_ready: Mapped[bool] = mapped_column(default=False)

    answers: Mapped['AnswerModel'] = relationship(
        uselist=True, back_populates='review')


class AnswerModel(Base):
    __tablename__ = 'answer'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    item_id: Mapped[int] = mapped_column(
        sa.ForeignKey('item.id', ondelete='CASCADE'))
    review_id: Mapped[int] = mapped_column(
        sa.ForeignKey('review.id', ondelete='CASCADE'))
    promt: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON)

    review: Mapped[ReviewModel] = relationship(
        uselist=False, back_populates='answers')
