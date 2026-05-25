import time

class PagamentoAPI:
    def cobrar(self, pedido_id, valor):
        print(f"   [API Pagamento] Cobrando R$ {valor} do pedido {pedido_id}... OK!")
        return {"status": "COBRADO"}

    def estornar(self, pedido_id, valor):
        print(f"   [API Pagamento] Realizando ESTORNO de R$ {valor} do pedido {pedido_id}... OK!")
        return {"status": "ESTORNADO"}

class EstoqueAPI:
    def reservar(self, pedido_id, produto_id):
        # SIMULAÇÃO DE ERRO: O estoque sempre falha para forçar a SAGA
        print(f"   [API Estoque] Tentando reservar produto {produto_id}... ERRO 500!")
        raise Exception("Serviço de Estoque Indisponível (Timeout)")

class OrquestradorSaga:
    def __init__(self):
        self.pagamento_api = PagamentoAPI()
        self.estoque_api = EstoqueAPI()

    def processar_pedido_completo(self, pedido_id, valor, produto_id):
        """
        LAB 05: CÓDIGO VULNERÁVEL
        Este método executa os passos, mas não tem inteligência para lidar com falhas parciais.
        Se o estoque falhar, o pagamento continuará cobrado (Inconsistência).
        """
        print(f"\n[SAGA] Iniciando processamento do pedido {pedido_id}...")
        
        # Passo 1: Cobrar
        self.pagamento_api.cobrar(pedido_id, valor)
        
        # Passo 2: Reservar Estoque (Este passo vai falhar lançando exceção)
        self.estoque_api.reservar(pedido_id, produto_id)
        
        return {"status": "SUCESSO_TOTAL"}
