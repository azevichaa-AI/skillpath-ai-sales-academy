class CoverageService:
    def priority_gaps(self, competency_results: list[dict]) -> list[dict]:
        gaps = []
        for item in competency_results:
            score = int(item.get("score", 0))
            if score <= 1:
                gaps.append({
                    "competency_id": item["competency_id"],
                    "competency_name": item["competency_name"],
                    "score": score,
                    "risk": "high" if score == 0 else "medium",
                    "reason": "Критически влияет на качество продаж" if score == 0 else "Требует практического закрепления"
                })
        return sorted(gaps, key=lambda x: x["score"])

coverage_service = CoverageService()
