from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080
    DATABASE_URL: str = "sqlite:///./data/saathi.db"
    ANTHROPIC_API_KEY: str = ""
    BACKEND_URL: str = "http://localhost:8000"
    GROQ_API_key: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
