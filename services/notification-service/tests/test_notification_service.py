from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_health(): assert client.get('/health').status_code == 200
def test_create_notification():
    r=client.post('/notifications', json={'user_id':'tester','event':'ORDER_PLACED','title':'Order placed','message':'Your order was placed','channel':'IN_APP','metadata_json':{}})
    assert r.status_code == 201
    assert r.json()['data']['read'] is False
