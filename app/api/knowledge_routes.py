from fastapi import APIRouter, HTTPException, Query
from app.services.knowledge_service import knowledge_service

router = APIRouter(prefix="/api", tags=["knowledge"])

@router.get("/knowledge/search")
def search(query: str = Query(..., min_length=1), limit: int = 5, competency_id: str | None = None):
    results = knowledge_service.search(query=query, limit=limit, competency_id=competency_id)
    return {"query": query, "results": results, "total": len(results)}

@router.get("/knowledge/materials/{material_id}")
def material(material_id: str):
    item = knowledge_service.get_material(material_id)
    if not item:
        raise HTTPException(status_code=404, detail="Material not found")
    return item

@router.get("/admin/content-status")
def content_status():
    return knowledge_service.content_status()
