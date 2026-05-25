Feature: Consistencia Eventual com SAGA

  Scenario: Falha no estoque deve disparar estorno do pagamento
    Given que o cliente deseja realizar um pedido de valor "100.00"
    When o orquestrador tenta processar o pedido completo
    Then o status final deve ser "CANCELADO_COM_ESTORNO"
