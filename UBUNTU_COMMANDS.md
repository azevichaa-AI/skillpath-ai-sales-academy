# Команды для Ubuntu

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git curl

python3 --version
pip3 --version
git --version

mkdir -p ~/AI_DEMOS
cd ~/AI_DEMOS

# Если проект уже распакован:
cd skillpath-ai-sales-academy

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Проверка:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/api/roles
curl http://127.0.0.1:8000/api/demo-profiles
curl -X POST http://127.0.0.1:8000/api/diagnostic/run-demo   -H "Content-Type: application/json"   -d '{"role_id":"b2b_sales_manager","profile_id":"strong_manager"}'
```

GitHub:

```bash
git init
git add .
git commit -m "Initial SkillPath AI Sales Academy MVP"
git branch -M main
git remote add origin https://github.com/USERNAME/skillpath-ai-sales-academy.git
git push -u origin main
```

Render:

```text
Build Command:
pip install -r requirements.txt

Start Command:
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```
