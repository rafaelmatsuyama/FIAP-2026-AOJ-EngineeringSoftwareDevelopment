import pytest
from fastapi.testclient import TestClient
from gateway import app

client = TestClient(app)

def test_mobile_home_aggregation_missing():
    """ESTADO INICIAL: O endpoint ainda não existe"""
    response = client.get("/mobile-home")
    assert response.status_code == 404, "O endpoint /mobile-home já existe? Deveria ser criado pelo aluno."

def test_rate_limit_not_implemented():
    """ESTADO INICIAL: O Bot consegue acessar tudo"""
    for _ in range(10):
        response = client.get("/precos/lista")
        assert response.status_code == 200
    print("\n[ALERTA] Bot conseguiu acessar 10x sem bloqueio!")

# --- TESTES DE MISSÃO (Vão falhar até o aluno implementar) ---

def test_mobile_home_success():
    """MISSÃO: O aluno deve implementar o BFF e retornar 200"""
    response = client.get("/mobile-home")
    assert response.status_code == 200, "ERRO: O endpoint /mobile-home ainda retorna 404 ou erro."
    
    data = response.json()
    assert "usuario" in data, "Faltando dados do usuário no BFF"
    assert "pedidos" in data, "Faltando dados de pedidos no BFF"
    assert len(data["pedidos"]) == 2

def test_rate_limit_blocking():
    """MISSÃO: O aluno deve configurar o Rate Limit para retornar 429"""
    status_codes = []
    for _ in range(10):
        status_codes.append(client.get("/precos/lista").status_code)
    
    # Após a implementação, esperamos que o status 429 apareça na lista
    assert 429 in status_codes, f"ERRO: O Gateway não bloqueou o Bot. Status recebidos: {status_codes}"
