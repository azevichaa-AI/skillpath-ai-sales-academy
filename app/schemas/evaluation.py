from pydantic import BaseModel, Field
from typing import Any

class CheckAnswerRequest(BaseModel):
    competency_id: str
    question: str
    answer: str

class EvaluationResponse(BaseModel):
    score: int
    max_score: int = 3
    level: str
    result: str
    feedback: str
    matched_points: list[str] = Field(default_factory=list)
    missing_points: list[str] = Field(default_factory=list)
    recommended_materials: list[dict[str, Any]] = Field(default_factory=list)
    source_chunks: list[dict[str, Any]] = Field(default_factory=list)

class CaseCheckRequest(BaseModel):
    competency_id: str
    case_id: str | None = None
    answer: str
