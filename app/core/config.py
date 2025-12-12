from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    app_name: str = Field(default="Org Management Service", alias="APP_NAME")
    jwt_secret: str = Field(alias="JWT_SECRET")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGO")
    jwt_expire_minutes: int = Field(default=1440, alias="JWT_EXPIRE_MINUTES")
    
    mongo_uri: str = Field(alias="MONGO_URI")
    master_db: str = Field(default="master_db", alias="MASTER_DB")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",  # Ignore extra fields from .env
        populate_by_name=True  # Allow both field name and alias
    )


settings = Settings()

