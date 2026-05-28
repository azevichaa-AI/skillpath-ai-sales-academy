from app.services.data_loader import load_json

class RoleService:
    def list_roles(self) -> list[dict]:
        return load_json("roles.json")

    def get_role(self, role_id: str) -> dict | None:
        return next((r for r in self.list_roles() if r.get("role_id") == role_id), None)

    def list_competencies(self, role_id: str) -> list[dict]:
        return [c for c in load_json("competencies.json") if c.get("role_id") == role_id]

    def get_competency(self, competency_id: str) -> dict | None:
        return next((c for c in load_json("competencies.json") if c.get("competency_id") == competency_id), None)

role_service = RoleService()
