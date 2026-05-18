from pytest_bdd import scenarios, given, when, then, parsers
from src.calculadoras import CalculadoraDeEnergia

# Informa ao pytest-bdd onde está o arquivo de texto (Gherkin)
scenarios('../features/megazord.feature')

# GIVEN: O Setup (Estado inicial)
@given(parsers.parse('que o cliente é tipo "{tipo_cliente}"'), target_fixture="contexto")
def setup_cliente(tipo_cliente):
    # Passamos os dados via um dicionário que funciona como a "memória" do teste
    pass

@given(parsers.parse('a missão será na região "{regiao}"'))
def setup_regiao(contexto, regiao):
    pass

# WHEN: A Ação do Sistema
@when(parsers.parse('o Megazord calcular o custo de uma missão de valor {valor_base:d}'))
def acao_calcular(contexto, valor_base):
    # DICA: Instancie a CalculadoraDeEnergia aqui, chame o calcular_total
    # e salve o resultado dentro do "contexto", para que o THEN consiga validar.
    pass

# THEN: A Validação (Asserts)
@then(parsers.parse('o custo final de energia deve ser {valor_esperado:d}'))
def checar_resultado(contexto, valor_esperado):
    pass
