import re
from app.services.data_loader import load_json
from app.services.knowledge_service import knowledge_service
from app.services.scoring_service import score_to_level

class AnswerEvaluator:
    def evaluate(self, competency_id: str, question: str, answer: str, expected_points: list[str] | None = None, keywords: list[str] | None = None) -> dict:
        expected_points = expected_points or self._expected_points(competency_id)
        keywords = keywords or self._keywords(competency_id)
        answer_norm = self._normalize(answer)
        matched_points = [p for p in expected_points if self._point_matches(p, answer_norm)]
        keyword_hits = [kw for kw in keywords if self._normalize(kw) in answer_norm]
        danger_hits = self._danger_hits(competency_id, answer_norm)
        raw = len(matched_points) + min(2, len(set(keyword_hits)))
        score = 0
        if raw >= 5:
            score = 3
        elif raw >= 3:
            score = 2
        elif raw >= 1:
            score = 1
        if danger_hits:
            score = min(score, 1)
        level_info = score_to_level(score)
        missing = [p for p in expected_points if p not in matched_points]
        chunks = knowledge_service.search(question + " " + answer, limit=3, competency_id=competency_id)
        feedback = self._feedback(score, matched_points, missing, danger_hits)
        return {
            "score": score,
            "max_score": 3,
            "level": level_info["level"],
            "result": level_info["track_type"],
            "feedback": feedback,
            "matched_points": matched_points,
            "missing_points": missing,
            "recommended_materials": self._recommended_materials(competency_id),
            "source_chunks": chunks,
        }

    def _expected_points(self, competency_id: str) -> list[str]:
        controls = load_json("control_questions.json")
        item = next((q for q in controls if q.get("competency_id") == competency_id), None)
        return item.get("expected_points", []) if item else ["контекст клиента", "ценность", "следующий шаг"]

    def _keywords(self, competency_id: str) -> list[str]:
        controls = load_json("control_questions.json")
        item = next((q for q in controls if q.get("competency_id") == competency_id), None)
        return item.get("keywords", []) if item else ["клиент", "задача", "ценность", "следующий шаг"]

    def _danger_hits(self, competency_id: str, answer_norm: str) -> list[str]:
        rubrics = load_json("rubrics.json")
        item = next((r for r in rubrics if r.get("competency_id") == competency_id), None)
        patterns = item.get("danger_patterns", []) if item else []
        return [p for p in patterns if self._normalize(p) in answer_norm]

    def _recommended_materials(self, competency_id: str) -> list[dict]:
        return [{"material_id": m["material_id"], "title": m["title"], "path": m["path"]} for m in load_json("learning_materials.json") if m.get("competency_id") == competency_id]

    def _normalize(self, text: str) -> str:
        return re.sub(r"\s+", " ", (text or "").lower().replace("ё", "е")).strip()

    def _point_matches(self, point: str, answer_norm: str) -> bool:
        words = [w for w in self._normalize(point).split() if len(w) > 3]
        return any(w in answer_norm for w in words)

    def _feedback(self, score: int, matched: list[str], missing: list[str], danger: list[str]) -> str:
        if danger:
            return "В ответе есть рискованные формулировки. Нужно опираться на стандарты, факты и ценность, не обещая невозможное."
        if score == 3:
            return "Ответ сильный: есть структура, связь с задачей клиента и понятный следующий шаг."
        if score == 2:
            return "Ответ в целом рабочий, но требует усиления по нескольким критериям."
        if score == 1:
            return "Ответ частично отражает тему, но не раскрывает ключевые элементы стандарта."
        return "Ответ не содержит достаточных признаков компетенции. Рекомендуется пройти базовый обучающий блок."

answer_evaluator = AnswerEvaluator()
