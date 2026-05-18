# Lab Autoguiado: Missão BDD (Documentação Viva) 🥒

No laboratório anterior, você aplicou SOLID e transformou o *Thunder Megazord* em um conjunto de calculadoras elegantes. Agora, o time de Negócios (P.O.s e Analistas) quer entender e validar se o sistema realmente funciona como esperado, sem precisar ler código Python.

Sua missão é implementar **Testes Ágeis** utilizando **BDD (Behavior-Driven Development)**, criando uma ponte entre o inglês (ou português) estruturado do Negócio e o seu código Python.

⏱️ **Tempo Estimado:** 30 minutos

---

## 🎯 Objetivo Final
Fazer com que os cenários de negócio descritos no arquivo de especificação (`.feature`) sejam lidos e executados automaticamente pelo sistema de testes, validando as calculadoras do Megazord.

**Critério de Sucesso:** Executar o comando `pytest` e ver todos os cenários Gherkin passarem com sucesso (Verde).

---

## 🗺️ Passo 1: Acesso e Setup
1. Retorne ao seu GitHub Codespaces (ou abra novamente caso tenha fechado).
2. Abra um Terminal (`Ctrl+J` ou `Cmd+J`) e navegue para a pasta do segundo laboratório:
   ```bash
   cd lab02-bdd
   ```
3. O ambiente de testes com BDD (`pytest-bdd`) já está instalado. Tente rodar os testes agora:
   ```bash
   pytest -v
   ```
   *Você verá erros informando que os "Steps" (Passos) não foram encontrados. Isso é normal, é exatamente o que vamos construir.*

---

## 📖 Passo 2: Entendendo a Linguagem de Negócios (Gherkin)
1. No explorador de arquivos, abra a pasta `features/` e clique no arquivo `megazord.feature`.
2. Leia o conteúdo. Observe como ele usa o formato estruturado: **Dado (Given) / Quando (When) / Então (Then)**.
3. Não altere nada nesse arquivo por enquanto. Entenda que esse texto é a nossa **Regra de Negócio** documentada.

---

## 🔗 Passo 3: Criando a "Cola" (Steps)
Nós precisamos dizer ao Python o que fazer quando ele ler a frase `Dado que o cliente é VIP`.

1. Abra o arquivo `tests/test_megazord_steps.py`.
2. Você verá funções Python vazias. Preencha-as copiando e colando os decoradores que "escutam" as frases do arquivo Gherkin:

```python
from pytest_bdd import scenarios, given, when, then, parsers
from src.calculadoras import CalculadoraDeEnergia

# Informa ao pytest-bdd onde está o arquivo de texto
scenarios('../features/megazord.feature')

# GIVEN: O Setup (Estado inicial)
@given(parsers.parse('que o cliente é tipo "{tipo_cliente}"'), target_fixture="contexto")
def setup_cliente(tipo_cliente):
    # Passamos os dados via um dicionário que funciona como a "memória" do teste
    return {"tipo_cliente": tipo_cliente}

@given(parsers.parse('a missão será na região "{regiao}"'))
def setup_regiao(contexto, regiao):
    contexto["regiao"] = regiao

# WHEN: A Ação do Sistema
@when(parsers.parse('o Megazord calcular o custo de uma missão de valor {valor_base:d}'))
def acao_calcular(contexto, valor_base):
    calculadora = CalculadoraDeEnergia()
    # Executa a nossa classe refatorada do Lab 01
    contexto["custo_final"] = calculadora.calcular_total(
        valor_base, 
        contexto["tipo_cliente"], 
        contexto["regiao"]
    )

# THEN: A Validação (Asserts)
@then(parsers.parse('o custo final de energia deve ser {valor_esperado:d}'))
def checar_resultado(contexto, valor_esperado):
    assert contexto["custo_final"] == valor_esperado
```

3. Volte ao terminal e execute novamente:
   ```bash
   pytest -v
   ```
   *Tudo verde? Parabéns, você acabou de automatizar um critério de aceite de negócio!*

---

## 🚀 Passo 4: O Desafio Prático (O P.O. ligou...)
O Product Owner acabou de criar uma nova regra de negócio: *"Se o cliente for da lista de **inadimplentes**, ele não tem desconto nenhum (paga 100%). O frete para eles na região **norte** custa o dobro da tabela normal (100 de frete)."*

Siga o ciclo BDD:
1. Abra o arquivo `features/megazord.feature` e crie um novo `Scenario` com essa história, usando a exata mesma estrutura de frases do cenário anterior.
2. Rode o `pytest`. Ele deve falhar (Cenário quebra).
3. Abra o arquivo `src/calculadoras.py` e adicione essa nova regra de negócio nas nossas Estratégias (Factories).
4. Rode o `pytest`. Ficou verde? Missão cumprida!

*Tente fazer sozinho! Se ficar travado, role a página para ver o Gabarito.*

<br><br><br><br><br><br><br><br><br><br>

---

## 🟢 GABARITO: Passo 4

**1. A Regra de Negócio (Em `features/megazord.feature`):**
```gherkin
  Scenario: Inadimplente na região Norte paga mais caro
    Given que o cliente é tipo "inadimplente"
    And a missão será na região "norte"
    When o Megazord calcular o custo de uma missão de valor 100
    Then o custo final de energia deve ser 200
```
*(Valor 100 base + 0% de desconto = 100. Mais 100 de frete norte = 200 total)*

**2. A Refatoração do Código (Em `src/calculadoras.py`):**
No final do arquivo, adicione as novas regras e atualize os dicionários das factories:

```python
# Adicione a estratégia do cliente inadimplente
class DescontoInadimplente(CalculadoraDesconto):
    def calcular(self, valor: float) -> float: 
        return valor * 1.00 # Paga 100%, sem desconto

# Adicione a regra de frete punitivo
class FreteNorteInadimplente(CalculadoraFrete):
    def calcular(self) -> float: 
        return 100.0 # O dobro do normal (50.0)

# ATUALIZE o método calcular_total na classe CalculadoraDeEnergia
class CalculadoraDeEnergia:
    def calcular_total(self, valor_base: float, tipo_cliente: str, regiao: str) -> float:
        
        estrategias_desconto = {
            "vip": DescontoVIP(),
            "premium": DescontoPremium(),
            "comum": DescontoComum(),
            "inadimplente": DescontoInadimplente() # Nova Regra
        }
        
        estrategias_frete = {
            "norte": FreteNorte(),
            "nordeste": FreteNordeste(),
            "sul": FreteSul()
        }

        # Nova Regra Composta: Inadimplente no Norte
        if tipo_cliente == "inadimplente" and regiao == "norte":
            estrategia_frete = FreteNorteInadimplente()
        else:
            estrategia_frete = estrategias_frete.get(regiao, FretePadrao())

        estrategia_desconto = estrategias_desconto.get(tipo_cliente, DescontoComum())
        
        valor_com_desconto = estrategia_desconto.calcular(valor_base)
        valor_frete = estrategia_frete.calcular()
        
        return valor_com_desconto + valor_frete
```

Execute o `pytest` e veja o poder de uma documentação viva validando seu código!
