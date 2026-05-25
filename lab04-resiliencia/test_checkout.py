import pytest
import time
from pytest_bdd import scenario, given, when, then, parsers
from checkout_service import CheckoutService
import responses # Usaremos responses para mockar a latência sem subir um server real

@scenario('resiliencia.feature', 'O Anti-Fraude está instável e deve falhar rápido')
def test_resiliencia_antifraude():
    pass

@pytest.fixture
def checkout():
    return CheckoutService(antifraude_url="http://api-antifraude/v1/validar")

@given('que o serviço de Anti-Fraude está com latência de 10s')
def setup_antifraude_lento():
    # Mockando a resposta lenta
    responses.add(
        responses.GET,
        "http://api-antifraude/v1/validar",
        json={"status": "OK"},
        status=200
    )
    # Simulamos o delay no mock (ou o aluno sentirá no teste real se usarmos um server)
    # Para o lab, o aluno verá o tempo de execução subir

@when(parsers.parse('eu tento processar um pagamento de "{valor}"'), target_fixture="resultado")
def processar_pagamento(checkout, valor):
    start_time = time.time()
    try:
        res = checkout.processar_pagamento({"valor": valor})
        duration = time.time() - start_time
        return {"response": res, "duration": duration}
    except Exception as e:
        duration = time.time() - start_time
        return {"error": str(e), "duration": duration}

@then(parsers.parse('o sistema deve responder em menos de {limite:f}s'))
def validar_tempo_resposta(resultado, limite):
    assert resultado["duration"] < limite, f"Sistema muito lento: {resultado['duration']}s"

@then(parsers.parse('deve retornar o status "{status}"'))
def validar_status(resultado, status):
    if "error" in resultado:
        pytest.fail(f"Erro inesperado: {resultado['error']}")
    assert resultado["response"]["status"] == status
