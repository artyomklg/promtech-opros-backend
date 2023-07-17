from typing import List, Optional
import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .models import OptionModel, ItemModel, FormModel
from .dao import OptionDAO, ItemDAO, FormDAO
from .schemas import (FormCreate, FormUpdate, ItemCreate,
                      ItemMove, ItemUpdateRequest, OptionCreate, OptionUpdateRequest, UpdateSchema)
from ..database import async_session_maker


class FormService:
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
    async def get_form(cls, id: int, without_items: bool = False) -> Optional[FormModel]:
        async with async_session_maker() as session:
            if without_items:
                form = await FormDAO.find_one_or_none(session, FormModel.id == id)
            else:
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
            await session.commit()
            # ! надо попробовать найти решение этой проблемы (returning в update не возвращает relationship-ы)
            form = await FormDAO.find_form(session, id)

        return form

    @classmethod
    async def update_form_by_schema(cls, update_schemas: List[UpdateSchema], form_id: int, includeFormInResponse: bool) -> Optional[FormModel]:
        async with async_session_maker() as session:
            for update_schema in update_schemas:
                match update_schema.type:
                    case 'updateForm':
                        pass
                    case 'createItem':
                        pass
                    case 'moveItem':
                        pass
                    case 'deleteItem':
                        pass
                    case 'updateItem':
                        pass
                    case 'createOption':
                        pass
                    case 'deleteOption':
                        pass
                    case 'updateOption':
                        pass
            await session.commit()

            if includeFormInResponse:
                form_out = await FormDAO.find_form(session, form_id)
                return form_out
            else:
                return None

    @classmethod
    async def _update_form(cls, session: AsyncSession, schema: FormUpdate, form_id: int):
        await FormDAO.update(session, FormModel.id == id, obj_in=schema)

    @classmethod
    async def _create_item(cls, session: AsyncSession, schema: ItemCreate):
        # !Добавить сдвиг элементов, если элемент создан не в самомм низу
        await ItemDAO.add(session, obj_in=ItemCreate)

    @classmethod
    async def _move_item(cls, session: AsyncSession, schema: ItemMove, form_id: int):
        # !Написать логику и скопипастить вниз и вверх
        ...

    @classmethod
    async def _delete_item(cls, session: AsyncSession, schema: int):
        # !Добавить сдвиг остальных элементов
        await ItemDAO.delete(session, ItemModel.id == schema)

    @classmethod
    async def _update_item(cls, session: AsyncSession, schema: ItemUpdateRequest):
        await ItemDAO.update(session, ItemModel.id == schema.item_id, obj_in=schema.item)

    @classmethod
    async def _create_option(cls, session: AsyncSession, schema: OptionCreate):
        await OptionDAO.add(session, obj_in=schema)

    @classmethod
    async def _delete_option(cls, session: AsyncSession, schema: int):
        await OptionDAO.delete(session, OptionModel.id == schema)

    @classmethod
    async def _update_option(cls, session: AsyncSession, schema: OptionUpdateRequest):
        await OptionDAO.update(session, OptionModel.id == schema.option_id, obj_in=schema.option)
