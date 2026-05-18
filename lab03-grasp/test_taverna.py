import pytest
from taverna import TaverneiroService, Inventario, ItemInventario

def test_venda_de_itens_simples():
    mochila = Inventario()
    servico = TaverneiroService()
    
    servico.vender_pocao(mochila)
    servico.vender_espada(mochila)
    
    # Valida se os itens entraram no inventario
    assert len(mochila.itens) == 2
    
    # Valida o cálculo total base
    total = servico.calcular_total_mochila(mochila)
    assert total == 200.0  # 50.0 da Poção + 150.0 da Espada

def test_taxa_magica_desafio_final():
    mochila = Inventario()
    servico = TaverneiroService()
    
    servico.vender_pocao(mochila) # 50.0 + 10% = 55.0
    servico.vender_espada(mochila) # 150.0 (sem taxa)
    
    # O total deve ser 205.0 peças de ouro, mas o código legado não tem a taxa.
    total = servico.calcular_total_mochila(mochila)
    assert total == 205.0, "O desafio da Taxa Mágica (10% na Poção) ainda não foi implementado!"
