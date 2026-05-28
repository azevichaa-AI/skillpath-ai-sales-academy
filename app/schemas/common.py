from pydantic import BaseModel, Field
from typing import Any, Optional

class StatusResponse(BaseModel):
    status: str = "ok"
    app: str
    version: str

class ErrorResponse(BaseModel):
    detail: str
    code: Optional[str] = None

class SourceChunk(BaseModel):
    source_id: str
    title: str
    path: str
    score: float
    text: str
    metadata: dict[str, Any] = Field(default_factory=dict)
