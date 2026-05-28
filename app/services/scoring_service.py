LEVELS = {
    0: ("critical_gap", "full_basic_track", "Критический пробел: требуется базовый обучающий трек."),
    1: ("basic", "basic_plus_practice", "Базовый уровень: нужна теория, примеры и практика."),
    2: ("working", "targeted_practice_track", "Рабочий уровень: нужна точечная практика и проверка на кейсе."),
    3: ("strong", "control_case_track", "Сильный уровень: достаточно контрольного кейса и поддерживающей практики."),
}

def normalize_score(value: int | float) -> int:
    try:
        score = int(round(float(value)))
    except Exception:
        score = 0
    return max(0, min(3, score))

def score_to_level(score: int) -> dict:
    score = normalize_score(score)
    level, track_type, recommendation = LEVELS[score]
    return {"score": score, "level": level, "track_type": track_type, "recommendation": recommendation}

def readiness_status(avg_score: float, critical_count: int) -> str:
    if critical_count >= 3:
        return "needs_training"
    if avg_score < 1.25:
        return "not_ready"
    if avg_score < 2.25:
        return "ready_with_conditions"
    return "certified"

def overall_level(avg_score: float) -> str:
    if avg_score < 0.75:
        return "critical"
    if avg_score < 1.75:
        return "basic"
    if avg_score < 2.5:
        return "working"
    return "strong"
