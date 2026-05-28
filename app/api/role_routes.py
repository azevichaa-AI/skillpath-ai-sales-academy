from fastapi import APIRouter, HTTPException
from app.services.role_service import role_service

router = APIRouter(prefix="/api", tags=["roles"])

@router.get("/roles")
def list_roles():
    return role_service.list_roles()

@router.get("/roles/{role_id}/competencies")
def list_competencies(role_id: str):
    role = role_service.get_role(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role_service.list_competencies(role_id)

@router.get("/competencies/{role_id}")
def legacy_competencies(role_id: str):
    return list_competencies(role_id)
