from fastapi import APIRouter

from controls.health import HealthResponse, health_check as health_check_control


router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse, description="Check API health and Supabase configuration.")
def health_check() -> HealthResponse:
    return health_check_control()
