import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_api_online(client):
    """Testa se a página do Swagger (documentação) está respondendo"""
    resposta = client.get('/apidocs/')
    assert resposta.status_code == 200

def test_historico_online(client):
    """Testa se a rota de histórico do banco de dados está online"""
    resposta = client.get('/history')
    assert resposta.status_code == 200