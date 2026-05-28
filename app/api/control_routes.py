from fastapi import APIRouter
from app.schemas.evaluation import CheckAnswerRequest
from app.services.answer_evaluator import answer_evaluator

router = APIRouter(prefix="/api", tags=["control"])

@router.post("/control/check-answer")
def check_answer(payload: CheckAnswerRequest):
    return answer_evaluator.evaluate(payload.competency_id, payload.question, payload.answer)
