from typing import List, Optional
from datetime import datetime
import uuid

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from ..database import Base


class OptionModel(Base):
    __tablename__ = 'option'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[Optional[str]]
    item_id: Mapped[int] = mapped_column(sa.ForeignKey(
        'item.id', ondelete='CASCADE'), nullable=False)

    item: Mapped['ItemModel'] = relationship(uselist=False, back_populates='options')


class ItemModel(Base):
    __tablename__ = 'item'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[Optional[str]]
    description: Mapped[Optional[str]]
    item_type: Mapped[str]
    item_order: Mapped[int]
    required: Mapped[bool] = mapped_column(default=True)
    form_id: Mapped[int] = mapped_column(sa.ForeignKey(
        'form.id', ondelete='CASCADE'), nullable=False)

    form: Mapped['FormModel'] = relationship(uselist=False, back_populates='items')
    options: Mapped[List[OptionModel]] = relationship(uselist=True, back_populates='item')


class FormModel(Base):
    __tablename__ = 'form'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[Optional[str]]
    description: Mapped[Optional[str]]
    is_template: Mapped[bool] = mapped_column(default=False)
    organization: Mapped[str] = mapped_column(default='okb.jpg')
    color: Mapped[str] = mapped_column(default='red')
    to_review: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(sa.TIMESTAMP(timezone=True),
                                                 server_default=func.now())
    link: Mapped[Optional[str]]
    creator_id: Mapped[uuid.UUID] = mapped_column(UUID, sa.ForeignKey(
        'user.id', ondelete='SET NULL'), nullable=False)

    items: Mapped[List[ItemModel]] = relationship(uselist=True, back_populates='form')


# class Question(Base):
#     id: int = sa.Column(sa.Integer, primary_key=True, nullable=False)
#     required: bool = sa.Column(sa.Boolean)
#     question_type: str = sa.Column(sa.String)
#     prompt: dict = sa.Column(JSONB)
#     item_id = sa.Column(sa.Integer, sa.ForeignKey('item.id'), nullable=False)

#     item = relationship('Item', lazy='joined',
#                         uselist=False, back_populates='question')
