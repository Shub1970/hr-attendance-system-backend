from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.attendance import router as attendance_router
from routers.employees import router as employees_router
from routers.health import router as health_router


app = FastAPI(
    title="HR Attendance API",
    description="FastAPI + Supabase backend for employee and attendance management.",
    version="1.0.0",
    swagger_ui_parameters={
        "docExpansion": "none",
        "defaultModelsExpandDepth": -1,
        "defaultModelExpandDepth": -1,
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://hr-attendance-system-frontend-u4pa.vercel.app",
        "http://localhost",
        "http://localhost:80",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(employees_router)
app.include_router(attendance_router)
