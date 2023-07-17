from typing import List, Optional
import uuid

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload

from .models import OptionModel, ItemModel, FormModel
from .dao import OptionDAO, ItemDAO, FormDAO
from .schemas import FormCreate, FormUpdate, UpdateSchema
from ..database import async_session_maker
from . import schemas as sch


class FormService():
    @classmethod
    async def create_form(cls, user_id: uuid.UUID) -> FormModel:
        async with async_session_maker() as session:
            new_form = await FormDAO.add(session, FormCreate(creator_id=user_id))

            form = await FormDAO.update(
                session,
                FormModel.id == new_form.id,
                obj_in=FormUpdate(
                    link=f'http://127.0.0.1:3000/forms/{new_form.id}')
            )
            await session.commit()
        return form

    @classmethod
    async def copy_form(cls, form_id: int, creator_id: uuid.UUID) -> FormModel:
        async with async_session_maker() as session:
            original_form = await FormDAO.find_form(session, form_id)

            if not original_form:
                raise HTTPException(status_code=404, detail="Form not found")

            form = await FormDAO.add(
                session,
                obj_in={
                    'title': original_form.title,
                    'description': original_form.description,
                    'is_template': False,
                    'organization': original_form.organization,
                    'color': original_form.color,
                    'to_review': False,
                    'creator_id': creator_id
                }
            )
            new_form = await FormDAO.update(
                session,
                FormModel.id == form.id,
                obj_in={'link': f'http://127.0.0.1:3000/forms/{form.id}'}
            )

            for original_item in original_form.items:
                new_item = await ItemDAO.add(
                    session,
                    obj_in={
                        'title': original_item.title,
                        'description': original_item.description,
                        'item_type': original_item.item_type,
                        'item_order': original_item.item_order,
                        'required': original_item.required,
                        'form_id': new_form.id
                    }
                )
                for original_option in original_item.options:
                    new_option = await OptionDAO.add(
                        session,
                        obj_in={
                            'title': original_option.title,
                            'item_id': new_item.id
                        }
                    )
                    new_item.options.append(new_option)
                new_form.items.append(new_item)

            await session.commit()
        return new_form

    @classmethod
    async def get_form(cls, id: int) -> FormModel:
        async with async_session_maker() as session:
            form = await FormDAO.find_form(session, id)
        if not form:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Form with {id=} not found')
        return form

    @classmethod
    async def get_list_forms(cls, is_template: bool, my: bool, creator_id: uuid.UUID, offset: int = 0, limit: int = 100) -> List[FormModel]:
        async with async_session_maker() as session:
            filter_by = {}
            if is_template:
                filter_by.update({'is_template': True})
            if my:
                filter_by.update({'creator_id': creator_id})

            forms = await FormDAO.find_all(session, offset=offset, limit=limit, **filter_by)
        return forms

    @classmethod
    async def form_to_review(cls, id: int) -> FormModel:
        async with async_session_maker() as session:
            form = await FormDAO.update(
                session,
                FormModel.id == id,
                obj_in={
                    'to_review': True
                }
            )

    @classmethod
    async def update_form(cls, update_schema: UpdateSchema, form_id: int):
        pass


# async def get_list_forms(templates: bool, my: bool, creator_id: uuid.UUID, session: AsyncSession) -> list[FormModel]:
#     stmt = select(FormModel)
#     if templates:
#         stmt = stmt.filter(FormModel.is_template == True)
#     if my:
#         stmt = stmt.filter(FormModel.creator_id == creator_id)
#     res = await session.execute(stmt)
#     templates = res.scalars().all()
#     if not templates:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail=f'There are not templates')
#     return templates
