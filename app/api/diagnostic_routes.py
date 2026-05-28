from fastapi import APIRouter, HTTPException
from app.schemas.diagnostic import DemoRunRequest, StartDiagnosticRequest, DiagnosticAnswerRequest, FinishDiagnosticRequest
from app.services.diagnostic_service import diagnostic_service

router = APIRouter(prefix="/api", tags=["diagnostic"])

@router.get("/demo-profiles")
def demo_profiles():
    return diagnostic_service.demo_profiles()

@router.post("/diagnostic/run-demo")
def run_demo(payload: DemoRunRequest):
    try:
        return diagnostic_service.run_demo(payload.role_id, payload.profile_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/diagnostic/run")
def run_demo_legacy(payload: DemoRunRequest):
    return run_demo(payload)

@router.post("/diagnostic/start")
def start(payload: StartDiagnosticRequest):
    return diagnostic_service.start(payload.role_id, payload.employee_name)

@router.post("/diagnostic/answer")
def answer(payload: DiagnosticAnswerRequest):
    try:
        return diagnostic_service.answer(payload.session_id, payload.question_id, payload.answer)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/diagnostic/finish")
def finish(payload: FinishDiagnosticRequest):
    try:
        return diagnostic_service.finish(payload.session_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/diagnostic/{session_id}/result")
def result(session_id: str):
    item = diagnostic_service.get_result(session_id)
    if not item:
        raise HTTPException(status_code=404, detail="Result not found")
    return item
