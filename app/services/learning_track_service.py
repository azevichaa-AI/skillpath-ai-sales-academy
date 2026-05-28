from uuid import uuid4
from app.services.data_loader import load_json
from app.services.knowledge_service import knowledge_service

TRACK_DESCRIPTIONS = {
    "full_basic_track": {
        "duration": "3–5 учебных блоков",
        "goal_prefix": "Сформировать базовое понимание и безопасную практику",
        "actions": ["изучить теорию", "разобрать хорошие и плохие примеры", "выполнить практические упражнения", "пройти контрольный кейс"],
    },
    "basic_plus_practice": {
        "duration": "2–3 учебных блока",
        "goal_prefix": "Закрыть базовые пробелы и закрепить навык",
        "actions": ["повторить ключевые правила", "разобрать типовые ошибки", "выполнить практику", "ответить на контрольные вопросы"],
    },
    "targeted_practice_track": {
        "duration": "1–2 практических блока",
        "goal_prefix": "Усилить применение навыка в реальных ситуациях",
        "actions": ["выполнить точечное упражнение", "решить кейс", "получить обратную связь"],
    },
    "control_case_track": {
        "duration": "1 контрольный блок",
        "goal_prefix": "Подтвердить соответствие стандарту роли",
        "actions": ["пройти контрольный кейс", "подтвердить стандарт", "получить поддерживающую рекомендацию"],
    },
}

class LearningTrackService:
    def build_from_results(self, employee_profile: str, competency_results: list[dict]) -> dict:
        modules = []
        materials = load_json("learning_materials.json")
        controls = load_json("control_questions.json")
        cases = load_json("case_tasks.json")
        for result in competency_results:
            competency_id = result["competency_id"]
            track_type = result["track_type"]
            desc = TRACK_DESCRIPTIONS.get(track_type, TRACK_DESCRIPTIONS["targeted_practice_track"])
            matched_materials = [m for m in materials if m.get("competency_id") == competency_id]
            source_chunks = knowledge_service.search(result["competency_name"], limit=2, competency_id=competency_id)
            modules.append({
                "competency_id": competency_id,
                "competency_name": result["competency_name"],
                "track_type": track_type,
                "goal": f"{desc['goal_prefix']}: {result['competency_name']}",
                "materials": [{"material_id": m["material_id"], "title": m["title"], "path": m["path"]} for m in matched_materials],
                "source_chunks": source_chunks,
                "practice_tasks": self._practice_tasks(track_type, result["competency_name"]),
                "control_questions": [q for q in controls if q.get("competency_id") == competency_id][:3],
                "case_tasks": [c for c in cases if c.get("competency_id") == competency_id][:2],
                "success_criteria": ["ответ опирается на задачу клиента", "есть структурное объяснение", "зафиксирован следующий шаг"],
            })
        avg = sum(int(r["score"]) for r in competency_results) / max(1, len(competency_results))
        return {
            "track_id": f"track_{uuid4().hex[:10]}",
            "employee_profile": employee_profile,
            "summary": f"Персональный маршрут построен по {len(modules)} компетенциям. Средний уровень: {avg:.2f}/3.",
            "duration_estimate": self._duration_estimate(competency_results),
            "modules": modules,
        }

    def _practice_tasks(self, track_type: str, name: str) -> list[str]:
        if track_type == "full_basic_track":
            return [f"Составить чек-лист по теме «{name}»", "Разобрать слабый пример и исправить его", "Сформулировать ответ клиенту по кейсу"]
        if track_type == "basic_plus_practice":
            return [f"Назвать типовые ошибки по теме «{name}»", "Решить мини-кейс с обратной связью"]
        if track_type == "targeted_practice_track":
            return [f"Выполнить точечное упражнение по теме «{name}»"]
        return [f"Пройти контрольный кейс по теме «{name}»"]

    def _duration_estimate(self, results: list[dict]) -> str:
        heavy = sum(1 for r in results if r["track_type"] in {"full_basic_track", "basic_plus_practice"})
        targeted = sum(1 for r in results if r["track_type"] == "targeted_practice_track")
        return f"{heavy * 2 + targeted + 1}–{heavy * 3 + targeted * 2 + 2} учебных блоков"

learning_track_service = LearningTrackService()
learning_tracks_store: dict[str, dict] = {}
