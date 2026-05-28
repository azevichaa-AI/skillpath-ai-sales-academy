from pydantic import BaseModel, Field
from .common import SourceChunk

class KnowledgeSearchResponse(BaseModel):
    query: str
    results: list[SourceChunk]
    total: int

class MaterialResponse(BaseModel):
    material_id: str
    title: str
    path: str
    content: str
    metadata: dict = Field(default_factory=dict)
