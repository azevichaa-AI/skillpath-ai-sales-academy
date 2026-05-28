# Архитектура SkillPath AI Sales Academy

## Frontend

Одностраничный интерфейс в `app/static`: landing page, выбор профиля, запуск диагностики, карта компетенций, learning track и проверка ответа.

## Backend

FastAPI приложение в `app/main.py` подключает маршруты:

- health;
- roles;
- diagnostic;
- learning;
- knowledge;
- control;
- cases;
- reports.

## Diagnostic Engine

Принимает роль и профиль/ответы, рассчитывает score по компетенциям, определяет уровень и track type.

## Scoring Engine

Шкала 0–3:

- 0 — critical_gap;
- 1 — basic;
- 2 — working;
- 3 — strong.

## Learning Track Engine

Строит маршрут развития по каждому пробелу: материалы, практика, контрольные вопросы, кейсы, критерии успеха.

## Knowledge/RAG Engine

Markdown-файлы индексируются при старте, режутся на чанки и ищутся keyword/scoring алгоритмом. Архитектура подготовлена к замене на Qdrant/Chroma/FAISS/pgvector.

## Answer Evaluation Engine

MVP использует rule-based оценку: expected_points, keywords, danger_patterns, source_chunks. Интерфейс готов к будущему LLM-evaluator.
