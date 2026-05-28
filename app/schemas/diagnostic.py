from pydantic import BaseModel, Field
from typing import Any

class DemoRunRequest(BaseModel):
    role_id: str = "b2b_sales_manager"
    profile_id: str

class StartDiagnosticRequest(BaseModel):
    role_id: str = "b2b_sales_manager"
    employee_name: str | None = None

class DiagnosticAnswerRequest(BaseModel):
    session_id: str
    question_id: str
    answer: str | list[int] | list[str]

class FinishDiagnosticRequest(BaseModel):
    session_id: str

class CompetencyResult(BaseModel):
    competency_id: str
    competency_name: str
    score: int
    max_score: int = 3
    level: str
    track_type: str
    evidence: list[str] = Field(default_factory=list)
    mistakes: list[str] = Field(default_factory=list)
    recommendation: str

class DiagnosticResult(BaseModel):
    session_id: str
    role_id: str
    employee_profile: str
    overall_level: str
    readiness_status: str
    overall_summary: str
    competency_results: list[CompetencyResult]
    priority_gaps: list[dict[str, Any]] = Field(default_factory=list)
    learning_track: list[dict[str, Any]] = Field(default_factory=list)
