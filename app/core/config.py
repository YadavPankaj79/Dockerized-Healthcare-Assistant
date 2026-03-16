from functools import lru_cache

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()  # Load environment variables from .env if present


class Settings(BaseSettings):
    app_name: str = "Healthcare Planning Assistant"
    env: str = Field("dev", validation_alias="ENV")
    debug: bool = Field(True, validation_alias="DEBUG")

    # LLM configuration
    default_model: str = Field("gemini", validation_alias="DEFAULT_MODEL")
    gemini_api_key: str | None = Field(default=None, validation_alias="GEMINI_API_KEY")
    gemini_model: str = Field("gemini-1.5-flash", validation_alias="GEMINI_MODEL")

    groq_api_key: str | None = Field(default=None, validation_alias="GROQ_API_KEY")
    groq_model: str = Field("llama-3.1-8b-instant", validation_alias="GROQ_MODEL")

    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()

