from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .models import OptionModel, ItemModel, FormModel
from .schemas import (
    OptionCreate, OptionUpdate,
    ItemCreate, ItemUpdate,
    FormCreate, FormUpdate
)
from ..dao import BaseDAO


class OptionDAO(BaseDAO[OptionModel, OptionCreate, OptionUpdate]):
    model = OptionModel


class ItemDAO(BaseDAO[ItemModel, ItemCreate, ItemUpdate]):
    model = ItemModel


class FormDAO(BaseDAO[FormModel, FormCreate, FormUpdate]):
    model = FormModel

    @classmethod
    async def find_form(cls, session: AsyncSession, id: int) -> Optional[FormModel]:
        stmt = select(FormModel).options(selectinload(
            FormModel.items).subqueryload(ItemModel.options)).filter(FormModel.id == id)

        res = await session.execute(stmt)
        return res.scalars().one_or_none()
