import pytest
from pytest_bdd import scenario, given, when, then, parsers
from saga_service import OrquestradorSaga

@scenario('saga.feature', 'Falha no estoque deve disparar estorno do pagamento')
def test_compensacao_saga():
    pass

@pytest.fixture
def orquestrador():
    return OrquestradorSaga()

@given('que o cliente deseja realizar um pedido de valor "100.00"', target_fixture="dados_pedido")
def setup_pedido():
    return {"pedido_id": "ORD-123", "valor": 100.00, "produto_id": "PROD-99"}

@when('o orquestrador tenta processar o pedido completo', target_fixture="resultado")
def processar_pedido(orquestrador, dados_pedido):
    try:
        res = orquestrador.processar_pedido_completo(
            dados_pedido["pedido_id"], 
            dados_pedido["valor"], 
            dados_pedido["produto_id"]
        )
        return res
    except Exception as e:
        # Se o aluno não capturou o erro, o teste recebe a exceção
        return {"status": "ERRO_NAO_TRATADO", "msg": str(e)}

@then(parsers.parse('o status final deve ser "{status_esperado}"'))
def validar_status_final(resultado, status_esperado):
    assert resultado["status"] == status_esperado, f"Esperava {status_esperado} mas obteve {resultado['status']}"
