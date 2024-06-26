# e.g. global env vars

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseSettings(BaseSettings):
    enable_sqlite: Optional[bool] = False

    if enable_sqlite == False:
        hostname: Optional[str] = "localhost"
        username: Optional[str] = "postgres"
        password: Optional[str] = None
        database: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", env_prefix="db_", extra="allow")

database_settings = DatabaseSettings()
