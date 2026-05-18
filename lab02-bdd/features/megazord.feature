Feature: Cálculo de Energia do Megazord (Descontos e Fretes)

  Scenario: VIP da região Sul pede equipamentos pesados
    Given que o cliente é tipo "vip"
    And a missão será na região "sul"
    When o Megazord calcular o custo de uma missão de valor 100
    Then o custo final de energia deve ser 115
