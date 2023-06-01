from fastapi import APIRouter

resp_router: APIRouter = APIRouter(prefix='/forms', tags=["responses"])


@resp_router.post('/{form_id}/responses/')
async def post_response(
    form_id: int
) -> None:
    return


@resp_router.get('/{form_id}/responses/{resp_id}')
async def get_response(
    form_id: int,
    resp_id: int
) -> None:
    return


@resp_router.get('/{form_id}/responses/')
async def get_responses(
    form_id: int
) -> None:
    return
