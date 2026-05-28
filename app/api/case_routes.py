from fastapi import APIRouter
from app.schemas.evaluation import CaseCheckRequest
from app.services.case_evaluator import case_evaluator

router = APIRouter(prefix="/api", tags=["cases"])

@router.post("/case/check")
def check_case(payload: CaseCheckRequest):
    return case_evaluator.check_case(payload.competency_id, payload.answer, payload.case_id)
