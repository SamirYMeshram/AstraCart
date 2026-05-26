from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    assert client.get('/health').status_code == 200

def test_register_login_refresh_flow():
    payload = {'email':'new.customer@example.com','full_name':'New Customer','password':'CustomerPass123!','role':'CUSTOMER'}
    r = client.post('/auth/register', json=payload)
    assert r.status_code in (201, 409)
    login = client.post('/auth/login', json={'email':payload['email'],'password':payload['password']})
    assert login.status_code == 200
    data = login.json()['data']
    assert data['access_token'] and data['refresh_token']
    me = client.get('/users/me', headers={'Authorization': f"Bearer {data['access_token']}"})
    assert me.status_code == 200
    refresh = client.post('/auth/refresh', json={'refresh_token': data['refresh_token']})
    assert refresh.status_code == 200
