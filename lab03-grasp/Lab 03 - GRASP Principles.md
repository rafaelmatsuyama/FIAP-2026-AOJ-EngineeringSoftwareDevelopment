# Lab Autoguiado: Missão GRASP & A Taverna Anêmica 🗡️

Neste laboratório, você analisará o código de uma Taverna de RPG. Infelizmente, o sistema atual foi construído usando o anti-padrão **Modelo de Domínio Anêmico**.

Isso significa que as nossas classes base (como `ItemInventario` e `Inventario`) são apenas "sacos de dados" (só têm variáveis, não têm inteligência). Todo o cálculo matemático pesado está sendo feito por um bisbilhoteiro chamado `TaverneiroService`, que rouba os dados das outras classes para fazer o trabalho delas.

Sua missão é dar poder de volta às classes base, aplicando os princípios **GRASP** (General Responsibility Assignment Software Patterns), focando em **Information Expert** (Especialista da Informação) e **Creator** (Criador).

⏱️ **Tempo Estimado:** 30 minutos

---

## 🎯 Objetivo Final
Refatorar a classe `TaverneiroService` movendo as lógicas de cálculo para o local correto (as classes de domínio), removendo o vício de criar classes "Service" gigantescas, sem quebrar os testes automatizados já existentes.

**Critério de Sucesso:** Executar o comando `pytest` no terminal e obter **100% de sucesso (Verde)** após todas as refatorações.

---

## 🗺️ Passo 1: Acesso, Setup e Reconhecimento
1. No seu Codespaces, abra um Terminal (`Ctrl+J` ou `Cmd+J`) e navegue até a pasta do laboratório:
   ```bash
   cd lab03-grasp
   ```
2. Abra o arquivo `taverna.py` e leia o código. Observe o problema:
   * A classe `Inventario` tem apenas uma lista vazia.
   * A classe `TaverneiroService` faz **tudo**: ela entra na lista do Inventario, puxa cada `Item`, lê o preço, calcula a soma e retorna. Isso fere o isolamento.
3. Rode os testes para garantir que o sistema está rodando (um deles, o do desafio, vai falhar propositalmente, ignore-o por agora):
   ```bash
   pytest test_taverna.py -v
   ```
   *Verde no teste principal? Então prepare sua espada, vamos refatorar.*

---

## ✂️ Passo 2: Information Expert (O Especialista)
O princípio GRASP "Information Expert" diz: *"A responsabilidade de calcular algo deve pertencer à classe que possui as informações necessárias para esse cálculo"*.

Quem possui a lista de itens? A classe `Inventario`. Então é ela quem deve saber o valor total, e não o `TaverneiroService`.

**1. Mova a inteligência para o Inventário:**
Abra o arquivo `taverna.py`. Adicione o método de cálculo dentro da classe `Inventario`:
```python
class Inventario:
    def __init__(self):
        self.itens = []
    
    # NOVA FUNÇÃO (Transferida do Service para cá)
    def calcular_valor_total(self) -> float:
        total = 0.0
        for item in self.itens:
            total += item.preco
        return total
```

**2. Remova a inteligência do Service:**
No `TaverneiroService`, apague a lógica longa do método `calcular_total_mochila` e apenas delegue (chame a função) para o inventário:
```python
class TaverneiroService:
    def calcular_total_mochila(self, inventario: Inventario) -> float:
        # O Taverneiro não faz mais a conta na mão, ele só pergunta pro Inventário!
        return inventario.calcular_valor_total()
```

Rode o `pytest`. Continuou verde no teste principal? Você acabou de aplicar o Especialista da Informação! O Service ficou mais magro e o Domínio mais inteligente.

---

## 🧩 Passo 3: Creator (O Criador)
O princípio "Creator" diz: *"Se a classe B contém ou agrega instâncias da classe A, a classe B deve ser a responsável por criar instâncias de A"*.

No momento, o `TaverneiroService` cria a poção e joga dentro da mochila. O Inventário deveria ser o responsável por criar os itens que guarda.

**1. Adicione a criação no Inventário:**
```python
class Inventario:
    # ... código anterior mantido ...

    # NOVA FUNÇÃO: O Inventário assume a criação (Creator)
    def adicionar_novo_item(self, nome: str, preco: float):
        novo_item = ItemInventario(nome, preco)
        self.itens.append(novo_item)
```

**2. Simplifique o Service:**
Agora, o Service não precisa importar ou instanciar `ItemInventario`. Ele apenas envia ordens. Modifique o método `vender_pocao`:
```python
class TaverneiroService:
    def vender_pocao(self, inventario: Inventario):
        print("Taverneiro: 'Aqui está sua poção, forasteiro!'")
        # Delega a criação para o próprio Inventario
        inventario.adicionar_novo_item("Poção de Cura", 50.0)
```

Rode o `pytest`. Se o teste principal estiver verde, parabéns. Seu Domínio não é mais anêmico!

---

## 🚀 Passo 4: O Desafio Prático (A Taxa Mágica)
O Rei implementou um novo imposto de Guilda na Taverna: *"Todos os itens mágicos comprados devem pagar 10% a mais na hora do cálculo do valor total. Itens mágicos são todos aqueles cujo nome começa com a palavra 'Poção'."*

Como o `Inventario` agora é o Especialista da Informação do cálculo:
1. Modifique a função `calcular_valor_total` que você criou dentro da classe `Inventario`.
2. Se o `item.nome` começar com "Poção", o valor somado dele deve ser `item.preco * 1.10`.
3. O teste `test_taxa_magica` está atualmente falhando no `pytest`. 
4. Corrija a matemática até ficar 100% verde!

*Tente fazer sozinho! Se ficar travado, role a página para ver o Gabarito.*

<br><br><br><br><br><br><br><br><br><br>

---

## 🟢 GABARITO: Passo 4

Na classe `Inventario`, a lógica da taxa mágica fica totalmente isolada:

```python
class Inventario:
    def __init__(self):
        self.itens = []
    
    def adicionar_novo_item(self, nome: str, preco: float):
        novo_item = ItemInventario(nome, preco)
        self.itens.append(novo_item)

    # Gabarito da alteração da Taxa Mágica
    def calcular_valor_total(self) -> float:
        total = 0.0
        for item in self.itens:
            if item.nome.startswith("Poção"):
                total += (item.preco * 1.10) # 10% de imposto
            else:
                total += item.preco
        return total
```
*(Nota: Graças ao GRASP, nós não precisamos mexer em absolutamente NADA na classe `TaverneiroService` para adicionar esse novo imposto de cálculo!)*

---

### 🧠 Bônus: Pergunta Reflexiva para os Sobreviventes

Olhe para o seu código do Passo 4 no Gabarito. Nós injetamos um `if item.nome.startswith("Poção")` diretamente dentro do cálculo do `Inventario`. 

**A Pergunta:** Existe a possibilidade de refatorar o código desse novo imposto para ser mais modular e extensível no futuro, sem ferir o GRASP ou o SOLID?

**A Dica 💡:** Lembra de como resolvemos o pesadelo de `if`s no Lab 01 (Thunder Megazord)? Se o "Imposto" for uma regra complexa que muda com frequência, que tal aplicar o **Strategy Pattern** para os impostos, ou usar o princípio GRASP **Polymorphism**? E se cada item soubesse dizer se é tributável ou não, usando o próprio Information Expert?
