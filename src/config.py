# e.g. global env vars

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_user: str
    db_pass: str

settings = Settings()
