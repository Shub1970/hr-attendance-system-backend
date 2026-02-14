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
    EmployeeCreate(
        employee_id="EMP-1006",
        full_name="Ananya Iyer",
        email="ananya.iyer@company.com",
        department="Engineering",
    ),
    EmployeeCreate(
        employee_id="EMP-1007",
        full_name="Karan Malhotra",
        email="karan.malhotra@company.com",
        department="Marketing",
    ),
    EmployeeCreate(
        employee_id="EMP-1008",
        full_name="Sneha Reddy",
        email="sneha.reddy@company.com",
        department="Finance",
    ),
    EmployeeCreate(
        employee_id="EMP-1009",
        full_name="Aditya Verma",
        email="aditya.verma@company.com",
        department="Operations",
    ),
    EmployeeCreate(
        employee_id="EMP-1010",
        full_name="Meera Nair",
        email="meera.nair@company.com",
        department="Human Resources",
    ),
    EmployeeCreate(
        employee_id="EMP-1011",
        full_name="Rahul Bansal",
        email="rahul.bansal@company.com",
        department="Sales",
    ),
    EmployeeCreate(
        employee_id="EMP-1012",
        full_name="Isha Kapoor",
        email="isha.kapoor@company.com",
        department="Engineering",
    ),
    EmployeeCreate(
        employee_id="EMP-1013",
        full_name="Manav Joshi",
        email="manav.joshi@company.com",
        department="Support",
    ),
    EmployeeCreate(
        employee_id="EMP-1014",
        full_name="Pooja Chawla",
        email="pooja.chawla@company.com",
        department="Product",
    ),
    EmployeeCreate(
        employee_id="EMP-1015",
        full_name="Nikhil Arora",
        email="nikhil.arora@company.com",
        department="Engineering",
    ),
    EmployeeCreate(
        employee_id="EMP-1016",
        full_name="Ritika Das",
        email="ritika.das@company.com",
        department="Design",
    ),
    EmployeeCreate(
        employee_id="EMP-1017",
        full_name="Harsh Vaid",
        email="harsh.vaid@company.com",
        department="Finance",
    ),
    EmployeeCreate(
        employee_id="EMP-1018",
        full_name="Divya Kulkarni",
        email="divya.kulkarni@company.com",
        department="Operations",
    ),
    EmployeeCreate(
        employee_id="EMP-1019",
        full_name="Akash Deshmukh",
        email="akash.deshmukh@company.com",
        department="Marketing",
    ),
    EmployeeCreate(
        employee_id="EMP-1020",
        full_name="Tanya Sethi",
        email="tanya.sethi@company.com",
        department="Legal",
    ),
    EmployeeCreate(
        employee_id="EMP-1021",
        full_name="Siddharth Jain",
        email="siddharth.jain@company.com",
        department="Engineering",
    ),
    EmployeeCreate(
        employee_id="EMP-1022",
        full_name="Nandini Bose",
        email="nandini.bose@company.com",
        department="Human Resources",
    ),
    EmployeeCreate(
        employee_id="EMP-1023",
        full_name="Varun Khanna",
        email="varun.khanna@company.com",
        department="Sales",
    ),
    EmployeeCreate(
        employee_id="EMP-1024",
        full_name="Kavya Menon",
        email="kavya.menon@company.com",
        department="Support",
    ),
    EmployeeCreate(
        employee_id="EMP-1025",
        full_name="Yash Tripathi",
        email="yash.tripathi@company.com",
        department="Product",
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
