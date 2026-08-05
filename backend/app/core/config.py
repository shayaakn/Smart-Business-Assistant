from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True

    # Database Configuration
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    # Database URL (optional, can be constructed from individual components)
    DATABASE_URL: str | None = None

    # LLM API Configuration
    LLM_API_KEY: str
    LLM_BASE_URL: str

    # Security Configuration
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 11520

    model_config = SettingsConfigDict(env_file=".env")

    def get_database_url(self) -> str:
        """Get the database URL, either from DATABASE_URL or construct it from components."""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Settings()
