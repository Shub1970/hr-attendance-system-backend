import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError, field_validator


load_dotenv()


class Settings(BaseModel):
    supabase_url: str
    supabase_key: str

    @field_validator("supabase_url", "supabase_key")
    @classmethod
    def must_not_be_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Environment value cannot be empty")
        return value


@lru_cache
def get_settings() -> Settings:
    try:
        return Settings(
            supabase_url=os.getenv("SUPABASE_URL", ""),
            supabase_key=os.getenv("SUPABASE_KEY", ""),
        )
    except ValidationError as exc:
        raise RuntimeError(
            "Invalid environment setup. Please set SUPABASE_URL and SUPABASE_KEY in .env"
        ) from exc
