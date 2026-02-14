from fastapi import FastAPI

from routers.attendance import router as attendance_router
from routers.employees import router as employees_router
from routers.health import router as health_router


app = FastAPI(
    title="HR Attendance API",
    description="FastAPI + Supabase backend for employee and attendance management.",
    version="1.0.0",
)

app.include_router(health_router)
app.include_router(employees_router)
app.include_router(attendance_router)
