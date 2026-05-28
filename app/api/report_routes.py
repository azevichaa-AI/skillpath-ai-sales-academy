from fastapi import APIRouter, HTTPException
from app.services.report_service import report_service

router = APIRouter(prefix="/api", tags=["reports"])

@router.get("/report/{session_id}")
def report(session_id: str):
    item = report_service.build(session_id)
    if not item:
        raise HTTPException(status_code=404, detail="Report not found")
    return item
