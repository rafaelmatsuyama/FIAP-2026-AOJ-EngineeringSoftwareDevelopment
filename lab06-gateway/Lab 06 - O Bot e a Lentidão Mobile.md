# Lab Autoguiado: O Bot e a Lentidão Mobile (Gateway & BFF) 🌐

Neste laboratório, vamos resolver dois problemas clássicos de arquitetura usando um **API Gateway** com o padrão **BFF (Backend-For-Frontend)**:

1.  **O Problema do Mobile:** Para montar a tela inicial, o app mobile faz 3 chamadas HTTP separadas (`Perfil`, `Pedidos`, `Notificações`). Em redes 3G/4G, isso causa uma latência horrível e consome muita bateria.
2.  **O Problema do Bot:** Nossa API está sendo "bombardeada" por scripts que tentam ler dados de preços a cada milissegundo, sobrecarregando nossos microserviços de banco de dados.

Sua missão é transformar um servidor FastAPI básico em um Gateway inteligente que consolida dados e bloqueia abusos.

⏱️ **Tempo Estimado:** 20 minutos (Missão) + 10 minutos (Masterclass)

---

## 🎯 Objetivo Final
1.  Criar um endpoint único `/mobile-home` que faz a agregação de múltiplos serviços internamente.
2.  Habilitar um Middleware de **Rate Limit** para bloquear qualquer IP que tente fazer mais de 5 requisições por segundo.

**Critério de Sucesso:** Executar o teste de performance e ver que o Mobile agora recebe tudo em 1 chamada e o teste de "Bot" é bloqueado com erro 429 (Too Many Requests).

---

## 🗺️ Passo 1: O Cenário "Chato"
1. No seu Codespaces, navegue até a pasta do laboratório e garanta que as dependências de rede estejam instaladas:
   ```bash
   cd lab06-gateway
   pip install fastapi uvicorn httpx slowapi
   ```
2. Inicie o Gateway (que por enquanto não faz nada):
   ```bash
   uvicorn gateway:app --reload
   ```
3. Em outro terminal, rode o teste de reconhecimento:
   ```bash
   cd lab06-gateway
   pytest test_gateway.py -v
   ```
   *Você verá que o teste de agregação falha (404 Not Found) e o teste de segurança passa direto (o Bot consegue acessar tudo).*

---

## ✂️ Passo 2: Construindo o BFF (Agregação)
Abra o arquivo `gateway.py`. Vamos criar o endpoint que facilitará a vida do desenvolvedor mobile. 

**Copie e cole este Snippet para consolidar os dados:**

```python
import httpx

BASE_URL = "http://localhost:8000"

@app.get("/mobile-home")
async def bff_mobile_home():
    print("[GATEWAY] Consolidando dados para Mobile...")
    
    # Em um cenário real, estas seriam chamadas para Microserviços diferentes
    async with httpx.AsyncClient() as client:
        # Chamada 1: Dados do Usuário
        res_user = await client.get(f"{BASE_URL}/usuarios/me")
        # Chamada 2: Últimos Pedidos
        res_orders = await client.get(f"{BASE_URL}/pedidos/recentes")
        
    return {
        "usuario": res_user.json(),
        "pedidos": res_orders.json()["itens"],
        "timestamp_gateway": time.time()
    }
```

---

## 🛡️ Passo 3: Proteção de Borda (Rate Limit)
Agora, vamos impedir que o sistema seja derrubado por abusos. Vamos usar um middleware simples para limitar o tráfego.

**Adicione este bloco de configuração no seu `gateway.py`:**

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Agora, proteja o endpoint sensível de preços
@app.get("/precos/lista")
@limiter.limit("5/second") # Máximo de 5 chamadas por segundo por IP
async def listar_precos(request: Request):
    return {"precos": [10.0, 20.0, 30.0], "status": "protegido"}
```

---

## 🧪 Passo 4: Validação Final
Rode novamente os testes:
```bash
pytest test_gateway.py -v
```
**O que deve acontecer:**
1.  O teste do Mobile deve retornar **VERDE** (Recebeu o JSON consolidado).
2.  O teste do Bot deve retornar **VERDE** (Ele tentou 10 vezes seguidas e o Gateway bloqueou com Erro 429 na 6ª tentativa).

---
*Dica de Ouro: O Gateway é o "Segurancinha" e o "Concierge" do seu sistema. Ele decide quem entra e como a informação é entregue.*
