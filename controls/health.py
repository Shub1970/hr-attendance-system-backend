from pydantic import BaseModel

from backend.config import get_settings
from backend.supabase_client import get_supabase_client


class HealthResponse(BaseModel):
    status: str
    supabase_configured: bool


def health_check() -> HealthResponse:
    settings = get_settings()
    get_supabase_client()
    return HealthResponse(
        status="ok",
        supabase_configured=bool(settings.supabase_url and settings.supabase_key),
    )
