import time

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routers import main_router

app = FastAPI(title=settings.app_name)

origins = [
    'http://127.0.0.1:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

app.include_router(main_router)


@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    end_time = time.time()
    execution_time = end_time - start_time

    print(f"Метод: {request.method}, Путь: {request.url.path}, Время выполнения: {execution_time} сек.")

    return response

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <a href="http://127.0.0.1:8000/docs">Documentation</a><br>
    <a href="http://127.0.0.1:8000/redoc">ReDoc</a>
    """


# @app.get("/auth", response_class=HTMLResponse)
# def google():
#     return """
#     <a href="https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=641924324482-bqvba9e5jf6j1qlk2ho8mrab107flt49.apps.googleusercontent.com&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fapi%2Fauth%2Fgoogle%2Fcallback&state=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJmYXN0YXBpLXVzZXJzOm9hdXRoLXN0YXRlIiwiZXhwIjoxNjc2MTI5Nzg5fQ.FQznyPtc6n4xg7zUYbOmXv3l2dYNs44lAjNYWW8XQY0&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email">GoogleOAuth</a><br>
#     """
