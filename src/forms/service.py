import uuid

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
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
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Form with {id=} not found')
    return form


async def create_form(session: AsyncSession, form: sch.FormCreate, creator_id: uuid.UUID) -> m.Form:
    form_data = jsonable_encoder(form)
    form_data.update({'creator_id': creator_id})
    form_db = m.Form(**form_data)
    session.add(form_db)
    await session.commit()
    await session.refresh(form_db)
    return form_db


async def copy_form(session: AsyncSession, form: sch.Form, creator_id: uuid.UUID) -> m.Form:
    new_form = m.Form(
        title=form.title,
        description=form.description,
        is_template=False,
        organiztion=form.organiztion,
        color=form.color,
        creator_id=creator_id
    )
    print(new_form.__dict__)
    session.add(new_form)
    print('added')
    await session.refresh(new_form)

    print(new_form.__dict__)
    return new_form
