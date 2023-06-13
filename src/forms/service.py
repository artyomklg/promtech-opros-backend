import uuid

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload

from . import models as m
from . import schemas as sch


async def get_form(session: AsyncSession, id: int) -> m.Form:
    stmt = select(m.Form).options(joinedload(
        m.Form.items).subqueryload(m.Item.options)).filter(m.Form.id == id)
    res = await session.execute(stmt)
    form = res.scalars().first()
    if not form:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Form with {id=} not found')
    return form


async def get_list_forms(templates: bool, my: bool, creator_id: uuid.UUID, session: AsyncSession) -> list[m.Form]:
    stmt = select(m.Form)
    if templates:
        stmt = stmt.filter(m.Form.is_template == True)
    if my:
        stmt = stmt.filter(m.Form.creator_id == creator_id)
    res = await session.execute(stmt)
    templates = res.scalars().all()
    if not templates:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'There are not templates')
    return templates


async def create_form(session: AsyncSession, creator_id: uuid.UUID) -> m.Form:
    form_db = m.Form(
        title='',
        description='',
        is_template=False,
        organization='okb.jpg',
        color='#F48221',
        creator_id=creator_id
    )
    session.add(form_db)
    await session.commit()
    await session.refresh(form_db)
    form_db.link = f'http://127.0.0.1:3000/forms/{form_db.id}/review'
    session.add(form_db)
    await session.commit()
    await session.refresh(form_db)
    return form_db


async def copy_form(session: AsyncSession, form: sch.Form, creator_id: uuid.UUID) -> m.Form:
    new_form = m.Form(
        title=form.title,
        description=form.description,
        is_template=False,
        organization=form.organization,
        color=form.color,
        creator_id=creator_id
    )
    print(new_form.__dict__)
    session.add(new_form)
    await session.commit()
    print('added')

    for item in form.items:
        new_item = m.Item(
            title=item.title,
            description=item.description,
            item_type=item.item_type,
            item_order=item.item_order,
            required=item.required,
            form_id=new_form.id
        )
    await session.refresh(new_form)

    print(new_form.__dict__)
    return new_form


async def update_form(session: AsyncSession, form: sch.Form, form_id: int):
    existing_form = await get_form(session, form_id)

    existing_form.title = form.title
    existing_form.description = form.description
    existing_form.is_template = form.is_template
    existing_form.organization = form.organization
    existing_form.color = form.color
    existing_form.link = form.link

    existing_item_ids = {item.id for item in existing_form.items}
    updated_item_ids = {item.id for item in form.items}

    deleted_item_ids = existing_item_ids - updated_item_ids
    if deleted_item_ids:
        await session.execute(delete(m.Item).where(m.Item.id.in_(deleted_item_ids)))

    for item in form.items:
        existing_item = next(
            (i for i in existing_form.items if i.id == item.id), None)
        if existing_item:
            existing_item.title = item.title
            existing_item.item_type = item.item_type
            existing_item.item_order = item.item_order
            existing_item.required = item.required
        else:
            new_item = m.Item(
                title=item.title,
                item_type=item.item_type,
                item_order=item.item_order,
                required=item.required,
                form_id=form_id,
                options=[]
            )
            existing_form.items.append(new_item)
            await session.commit()
            item.id = new_item.id
            existing_item = new_item
            print('add new item', new_item.__dict__)

        if existing_item:
            existing_option_ids = {
                option.id for option in existing_item.options}
        else:
            existing_option_ids = set()
        updated_option_ids = {option.id for option in item.options}

        deleted_option_ids = existing_option_ids - updated_option_ids
        if deleted_option_ids:
            await session.execute(delete(m.Option).where(m.Option.id.in_(deleted_option_ids)))

        for option in item.options:
            existing_option = next((o for o in existing_item.options if (
                o.id == option.id and option.id is not None)), None)

            if existing_option:
                existing_option.title = option.title
            else:
                new_option = m.Option(
                    title=option.title
                )
                if existing_item:
                    existing_item.options.append(new_option)
                    print('add new option', new_option.__dict__)

    try:
        await session.commit()
        return existing_form
    except Exception as e:
        await session.rollback()
        return
