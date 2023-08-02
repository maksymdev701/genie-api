from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    MONGO_INITDB_DATABASE: str

    CLIENT_ORIGIN: str

    OPENAI_API_KEY: str

    class Config:
        env_file = "./.env"


settings = Settings()
