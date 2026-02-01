from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = (
        "postgresql+psycopg://postgres:postgres@localhost:5432/plataforma_logistica"
    )

    jwt_secret: str = "cambia-esto-por-un-secreto-largo-de-al-menos-32-bytes"
    jwt_algorithm: str = "HS256"
    jwt_exp_minutes: int = 60


settings = Settings()
