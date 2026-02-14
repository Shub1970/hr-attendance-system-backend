from datetime import date
from typing import Any
from uuid import UUID

from fastapi import HTTPException, status
from postgrest import APIError

from backend.supabase_client import get_supabase_client
from models.attendance import AttendanceCreate, AttendanceOut, AttendanceStatus, AttendanceUpdate


def _raise_from_postgrest(error: APIError) -> None:
    if error.code == "23505":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Attendance for this employee and date already exists.",
        )
    if error.code in {"23503", "23514"}:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=error.message or "Invalid attendance payload.",
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=error.message or "Unexpected database error.",
    )


def _first_row_or_500(data: list[dict[str, Any]]) -> dict[str, Any]:
    if not data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation returned no data.",
        )
    return data[0]


def create_attendance(payload: AttendanceCreate) -> AttendanceOut:
    client = get_supabase_client()

    try:
        response = client.table("attendance").insert(payload.model_dump(mode="json")).execute()
    except APIError as error:
        _raise_from_postgrest(error)

    return AttendanceOut.model_validate(_first_row_or_500(response.data))


def list_attendance(
    employee_id: UUID | None = None,
    attendance_date: date | None = None,
    status_value: AttendanceStatus | None = None,
) -> list[AttendanceOut]:
    client = get_supabase_client()

    query = client.table("attendance").select("*").order("attendance_date", desc=True)
    if employee_id:
        query = query.eq("employee_id", str(employee_id))
    if attendance_date:
        query = query.eq("attendance_date", attendance_date.isoformat())
    if status_value:
        query = query.eq("status", status_value.value)

    try:
        response = query.execute()
    except APIError as error:
        _raise_from_postgrest(error)

    return [AttendanceOut.model_validate(row) for row in response.data]


def get_attendance(attendance_id: UUID) -> AttendanceOut:
    client = get_supabase_client()

    try:
        response = (
            client.table("attendance").select("*").eq("id", str(attendance_id)).execute()
        )
    except APIError as error:
        _raise_from_postgrest(error)

    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found.",
        )

    return AttendanceOut.model_validate(response.data[0])


def update_attendance(attendance_id: UUID, payload: AttendanceUpdate) -> AttendanceOut:
    client = get_supabase_client()
    update_payload = payload.model_dump(exclude_none=True, mode="json")

    if not update_payload:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update.",
        )

    try:
        response = (
            client.table("attendance")
            .update(update_payload)
            .eq("id", str(attendance_id))
            .execute()
        )
    except APIError as error:
        _raise_from_postgrest(error)

    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found.",
        )

    return AttendanceOut.model_validate(response.data[0])


def delete_attendance(attendance_id: UUID) -> dict[str, str]:
    client = get_supabase_client()

    try:
        existing = client.table("attendance").select("id").eq("id", str(attendance_id)).execute()
    except APIError as error:
        _raise_from_postgrest(error)

    if not existing.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found.",
        )

    try:
        client.table("attendance").delete().eq("id", str(attendance_id)).execute()
    except APIError as error:
        _raise_from_postgrest(error)

    return {"message": "Attendance deleted successfully."}
