from postgrest import APIError

from backend.supabase_client import get_supabase_client
from models.employee import EmployeeCreate


SEED_EMPLOYEES: list[EmployeeCreate] = [
    EmployeeCreate(
        employee_id="EMP-1001",
        full_name="Aarav Sharma",
        email="aarav.sharma@company.com",
        department="Engineering",
    ),
    EmployeeCreate(
        employee_id="EMP-1002",
        full_name="Priya Patel",
        email="priya.patel@company.com",
        department="Human Resources",
    ),
    EmployeeCreate(
        employee_id="EMP-1003",
        full_name="Rohan Mehta",
        email="rohan.mehta@company.com",
        department="Finance",
    ),
    EmployeeCreate(
        employee_id="EMP-1004",
        full_name="Neha Singh",
        email="neha.singh@company.com",
        department="Operations",
    ),
    EmployeeCreate(
        employee_id="EMP-1005",
        full_name="Vikram Rao",
        email="vikram.rao@company.com",
        department="Sales",
    ),
]


def seed_employees() -> int:
    client = get_supabase_client()
    payload = [employee.model_dump() for employee in SEED_EMPLOYEES]

    response = client.table("employees").upsert(payload, on_conflict="employee_id").execute()
    return len(response.data or [])


if __name__ == "__main__":
    try:
        seeded_count = seed_employees()
        print(f"Employees seed completed. Upserted records: {seeded_count}")
    except APIError as error:
        print(f"Employees seed failed: {error.message}")
        raise SystemExit(1)
