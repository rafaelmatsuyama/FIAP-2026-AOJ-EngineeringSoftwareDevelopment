# Lab Autoguiado: A Queda em Cascata & O Escudo de Resiliência 🛡️

Neste laboratório, você enfrentará um dos problemas mais comuns em Sistemas Distribuídos: a **Falha em Cascata**. 

Nosso serviço de `Checkout` depende de um serviço externo de `AntiFraude`. O problema é que a rede não é confiável e a API de Anti-Fraude começou a apresentar latências altíssimas (10 segundos por chamada). Sem proteção, o nosso sistema "trava" esperando a resposta, esgotando a memória e derrubando o servidor para todos os outros clientes.

Sua missão é implementar o padrão **Circuit Breaker** (Disjuntor) para "falhar rápido" e proteger os recursos do nosso sistema, garantindo uma resposta de **Fallback** amigável para o usuário.

⏱️ **Tempo Estimado:** 20 minutos (Missão) + 10 minutos (Masterclass)

---

## 🎯 Objetivo Final
Implementar a biblioteca `tenacity` para envelopar chamadas instáveis, configurando limites de tentativa (Retries) e uma rota de fuga (Fallback) que evite o travamento total da aplicação.

**Critério de Sucesso:** Executar os testes e garantir que o sistema responda em menos de 1 segundo, mesmo quando o Anti-Fraude estiver lento.

---

## 🗺️ Passo 1: O Caos Instalado
1. No seu Codespaces, navegue até a pasta do laboratório:
   ```bash
   cd labs/lab04-resiliencia
   ```
2. Tente rodar o teste de stress e observe a demora (o terminal vai parecer travado):
   ```bash
   pytest test_checkout.py -v
   ```
   *Sentiu o lag? Isso acontece porque o `requests.get` está esperando 10s por cada transação. Se tivermos 100 clientes, o sistema morre.*

---

## 🛠️ Passo 2: Instalando o Escudo (Tenacity)
O `tenacity` é uma biblioteca Python poderosa para gerenciar retries e comportamentos de falha.
Certifique-se de que ela está instalada:
```bash
pip install tenacity
```

---

## ✂️ Passo 3: Implementando o Circuit Breaker
Abra o arquivo `checkout_service.py`. Você verá que a função `processar_pagamento` é vulnerável. Vamos protegê-la.

**1. Prepare o Código de Socorro (Fallback):**
Adicione este método na classe `CheckoutService`. Ele será chamado quando o sistema desistir de esperar o Anti-Fraude:
```python
def fallback_seguro(self, retry_state):
    print("!!! ALERTA: Anti-Fraude instável. Acionando Fallback de Segurança !!!")
    return {
        "status": "ANALISE_MANUAL", 
        "codigo": 202,
        "mensagem": "Pagamento recebido. Aguarde análise manual devido à instabilidade técnica."
    }
```

**2. Configure o Disjuntor (Decorator):**
Importe as ferramentas e decore a função principal. Copie e cole este Snippet sobre a função original:
```python
from tenacity import retry, stop_after_attempt, wait_fixed

class CheckoutService:
    # O decorator abaixo gerencia as tentativas e a falha
    @retry(
        stop=stop_after_attempt(3), # Tenta apenas 3 vezes
        wait=wait_fixed(0.1),        # Espera só 100ms entre elas
        retry_error_callback=fallback_seguro # Se falhar tudo, chama o socorro
    )
    def processar_pagamento(self, transacao):
        # IMPORTANTE: Adicione um timeout curto no requests para não travar a thread!
        response = requests.get("http://api-antifraude:8080/v1/validar", timeout=0.5)
        return response.json()
```

---

## 🧪 Passo 4: Validação em Tempo Real
Rode novamente o teste:
```bash
pytest test_checkout.py -v
```
**O que deve acontecer:** O teste deve passar **IMEDIATAMENTE** (em milissegundos). Você verá no log a mensagem do seu Fallback. O sistema não travou; ele apenas tomou uma decisão de negócio alternativa diante da falha técnica.

---
*Dica de Ouro: Sistemas Distribuídos saudáveis preferem uma Resposta Rápida (mesmo que incompleta) a um Silêncio Eterno.*
