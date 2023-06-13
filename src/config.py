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
    ALGORITM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 20
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    # GOOGLE_OAUTH_CLIENT_ID: str
    # GOOGLE_OAUTH_CLIENT_SECRET: str

    # origins
    CLIENT_ORIGIN: str

    @property
    def Database_URL(self):
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'

    @property
    def Database_URL_psycopg2(self):
        return f'postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'

    class Config:
        env_file = env_path


settings: Settings = Settings()
