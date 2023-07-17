from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status

from .service import FormService
from ..users.schemas import User
from ..users.dependencies import get_current_superuser
from ..users.models import UserModel
from .schemas import Form, FormUpdate, FormWithoutItems, UpdateSchema

forms_router: APIRouter = APIRouter(prefix='/forms', tags=["forms"])


@forms_router.post('/') # ! ready
async def create_form(
    id: int | None = None,
    user: UserModel = Depends(get_current_superuser),
) -> Form:
    if id:
        form_out = await FormService.copy_form(id, user.id)
        return form_out
    else:
        form_out = await FormService.create_form(user.id)
        return form_out


@forms_router.get('/') # ! ready
async def get_list_forms(
    templates: bool,
    my: bool,
    offset: Optional[str] = 0,
    limit: Optional[str] = 100,
    user: UserModel = Depends(get_current_superuser)
) -> List[FormWithoutItems]:
    forms = await FormService.get_list_forms(templates, my, user.id, offset=offset, limit=limit)
    return forms


@forms_router.post('/{id}')
async def form_to_review(
    id: int,
    user: UserModel = Depends(get_current_superuser)
) -> Form:
    form = await FormService.get_form(id)
    if form.creator_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    form_out = await FormService.form_to_review(id)
    return form_out


@forms_router.get('/{id}') # ! ready
async def get_form(
    id: int,
    user: UserModel = Depends(get_current_superuser)
) -> Form:
    return await FormService.get_form(id)



@forms_router.put('/{id}')
async def update_form(
    id: int,
    form: FormUpdate,
    user: User = Depends(get_current_superuser)
) -> Form:
    if user.id != form.creator_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    res = await service.update_form(session, form, id)
    return res
