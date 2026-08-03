from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True
    
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    
    LLM_API_KEY: str
    LLM_BASE_URL: str
    
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 11520

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()