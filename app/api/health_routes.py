from fastapi import APIRouter
from app.config import APP_NAME, APP_VERSION
from app.services.knowledge_service import knowledge_service

router = APIRouter()

@router.get("/health")
def health():
    status = knowledge_service.content_status()
    return {"status": "ok", "app": APP_NAME, "version": APP_VERSION, "knowledge": status}
