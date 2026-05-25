# Lab Autoguiado: O Dinheiro Preso & A Transação Compensatória (SAGA) 🔄

Neste laboratório, você vai lidar com o pesadelo do e-commerce: a quebra de consistência. Em um banco de dados relacional (Monolito), usamos o **Commit/Rollback** para garantir que tudo ocorra ou nada ocorra (ACID). Em Sistemas Distribuídos, isso não é possível. 

Nosso fluxo de `Checkout` aprova o pagamento via API de Cartão, mas o serviço de `Estoque` está instável e rejeita a reserva do produto (Erro 500). O resultado? O cliente pagou e não vai receber nada.

Sua missão é implementar a lógica de **Transação Compensatória** (SAGA). Se um passo falhar, o sistema deve orquestrar a reversão dos passos anteriores que já haviam dado certo.

⏱️ **Tempo Estimado:** 20 minutos (Missão) + 10 minutos (Masterclass)

---

## 🎯 Objetivo Final
Refatorar o serviço de Orquestração de Pedidos implementando um bloco `try/except` que, ao detectar a falha no Estoque, dispare automaticamente uma requisição para a API de **Estorno de Pagamento**.

**Critério de Sucesso:** Executar os testes automatizados e garantir que o status do pedido termine em "CANCELADO_COM_ESTORNO".

---

## 🗺️ Passo 1: Reconhecimento do Desastre
1. No seu Codespaces, navegue até a pasta do laboratório:
   ```bash
   cd lab05-saga
   ```
2. Rode os testes e analise o desastre:
   ```bash
   pytest test_saga.py -v
   ```
   *O teste vai falhar alertando que o pedido ficou "PRESO" (Cobrado, mas sem estoque). É o fim do mundo para o atendimento ao cliente.*

---

## ✂️ Passo 2: A Orquestração de Resgate (SAGA)
Abra o arquivo `saga_service.py`. Você verá a classe `OrquestradorSaga` e a função vulnerável `processar_pedido_completo`.

A função atual simplesmente "morre" ao levantar a exceção do Estoque, largando o pagamento processado. Vamos consertar isso.

**Substitua o conteúdo da função `processar_pedido_completo` por este Snippet:**

```python
    def processar_pedido_completo(self, pedido_id, valor, produto_id):
        print(f"\n[SAGA] Iniciando processamento do pedido {pedido_id}...")
        
        # Passo 1: Cobrar o Cliente
        # Se falhar aqui, não tem problema, o fluxo para.
        self.pagamento_api.cobrar(pedido_id, valor)
        
        # Passo 2: Tentar reservar o Estoque
        try:
            # O estoque é instável e vai falhar!
            self.estoque_api.reservar(pedido_id, produto_id)
            return {"status": "SUCESSO_TOTAL"}
            
        except Exception as e:
            print(f"[SAGA] Falha Crítica no Estoque detectada: {e}")
            print(f"[SAGA] Iniciando Transação Compensatória (Rollback)...")
            
            # --- O CORAÇÃO DO SAGA ---
            # Como falhou no passo 2, DEVEMOS desfazer o passo 1.
            resultado_estorno = self.pagamento_api.estornar(pedido_id, valor)
            
            if resultado_estorno["status"] == "ESTORNADO":
                return {"status": "CANCELADO_COM_ESTORNO", "motivo": "Falta de estoque"}
            else:
                # O Pior Cenário: O estorno também falhou!
                # Isso requer intervenção humana imediata (Dead Letter Queue/Alertas)
                return {"status": "INCONSISTENTE_FATAL", "motivo": "Falha no estorno"}
```

---

## 🧪 Passo 3: Validação da Compensação
Rode novamente o teste para validar a consistência eventual:
```bash
pytest test_saga.py -v
```
**O que deve acontecer:** O teste deve retornar **VERDE**. O log mostrará claramente a tentativa de reserva de estoque falhando e a SAGA imediatamente acionando o método de estorno para devolver o dinheiro do cliente.

---
*Dica de Ouro: Em Microserviços, você deve assumir que os serviços VÃO falhar. Seu design não deve tentar impedir a falha, mas sim gerenciar a recuperação do estado (Eventual Consistency).*
