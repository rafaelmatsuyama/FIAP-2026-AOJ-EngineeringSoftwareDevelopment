import time
import requests

class CheckoutService:
    def __init__(self, antifraude_url="http://localhost:8080/v1/validar"):
        self.antifraude_url = antifraude_url

    def processar_pagamento(self, transacao):
        """
        LAB 04: CÓDIGO VULNERÁVEL
        Atualmente, este método não possui proteção contra latência de rede.
        Se o serviço de Anti-Fraude demorar, esta thread ficará travada.
        """
        try:
            # O aluno verá que este requests sem timeout adequado é o culpado
            response = requests.get(self.antifraude_url, timeout=30)
            return response.json()
        except Exception as e:
            print(f"Erro na transação: {e}")
            raise e
