from pydantic import BaseSettings, AnyHttpUrl, SecretStr


class Settings(BaseSettings):
    subscription_api_url: AnyHttpUrl
    api_key: SecretStr
    smtp_host: str

    class Config:
        env_file = ".env"
