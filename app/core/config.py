from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    APP_NAME: str = "Ticket CRUD API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    DATABASE_URL: str = "postgresql+asyncpg://postgres:1234@localhost:5432/ai_service_desk"
    SECRET_KEY: str = "secret_key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    AWS_DEMO_MODE: bool = False
    DATABASE_READY: bool = True
    BEDROCK_MODEL_ID: str = "arn:aws:bedrock:us-east-1:604264782540:application-inference-profile/ji9xd8sqpai6"
    AWS_ACCESS_KEY_ID: str 
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION:str = "us-east-1"
settings = Settings()