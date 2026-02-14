from uuid import UUID

from fastapi import APIRouter, status

from controls import employees as employees_control
from models.employee import EmployeeCreate, EmployeeOut, EmployeeUpdate


router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post(
    "",
    response_model=EmployeeOut,
    status_code=status.HTTP_201_CREATED,
    description="Create a new employee.",
)
def create_employee(payload: EmployeeCreate) -> EmployeeOut:
    return employees_control.create_employee(payload)


@router.get("", response_model=list[EmployeeOut], description="Get all employees.")
def list_employees() -> list[EmployeeOut]:
    return employees_control.list_employees()


@router.get("/{employee_id}", response_model=EmployeeOut, description="Get one employee by UUID.")
def get_employee(employee_id: UUID) -> EmployeeOut:
    return employees_control.get_employee(employee_id)


@router.put("/{employee_id}", response_model=EmployeeOut, description="Update an employee by UUID.")
def update_employee(employee_id: UUID, payload: EmployeeUpdate) -> EmployeeOut:
    return employees_control.update_employee(employee_id, payload)


@router.delete("/{employee_id}", description="Delete an employee by UUID.")
def delete_employee(employee_id: UUID) -> dict[str, str]:
    return employees_control.delete_employee(employee_id)
