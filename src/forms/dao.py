from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..dao import BaseDAO
from .models import FormModel, ItemModel, OptionModel
from .schemas import (
    FormCreate,
    FormUpdate,
    ItemCreate,
    ItemUpdate,
    OptionCreate,
    OptionUpdate,
)


class OptionDAO(BaseDAO[OptionModel, OptionCreate, OptionUpdate]):
    model = OptionModel


class ItemDAO(BaseDAO[ItemModel, ItemCreate, ItemUpdate]):
    model = ItemModel


class FormDAO(BaseDAO[FormModel, FormCreate, FormUpdate]):
    model = FormModel

    @classmethod
    async def find_form(cls, session: AsyncSession, id: int) -> Optional[FormModel]:
        stmt = (
            select(FormModel)
            .options(selectinload(FormModel.items).subqueryload(ItemModel.options))
            .filter(FormModel.id == id)
        )

        res = await session.execute(stmt)
        return res.scalars().one_or_none()
