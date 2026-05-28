from app.services.diagnostic_service import results_store

class ReportService:
    def build(self, session_id: str) -> dict | None:
        result = results_store.get(session_id)
        if not result:
            return None
        strong = [r for r in result["competency_results"] if r["score"] >= 3]
        risks = [r for r in result["competency_results"] if r["score"] <= 1]
        practice = [r for r in result["competency_results"] if r["score"] == 2]
        return {
            "session_id": session_id,
            "employee_report": {
                "summary": result["overall_summary"],
                "strong_sides": [r["competency_name"] for r in strong],
                "development_zones": [r["competency_name"] for r in risks + practice],
                "next_step": "Пройти назначенный learning track и контрольные кейсы.",
            },
            "manager_report": {
                "readiness_status": result["readiness_status"],
                "priority_gaps": result["priority_gaps"],
                "risks": [r["competency_name"] for r in risks],
                "recommendation": "Назначить обучение по критическим пробелам и проверить применение навыков на кейсах.",
            },
            "hr_report": {
                "training_needs": [r["competency_name"] for r in risks],
                "targeted_practice": [r["competency_name"] for r in practice],
                "certification_candidates": [r["competency_name"] for r in strong],
            },
        }

report_service = ReportService()
