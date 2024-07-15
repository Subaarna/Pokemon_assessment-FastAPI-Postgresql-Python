from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POKEAPI_URL: str = "https://pokeapi.co/api/v2/pokemon?limit=1000"

    class Config:
        env_file = ".env"

settings = Settings()
