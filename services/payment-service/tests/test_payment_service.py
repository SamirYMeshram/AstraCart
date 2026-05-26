from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_health(): assert client.get('/health').status_code == 200
def test_payment_initiate():
    r=client.post('/payments/initiate', json={'order_id':'order-test','amount':999})
    assert r.status_code == 201
    assert r.json()['data']['status'] == 'INITIATED'
