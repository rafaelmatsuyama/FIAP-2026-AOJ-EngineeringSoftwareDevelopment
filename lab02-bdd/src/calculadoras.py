from abc import ABC, abstractmethod

# --- ESTRATÉGIAS DE DESCONTO ---
class CalculadoraDesconto(ABC):
    @abstractmethod
    def calcular(self, valor: float) -> float: pass

class DescontoVIP(CalculadoraDesconto):
    def calcular(self, valor: float) -> float: return valor * 0.85

class DescontoPremium(CalculadoraDesconto):
    def calcular(self, valor: float) -> float: return valor * 0.90

class DescontoComum(CalculadoraDesconto):
    def calcular(self, valor: float) -> float: return valor * 0.95

# --- ESTRATÉGIAS DE FRETE ---
class CalculadoraFrete(ABC):
    @abstractmethod
    def calcular(self) -> float: pass

class FreteNorte(CalculadoraFrete):
    def calcular(self) -> float: return 50.0

class FreteNordeste(CalculadoraFrete):
    def calcular(self) -> float: return 40.0

class FreteSul(CalculadoraFrete):
    def calcular(self) -> float: return 30.0

class FretePadrao(CalculadoraFrete):
    def calcular(self) -> float: return 20.0

# --- CLASSE PRINCIPAL REFATORADA ---
class CalculadoraDeEnergia:
    def calcular_total(self, valor_base: float, tipo_cliente: str, regiao: str) -> float:
        estrategias_desconto = {
            "vip": DescontoVIP(),
            "premium": DescontoPremium(),
            "comum": DescontoComum()
        }
        
        estrategias_frete = {
            "norte": FreteNorte(),
            "nordeste": FreteNordeste(),
            "sul": FreteSul()
        }

        estrategia_desconto = estrategias_desconto.get(tipo_cliente, DescontoComum())
        estrategia_frete = estrategias_frete.get(regiao, FretePadrao())
        
        valor_com_desconto = estrategia_desconto.calcular(valor_base)
        valor_frete = estrategia_frete.calcular()
        
        return valor_com_desconto + valor_frete
