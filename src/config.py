import pathlib

from pydantic import BaseSettings

env_path = f'{pathlib.Path(__file__).parent.parent.absolute()}\\.env'


class Settings(BaseSettings):
    app_name: str = 'local_forms'
    # postgres
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    # auth
    SECRET: str
    GOOGLE_OAUTH_CLIENT_ID: str
    GOOGLE_OAUTH_CLIENT_SECRET: str

    # origins
    CLIENT_ORIGIN: str

    class Config:
        env_file = env_path


settings: Settings = Settings()