from datetime import date
from uuid import UUID

from fastapi import APIRouter, Query, status

from controls import attendance as attendance_control
from models.attendance import AttendanceCreate, AttendanceOut, AttendanceStatus, AttendanceUpdate


router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post(
    "",
    response_model=AttendanceOut,
    status_code=status.HTTP_201_CREATED,
    description="Create an attendance record.",
)
def create_attendance(payload: AttendanceCreate) -> AttendanceOut:
    return attendance_control.create_attendance(payload)


@router.get("", response_model=list[AttendanceOut], description="Get attendance records.")
def list_attendance(
    employee_id: UUID | None = Query(default=None),
    attendance_date: date | None = Query(default=None),
    status_value: AttendanceStatus | None = Query(default=None, alias="status"),
) -> list[AttendanceOut]:
    return attendance_control.list_attendance(employee_id, attendance_date, status_value)


@router.get("/{attendance_id}", response_model=AttendanceOut, description="Get one attendance record by UUID.")
def get_attendance(attendance_id: UUID) -> AttendanceOut:
    return attendance_control.get_attendance(attendance_id)


@router.put("/{attendance_id}", response_model=AttendanceOut, description="Update an attendance record by UUID.")
def update_attendance(attendance_id: UUID, payload: AttendanceUpdate) -> AttendanceOut:
    return attendance_control.update_attendance(attendance_id, payload)


@router.delete("/{attendance_id}", description="Delete an attendance record by UUID.")
def delete_attendance(attendance_id: UUID) -> dict[str, str]:
    return attendance_control.delete_attendance(attendance_id)
