import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqladmin import Admin

from .admin.auth import authentication_backend
from .admin.views import (
    AnswerAdmin,
    FormAdmin,
    ItemAdmin,
    OptionAdmin,
    RefreshSessionAdmin,
    ReviewAdmin,
    UserAdmin,
)
from .config import settings
from .database import engine
from .routers import main_router

app = FastAPI(title=settings.app_name)

origins = ["http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

app.include_router(main_router)


admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(RefreshSessionAdmin)
admin.add_view(FormAdmin)
admin.add_view(ItemAdmin)
admin.add_view(OptionAdmin)
admin.add_view(ReviewAdmin)
admin.add_view(AnswerAdmin)


@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    end_time = time.time()
    execution_time = end_time - start_time

    print(
        f"Метод: {request.method}, Путь: {request.url.path}, Время выполнения: {execution_time} сек."
    )

    return response


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <a href="http://127.0.0.1:8000/docs">Documentation</a><br>
    <a href="http://127.0.0.1:8000/redoc">ReDoc</a>
    """
