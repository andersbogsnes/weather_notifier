from pydantic import BaseSettings, SecretStr, Field


class DBAuth(BaseSettings):
    db_url: SecretStr

    class Config:
        env_file = ".env"


class APIAuth(BaseSettings):
    api_key: SecretStr

    class Config:
        env_file = ".env"


class Settings(BaseSettings):
    db: DBAuth = Field(default_factory=DBAuth)
    api: APIAuth = Field(default_factory=APIAuth)


async def get_settings() -> Settings:
    return Settings()
