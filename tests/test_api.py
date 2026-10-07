from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'

def test_products_have_seed_data():
    response = client.get('/products')
    assert response.status_code == 200
    assert len(response.json()) >= 10

def test_semantic_search_returns_ranked_products():
    response = client.get('/search', params={'q': 'comfortable shoes for running'})
    assert response.status_code == 200
    assert response.json()['count'] > 0
    assert 'score' in response.json()['results'][0]

def test_recommendations_and_missing_product():
    assert client.get('/recommend/1').status_code == 200
    assert client.get('/recommend/99999').status_code == 404
