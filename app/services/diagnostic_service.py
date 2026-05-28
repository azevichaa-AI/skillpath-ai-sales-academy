from uuid import uuid4
from app.services.data_loader import load_json
from app.services.role_service import role_service
from app.services.scoring_service import score_to_level, readiness_status, overall_level
from app.services.coverage_service import coverage_service
from app.services.learning_track_service import learning_track_service, learning_tracks_store
from app.services.answer_evaluator import answer_evaluator

sessions_store: dict[str, dict] = {}
results_store: dict[str, dict] = {}

class DiagnosticService:
    def demo_profiles(self) -> list[dict]:
        return load_json("demo_profiles.json")

    def run_demo(self, role_id: str, profile_id: str) -> dict:
        profile = next((p for p in self.demo_profiles() if p.get("profile_id") == profile_id), None)
        if not profile:
            raise ValueError(f"Unknown profile_id: {profile_id}")
        competencies = role_service.list_competencies(role_id)
        results = self._results_from_scores(competencies, profile.get("scores", {}))
        return self._finalize_result(role_id, profile["name"], profile["description"], results)

    def start(self, role_id: str, employee_name: str | None = None) -> dict:
        session_id = f"sess_{uuid4().hex[:10]}"
        questions = [q for q in load_json("diagnostic_questions.json") if q.get("role_id") == role_id][:12]
        sessions_store[session_id] = {"session_id": session_id, "role_id": role_id, "employee_name": employee_name or "Сотрудник", "answers": [], "questions": questions}
        return {"session_id": session_id, "role_id": role_id, "employee_name": employee_name, "questions": questions}

    def answer(self, session_id: str, question_id: str, answer) -> dict:
        session = sessions_store.get(session_id)
        if not session:
            raise ValueError("Unknown session_id")
        q = next((item for item in session["questions"] if item.get("question_id") == question_id), None)
        if not q:
            raise ValueError("Unknown question_id")
        score = self._score_question(q, answer)
        record = {"question_id": question_id, "competency_id": q["competency_id"], "answer": answer, "score": score}
        session["answers"].append(record)
        return {"accepted": True, "record": record}

    def finish(self, session_id: str) -> dict:
        session = sessions_store.get(session_id)
        if not session:
            raise ValueError("Unknown session_id")
        competencies = role_service.list_competencies(session["role_id"])
        per_comp = {c["competency_id"]: [] for c in competencies}
        for ans in session["answers"]:
            per_comp.setdefault(ans["competency_id"], []).append(ans["score"])
        scores = {cid: round(sum(vals)/len(vals)) if vals else 0 for cid, vals in per_comp.items()}
        results = self._results_from_scores(competencies, scores)
        return self._finalize_result(session["role_id"], session["employee_name"], "Полная диагностическая сессия", results, session_id=session_id)

    def get_result(self, session_id: str) -> dict | None:
        return results_store.get(session_id)

    def _score_question(self, q: dict, answer) -> int:
        if q.get("type") in {"single_choice", "multiple_choice"}:
            expected = set(map(str, q.get("correct_answer", [])))
            got = set(map(str, answer if isinstance(answer, list) else [answer]))
            if got == expected:
                return 3
            if got & expected:
                return 2
            return 0
        evaluated = answer_evaluator.evaluate(q["competency_id"], q["question"], str(answer), q.get("expected_points"), q.get("keywords"))
        return int(evaluated["score"])

    def _results_from_scores(self, competencies: list[dict], scores: dict) -> list[dict]:
        results = []
        for comp in competencies:
            score = int(scores.get(comp["competency_id"], 0))
            info = score_to_level(score)
            evidence = ["демонстрационный профиль" if scores else "ответы диагностической сессии"]
            mistakes = []
            if score <= 1:
                mistakes.append("недостаточно признаков уверенного применения компетенции")
            results.append({
                "competency_id": comp["competency_id"],
                "competency_name": comp["name"],
                "score": info["score"],
                "max_score": 3,
                "level": info["level"],
                "track_type": info["track_type"],
                "evidence": evidence,
                "mistakes": mistakes,
                "recommendation": info["recommendation"],
            })
        return results

    def _finalize_result(self, role_id: str, profile_name: str, profile_desc: str, results: list[dict], session_id: str | None = None) -> dict:
        session_id = session_id or f"demo_{uuid4().hex[:10]}"
        avg = sum(r["score"] for r in results) / max(1, len(results))
        critical_count = sum(1 for r in results if r["score"] == 0)
        gaps = coverage_service.priority_gaps(results)
        track = learning_track_service.build_from_results(profile_name, results)
        learning_tracks_store[track["track_id"]] = track
        summary = self._summary(profile_name, avg, gaps)
        result = {
            "session_id": session_id,
            "role_id": role_id,
            "employee_profile": profile_name,
            "profile_description": profile_desc,
            "overall_level": overall_level(avg),
            "readiness_status": readiness_status(avg, critical_count),
            "overall_summary": summary,
            "competency_results": results,
            "priority_gaps": gaps,
            "learning_track": track["modules"],
            "track_id": track["track_id"],
        }
        results_store[session_id] = result
        return result

    def _summary(self, name: str, avg: float, gaps: list[dict]) -> str:
        if avg >= 2.5:
            return f"{name}: высокий уровень, основной маршрут — контрольные кейсы и точечное усиление."
        if avg >= 1.5:
            return f"{name}: рабочий уровень, требуется точечная практика по приоритетным пробелам."
        return f"{name}: требуется базовый обучающий трек по ключевым компетенциям продаж."

diagnostic_service = DiagnosticService()
