from fastapi import APIRouter, Depends, HTTPException, status

from ..database import get_async_session, AsyncSession
from ..auth.models import User
from ..auth.base_config import current_active_user
from . import models as m
from . import schemas as sch
from . import service

forms_router: APIRouter = APIRouter(prefix='/forms', tags=["forms"])


@forms_router.post('/', response_model=sch.Form)
async def create_form(
    id: int | None = None,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
) -> sch.Form:
    if id:
        form_db = await service.get_form(session, id)
        form_sch = sch.Form.from_orm(form_db)
        form_out = await service.copy_form(session, form_sch, user.id)
        return form_out
    else:
        form_out = await service.create_form(session, user.id)
        return sch.FormWithoutItems.from_orm(form_out)


@forms_router.get('/', response_model=list[sch.FormWithoutItems])
async def get_templates(
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session)
) -> list[sch.FormWithoutItems]:
    templates = await service.get_list_templates(session)
    return templates


@forms_router.get('/{id}', response_model=sch.Form)
async def get_form(
    id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
) -> sch.Form:
    res = await service.get_form(session, id)
    if res.creator_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return res


@forms_router.put('/{id}')
async def update_form(
    id: int,
    form: sch.FormUpdate,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
) -> sch.Form:
    if user.id != form.creator_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    res = await service.update_form(session, form, id)
    return res