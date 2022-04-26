from pydantic import BaseSettings, SecretStr


class DBAuth(BaseSettings):
    db_url: SecretStr

    class Config:
        env_file = ".env"


async def get_settings() -> DBAuth:
    return DBAuth()
