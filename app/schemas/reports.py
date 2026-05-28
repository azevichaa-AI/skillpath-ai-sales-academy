from pydantic import BaseModel, Field
from typing import Any

class ReportResponse(BaseModel):
    session_id: str
    employee_report: dict[str, Any]
    manager_report: dict[str, Any]
    hr_report: dict[str, Any]
