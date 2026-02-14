from datetime import date, datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AttendanceStatus(str, Enum):
    present = "present"
    absent = "absent"


class AttendanceCreate(BaseModel):
    employee_id: UUID
    attendance_date: date
    status: AttendanceStatus


class AttendanceUpdate(BaseModel):
    attendance_date: Optional[date] = None
    status: Optional[AttendanceStatus] = None


class AttendanceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    employee_id: UUID
    attendance_date: date
    status: AttendanceStatus
    created_at: datetime
