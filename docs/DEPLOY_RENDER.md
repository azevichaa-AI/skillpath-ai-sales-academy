# Deploy на Render

1. Загрузите проект в GitHub.
2. В Render создайте New Web Service.
3. Подключите репозиторий.
4. Environment: Python.
5. Build Command: `pip install -r requirements.txt`.
6. Start Command: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
7. Откройте `/health` и `/docs` после деплоя.
