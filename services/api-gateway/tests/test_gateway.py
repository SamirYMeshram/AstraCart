from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_gateway_health_shape():
    r=client.get('/health')
    assert r.status_code == 200
    assert r.json()['success'] is True
def test_unregistered_route():
    r=client.get('/unknown/service')
    assert r.status_code in (404, 429)
