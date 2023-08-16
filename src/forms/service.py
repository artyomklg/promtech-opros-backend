import uuid
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import async_session_maker
from .dao import FormDAO, ItemDAO, OptionDAO
from .models import FormModel, ItemModel, OptionModel
from .schemas import (
    CreateItemRequest,
    CreateOptionRequest,
    DeleteItemRequest,
    DeleteOptionRequest,
    FormCreate,
    FormUpdate,
    ItemCreate,
    ItemDelete,
    ItemMove,
    ItemUpdateRequest,
    MoveItemRequest,
    OptionCreate,
    OptionUpdateRequest,
    UpdateFormRequest,
    UpdateItemRequest,
    UpdateOptionRequest,
    UpdateSchema,
)


class FormService:
    @classmethod
    async def create_form(cls, user_id: uuid.UUID) -> FormModel:
        async with async_session_maker() as session:
            new_form = await FormDAO.add(session, FormCreate(creator_id=user_id))

            form = await FormDAO.update(
                session,
                FormModel.id == new_form.id,
                obj_in=FormUpdate(link=f"http://127.0.0.1:3000/forms/{new_form.id}"),
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
                    "title": original_form.title,
                    "description": original_form.description,
                    "is_template": False,
                    "organization": original_form.organization,
                    "color": original_form.color,
                    "to_review": False,
                    "creator_id": creator_id,
                },
            )
            new_form = await FormDAO.update(
                session,
                FormModel.id == form.id,
                obj_in={"link": f"http://127.0.0.1:3000/forms/{form.id}"},
            )

            for original_item in original_form.items:
                new_item = await ItemDAO.add(
                    session,
                    obj_in={
                        "title": original_item.title,
                        "description": original_item.description,
                        "item_type": original_item.item_type,
                        "item_order": original_item.item_order,
                        "required": original_item.required,
                        "form_id": new_form.id,
                    },
                )
                for original_option in original_item.options:
                    new_option = await OptionDAO.add(
                        session,
                        obj_in={"title": original_option.title, "item_id": new_item.id},
                    )
                    new_item.options.append(new_option)
                new_form.items.append(new_item)

            await session.commit()
        return new_form

    @classmethod
    async def get_form(
        cls, id: int, without_items: bool = False
    ) -> Optional[FormModel]:
        async with async_session_maker() as session:
            if without_items:
                form = await FormDAO.find_one_or_none(session, FormModel.id == id)
            else:
                form = await FormDAO.find_form(session, id)
        if not form:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Form with {id=} not found",
            )
        return form

    @classmethod
    async def get_list_forms(
        cls,
        is_template: bool,
        my: bool,
        creator_id: uuid.UUID,
        offset: int = 0,
        limit: int = 100,
    ) -> List[FormModel]:
        async with async_session_maker() as session:
            filter_by = {}
            if is_template:
                filter_by.update({"is_template": True})
            if my:
                filter_by.update({"creator_id": creator_id})

            forms = await FormDAO.find_all(
                session, offset=offset, limit=limit, **filter_by
            )
        return forms

    @classmethod
    async def form_to_review(cls, id: int) -> FormModel:
        async with async_session_maker() as session:
            form = await FormDAO.update(
                session, FormModel.id == id, obj_in={"to_review": True}
            )
            await session.commit()
            # ! надо попробовать найти решение этой проблемы (returning в update не возвращает relationship-ы)
            form = await FormDAO.find_form(session, id)

        return form

    @classmethod
    async def update_form_by_schema(
        cls, update_schema: UpdateSchema, form_id: int
    ) -> Optional[FormModel]:
        async with async_session_maker() as session:
            for request in update_schema.requests:
                # print(type(request))
                # print(request)
                # print()
                if isinstance(request, UpdateFormRequest):
                    await cls._update_form(session, request.updateForm, form_id)
                elif isinstance(request, CreateItemRequest):
                    await cls._create_item(session, request.createItem)
                elif isinstance(request, MoveItemRequest):
                    await cls._move_item(session, request.moveItem, form_id)
                elif isinstance(request, DeleteItemRequest):
                    await cls._delete_item(session, request.deleteItem)
                elif isinstance(request, UpdateItemRequest):
                    await cls._update_item(session, request.updateItem)
                elif isinstance(request, CreateOptionRequest):
                    await cls._create_option(session, request.createOption)
                elif isinstance(request, DeleteOptionRequest):
                    await cls._delete_option(session, request.deleteOption)
                elif isinstance(request, UpdateOptionRequest):
                    await cls._update_option(session, request.updateOption)

            await session.commit()

            if update_schema.includeFormInResponse:
                form_out = await FormDAO.find_form(session, form_id)
                return form_out
            else:
                return None

    @classmethod
    async def _update_form(
        cls, session: AsyncSession, schema: FormUpdate, form_id: int
    ) -> None:
        await FormDAO.update(session, FormModel.id == form_id, obj_in=schema)

    @classmethod
    async def _create_item(cls, session: AsyncSession, schema: ItemCreate) -> None:
        items = await ItemDAO.find_all(
            session,
            ItemModel.form_id == schema.form_id,
            ItemModel.item_order >= schema.item_order,
        )
        update_list = [
            {"id": item.id, "item_order": item.item_order + 1} for item in items
        ]
        if update_list != []:
            await ItemDAO.update_bulk(session, update_list)

        await ItemDAO.add(session, obj_in=schema)

    @classmethod
    async def _move_item(
        cls, session: AsyncSession, schema: ItemMove, form_id: int
    ) -> None:
        original_item = await ItemDAO.find_one_or_none(
            session, item_order=schema.original_location, form_id=form_id
        )
        if not original_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"item with location={schema.original_location} in form with id={form_id} not found",
            )
        if schema.new_location < schema.original_location:
            items = await ItemDAO.find_all(
                session,
                ItemModel.item_order >= schema.new_location,
                ItemModel.item_order < schema.original_location,
                form_id=form_id,
            )
            update_list = [
                {"id": item.id, "item_order": item.item_order + 1} for item in items
            ]
        elif schema.new_location > schema.original_location:
            items = await ItemDAO.find_all(
                session,
                ItemModel.item_order > schema.original_location,
                ItemModel.item_order <= schema.new_location,
                form_id=form_id,
            )
            update_list = [
                {"id": item.id, "item_order": item.item_order - 1} for item in items
            ]
        update_list.append({"id": original_item.id, "item_order": schema.new_location})
        await ItemDAO.update_bulk(session, update_list)

    @classmethod
    async def _delete_item(cls, session: AsyncSession, schema: ItemDelete) -> None:
        current_item = await ItemDAO.find_one_or_none(
            session, id=schema.id, item_order=schema.location
        )
        if not current_item:
            HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wrong data")

        items = await ItemDAO.find_all(
            session,
            ItemModel.form_id == current_item.form_id,
            ItemModel.item_order > current_item.item_order,
        )
        update_list = [
            {"id": item.id, "item_order": item.item_order - 1} for item in items
        ]
        if update_list != []:
            await ItemDAO.update_bulk(session, update_list)

        await ItemDAO.delete(session, ItemModel.id == schema.id)

    @classmethod
    async def _update_item(
        cls, session: AsyncSession, schema: ItemUpdateRequest
    ) -> None:
        await ItemDAO.update(
            session, ItemModel.id == schema.item_id, obj_in=schema.item
        )

    @classmethod
    async def _create_option(cls, session: AsyncSession, schema: OptionCreate) -> None:
        await OptionDAO.add(session, obj_in=schema)

    @classmethod
    async def _delete_option(cls, session: AsyncSession, schema: int) -> None:
        await OptionDAO.delete(session, OptionModel.id == schema)

    @classmethod
    async def _update_option(
        cls, session: AsyncSession, schema: OptionUpdateRequest
    ) -> None:
        await OptionDAO.update(
            session, OptionModel.id == schema.option_id, obj_in=schema.option
        )
