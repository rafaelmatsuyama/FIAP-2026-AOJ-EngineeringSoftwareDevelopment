Feature: Resiliencia no Checkout

  Scenario: O Anti-Fraude está instável e deve falhar rápido
    Given que o serviço de Anti-Fraude está com latência de 10s
    When eu tento processar um pagamento de "R$ 100,00"
    Then o sistema deve responder em menos de 1.0s
    And deve retornar o status "ANALISE_MANUAL"
