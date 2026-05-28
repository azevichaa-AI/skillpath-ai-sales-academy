from pydantic import BaseModel, Field
from typing import Any

class LearningTrackBuildRequest(BaseModel):
    role_id: str = "b2b_sales_manager"
    employee_profile: str = "custom"
    competency_results: list[dict[str, Any]]

class LearningModule(BaseModel):
    competency_id: str
    competency_name: str
    track_type: str
    goal: str
    materials: list[dict[str, Any]] = Field(default_factory=list)
    practice_tasks: list[str] = Field(default_factory=list)
    control_questions: list[dict[str, Any]] = Field(default_factory=list)
    case_tasks: list[dict[str, Any]] = Field(default_factory=list)
    success_criteria: list[str] = Field(default_factory=list)

class LearningTrack(BaseModel):
    track_id: str
    employee_profile: str
    summary: str
    duration_estimate: str
    modules: list[LearningModule]
