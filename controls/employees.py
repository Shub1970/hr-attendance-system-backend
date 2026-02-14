from typing import Any
from uuid import UUID

from fastapi import HTTPException, status
from postgrest import APIError

from backend.supabase_client import get_supabase_client
from models.employee import EmployeeCreate, EmployeeOut, EmployeeUpdate


def _raise_from_postgrest(error: APIError) -> None:
    if error.code == "23505":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee with the same employee_id or email already exists.",
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


def create_employee(payload: EmployeeCreate) -> EmployeeOut:
    client = get_supabase_client()

    try:
        response = client.table("employees").insert(payload.model_dump()).execute()
    except APIError as error:
        _raise_from_postgrest(error)

    return EmployeeOut.model_validate(_first_row_or_500(response.data))


def list_employees() -> list[EmployeeOut]:
    client = get_supabase_client()

    try:
        response = (
            client.table("employees")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )
    except APIError as error:
        _raise_from_postgrest(error)

    return [EmployeeOut.model_validate(row) for row in response.data]


def get_employee(employee_id: UUID) -> EmployeeOut:
    client = get_supabase_client()

    try:
        response = client.table("employees").select("*").eq("id", str(employee_id)).execute()
    except APIError as error:
        _raise_from_postgrest(error)

    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found.",
        )

    return EmployeeOut.model_validate(response.data[0])


def update_employee(employee_id: UUID, payload: EmployeeUpdate) -> EmployeeOut:
    client = get_supabase_client()
    update_payload = payload.model_dump(exclude_none=True)

    if not update_payload:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update.",
        )

    try:
        response = (
            client.table("employees")
            .update(update_payload)
            .eq("id", str(employee_id))
            .execute()
        )
    except APIError as error:
        _raise_from_postgrest(error)

    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found.",
        )

    return EmployeeOut.model_validate(response.data[0])


def delete_employee(employee_id: UUID) -> dict[str, str]:
    client = get_supabase_client()

    try:
        existing = client.table("employees").select("id").eq("id", str(employee_id)).execute()
    except APIError as error:
        _raise_from_postgrest(error)

    if not existing.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found.",
        )

    try:
        client.table("employees").delete().eq("id", str(employee_id)).execute()
    except APIError as error:
        _raise_from_postgrest(error)

    return {"message": "Employee deleted successfully."}
