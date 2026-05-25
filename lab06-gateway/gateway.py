from fastapi import FastAPI, Request
import time

app = FastAPI()

# MOCKS DE MICROSERVIÇOS INTERNOS (Simulando o Backend)
@app.get("/usuarios/me")
async def get_user():
    return {"id": 1, "nome": "Rafael Matsuyama", "perfil": "Premium"}

@app.get("/pedidos/recentes")
async def get_recent_orders():
    return {"itens": [{"id": 101, "total": 50.0}, {"id": 102, "total": 120.0}]}

# --- LAB 06: ENDPOINT VULNERÁVEL (BOT) ---
@app.get("/precos/lista")
async def listar_precos():
    # Atualmente sem Rate Limit! O aluno deverá proteger este endpoint.
    return {"precos": [10.0, 20.0, 30.0], "status": "desprotegido"}

# --- LAB 06: MISSÃO BFF (O aluno deve criar o /mobile-home) ---
# O aluno deverá implementar o endpoint agregador conforme o roteiro.
