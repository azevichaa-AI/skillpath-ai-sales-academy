from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json()['status'] == 'ok'

def test_roles():
    r = client.get('/api/roles')
    assert r.status_code == 200
    assert len(r.json()) >= 1

def test_run_demo():
    r = client.post('/api/diagnostic/run-demo', json={'role_id':'b2b_sales_manager','profile_id':'strong_manager'})
    assert r.status_code == 200
    data = r.json()
    assert data['readiness_status'] in {'certified','ready_with_conditions','needs_training','not_ready'}
    assert len(data['competency_results']) >= 10

def test_knowledge_search():
    r = client.get('/api/knowledge/search', params={'query':'возражение цена клиент', 'limit':3})
    assert r.status_code == 200
    assert r.json()['total'] >= 1

def test_check_answer():
    r = client.post('/api/control/check-answer', json={'competency_id':'objection_handling','question':'Клиент говорит, что дорого. Что ответить?','answer':'Нужно уточнить, что именно сравнивает клиент, вернуться к ценности и договориться о следующем шаге.'})
    assert r.status_code == 200
    assert r.json()['score'] >= 1
