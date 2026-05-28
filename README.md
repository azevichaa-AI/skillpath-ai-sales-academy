# SkillPath AI Sales Academy

AI-платформа для диагностики, обучения и сертификации специалистов по продажам.

Платформа помогает компаниям оценивать sales-компетенции, выявлять пробелы, назначать персональные learning tracks и проверять применение знаний на практических кейсах. MVP работает без внешних платных API: база знаний хранится в Markdown/JSON, RAG-поиск реализован простым keyword/scoring engine, проверка ответов — rule-based evaluator с готовым интерфейсом для будущего подключения LLM.

## Возможности MVP

- B2B landing page с интерактивной демонстрацией.
- FastAPI backend и Swagger API.
- Роли продаж и компетентностная модель.
- 14 компетенций для B2B Sales Manager.
- 4 демонстрационных профиля сотрудников.
- Диагностика по шкале 0–3.
- Карта компетенций и приоритетные пробелы.
- Автоматический learning track.
- Markdown/JSON база знаний.
- RAG-поиск по базе знаний.
- Проверка открытого ответа и кейса.
- Отчёт для сотрудника, руководителя и HR.
- Render/VPS-ready структура.

## Локальный запуск на Ubuntu

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git curl

cd ~/AI_DEMOS
# либо распакуйте архив, либо клонируйте репозиторий
cd skillpath-ai-sales-academy

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Открыть:

- сайт: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs
- health: http://127.0.0.1:8000/health

## Проверка API

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/api/roles
curl http://127.0.0.1:8000/api/demo-profiles
curl -X POST http://127.0.0.1:8000/api/diagnostic/run-demo   -H "Content-Type: application/json"   -d '{"role_id":"b2b_sales_manager","profile_id":"strong_manager"}'
```

## Deploy на Render

Build Command:

```bash
pip install -r requirements.txt
```

Start Command:

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Deploy на VPS Ubuntu

```bash
cd ~/AI_DEMOS/skillpath-ai-sales-academy
source .venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Структура

- `app/api` — маршруты FastAPI.
- `app/services` — diagnostic, scoring, learning, RAG, evaluation, report engines.
- `app/data` — JSON-данные MVP.
- `knowledge_base` — Markdown-база знаний.
- `app/static` — frontend.
- `docs` — архитектура, API, пилот, формат базы знаний.

## Roadmap

- PostgreSQL для пользователей и результатов.
- Qdrant/Chroma/FAISS для векторного RAG.
- OpenRouter/Gemini/local LLM evaluator.
- Admin panel для редактирования компетенций и вопросов.
- LMS/HRM integration.
- Authentication and roles.
