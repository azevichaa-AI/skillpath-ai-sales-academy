from app.services.data_loader import load_json
from app.services.answer_evaluator import answer_evaluator

class CaseEvaluator:
    def check_case(self, competency_id: str, answer: str, case_id: str | None = None) -> dict:
        cases = load_json("case_tasks.json")
        case = None
        if case_id:
            case = next((c for c in cases if c.get("case_id") == case_id), None)
        if not case:
            case = next((c for c in cases if c.get("competency_id") == competency_id), None)
        question = (case or {}).get("task", "Решите практический кейс.")
        expected_points = (case or {}).get("expected_points")
        keywords = (case or {}).get("keywords")
        result = answer_evaluator.evaluate(competency_id, question, answer, expected_points, keywords)
        result["case"] = case
        return result

case_evaluator = CaseEvaluator()
