from pydantic import BaseModel, Field

class Role(BaseModel):
    role_id: str
    name: str
    name_ru: str | None = None
    status: str = "active"
    description: str = ""
    competency_ids: list[str] = Field(default_factory=list)

class Competency(BaseModel):
    competency_id: str
    role_id: str
    name: str
    name_en: str = ""
    description: str = ""
    weight: float = 1.0
    tags: list[str] = Field(default_factory=list)
