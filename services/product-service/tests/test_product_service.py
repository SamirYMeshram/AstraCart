from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)
def test_health(): assert client.get('/health').status_code == 200
def test_categories_endpoint(): assert client.get('/categories').status_code == 200
def test_product_create_and_search_requires_seller_or_admin_headers():
    cat = client.post('/categories', json={'name':'Test Gear','slug':'test-gear','description':'Testing','icon':'Test'}, headers={'X-User-Role':'ADMIN','X-User-Id':'admin'}).json()['data']
    product = {'title':'Test Product Pro','slug':'test-product-pro','description':'A complete product for integration tests','price':99.9,'stock_quantity':10,'category_id':cat['id'],'seller_id':'seller','images':[],'rating':4.8,'sku':'TEST-PRO-1'}
    r = client.post('/products', json=product, headers={'X-User-Role':'SELLER','X-User-Id':'seller'})
    assert r.status_code == 201
    s = client.get('/products/search?q=Test')
    assert s.status_code == 200 and s.json()['data']
