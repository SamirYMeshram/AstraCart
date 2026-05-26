from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_health(): assert client.get('/health').status_code == 200
def test_cart_view():
    r=client.get('/cart', headers={'X-User-Id':'tester'})
    assert r.status_code == 200
    assert 'subtotal' in r.json()['data']
