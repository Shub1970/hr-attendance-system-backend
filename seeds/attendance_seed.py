from datetime import date, timedelta

from postgrest import APIError

from backend.supabase_client import get_supabase_client
from models.attendance import AttendanceStatus


def _status_for_day(day: date, employee_code: str) -> AttendanceStatus:
    if day == date.today():
        score = (day.toordinal() + sum(ord(ch) for ch in employee_code)) % 10
        return AttendanceStatus.present if score < 6 else AttendanceStatus.absent

    if day.weekday() >= 5:
        return AttendanceStatus.absent

    score = (day.toordinal() + sum(ord(ch) for ch in employee_code)) % 10
    return AttendanceStatus.present if score < 8 else AttendanceStatus.absent


def seed_attendance(day_offsets: tuple[int, ...] = (0, 1, 3)) -> int:
    client = get_supabase_client()

    employees_response = client.table("employees").select("id, employee_id").execute()
    raw_employees = employees_response.data or []
    employees: list[dict[str, str]] = []

    for record in raw_employees:
        if not isinstance(record, dict):
            continue

        employee_uuid = record.get("id")
        employee_code = record.get("employee_id")
        if isinstance(employee_uuid, str) and isinstance(employee_code, str):
            employees.append({"id": employee_uuid, "employee_id": employee_code})

    if not employees:
        return 0

    today = date.today()
    payload: list[dict[str, str]] = []

    for day_offset in sorted(set(day_offsets)):
        current_date = today - timedelta(days=day_offset)
        for employee in employees:
            status_value = _status_for_day(current_date, employee["employee_id"])
            payload.append(
                {
                    "employee_id": employee["id"],
                    "attendance_date": current_date.isoformat(),
                    "status": status_value.value,
                }
            )

    response = (
        client.table("attendance")
        .upsert(payload, on_conflict="employee_id,attendance_date")
        .execute()
    )
    return len(response.data or [])


if __name__ == "__main__":
    try:
        seeded_count = seed_attendance(day_offsets=(0, 1, 3))
        if seeded_count == 0:
            print("Attendance seed skipped: no employees found. Seed employees first.")
        else:
            print(f"Attendance seed completed. Upserted records: {seeded_count}")
    except APIError as error:
        print(f"Attendance seed failed: {error.message}")
        raise SystemExit(1)
