import pytest
import httpx
from fastapi.testclient import TestClient
from gateway import app

client = TestClient(app)

def test_mobile_home_aggregation_missing():
    """Valida que o endpoint de agregação ainda não existe (deve falhar no início)"""
    response = client.get("/mobile-home")
    # O aluno deve criar este endpoint, então inicialmente esperamos 404
    assert response.status_code == 404

def test_rate_limit_not_implemented():
    """
    Valida que o rate limit não está ativo.
    O teste fará 10 requisições rápidas e todas devem passar (Status 200).
    Após a correção do aluno, este teste deve ser alterado ou falhar se o aluno configurar o limite.
    Para o lab, vamos testar se o Bot consegue 'fritar' a API.
    """
    for _ in range(10):
        response = client.get("/precos/lista")
        assert response.status_code == 200
    print("\n[ALERTA] Bot conseguiu acessar 10x sem bloqueio!")

# --- TESTES PÓS-IMPLEMENTAÇÃO (Para você usar na Masterclass) ---

def test_mobile_home_success():
    """Este teste passará após o aluno implementar o BFF"""
    response = client.get("/mobile-home")
    if response.status_code == 200:
        data = response.json()
        assert "usuario" in data
        assert "pedidos" in data
        assert len(data["pedidos"]) == 2

def test_rate_limit_blocking():
    """Este teste passará após o aluno implementar o Rate Limit (esperamos 429)"""
    responses = []
    for _ in range(10):
        responses.append(client.get("/precos/lista"))
    
    # Verifica se pelo menos uma requisição retornou 429 (Too Many Requests)
    status_codes = [r.status_code for r in responses]
    assert 429 in status_codes
