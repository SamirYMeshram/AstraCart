from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_health(): assert client.get('/health').status_code == 200
def test_orders_list(): assert client.get('/orders', headers={'X-User-Id':'demo-customer'}).status_code == 200
