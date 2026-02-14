from fastapi import APIRouter
from pydantic import BaseModel

from backend.config import get_settings
from backend.supabase_client import get_supabase_client


router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    status: str
    supabase_configured: bool


@router.get("/health", response_model=HealthResponse, summary="Health check")
def health_check() -> HealthResponse:
    settings = get_settings()
    get_supabase_client()
    return HealthResponse(
        status="ok",
        supabase_configured=bool(settings.supabase_url and settings.supabase_key),
    )
