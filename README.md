# Projeto da Disciplina - Sistemas Operacionais I

## **Descrição do Projeto**
Este projeto simula uma **rede de entregas concorrente** em que encomendas são transportadas por veículos entre pontos de redistribuição. A sincronização é feita utilizando **threads**, **semaforos** e **locks**. O objetivo principal é gerenciar o transporte de encomendas, assegurando que a condição `P > A > C` seja atendida, onde:
- `P` é o número de encomendas,
- `A` é a capacidade de carga dos veículos,
- `C` é o número de veículos,
- `S` é o número de pontos de redistribuição.

Os pontos de redistribuição servem como locais intermediários onde encomendas são organizadas em filas para serem carregadas pelos veículos. Os veículos percorrem esses pontos em ordem circular.

O programa implementa as funcionalidades de registro de rastros das encomendas, sincronização dos pontos de redistribuição e monitoramento do fluxo das operações.

---

## **Funcionalidades Implementadas**
1. **Gerenciamento de Encomendas:**
   - Cada encomenda é representada por uma instância da classe `Encomenda`.
   - Contém informações como número da encomenda, ponto de origem, ponto de destino e horários de chegada, carregamento e descarregamento.

2. **Veículos e Transporte:**
   - Cada veículo possui uma capacidade de carga (`A`) e move-se entre os pontos de redistribuição em ordem circular.
   - Veículos carregam encomendas disponíveis no ponto atual e descarregam no ponto de destino.

3. **Pontos de Redistribuição:**
   - Gerenciam filas de encomendas utilizando semáforos para garantir que apenas um veículo seja processado por vez.
   - Processam o carregamento e descarregamento de encomendas.
   - Atendem veículos que chegam aleatoriamente para gerenciar as filas de encomendas.

4. **Sincronização e Concorrência:**
   - Utiliza semáforos e locks para evitar condições de corrida.
   - As threads gerenciam encomendas, veículos e pontos de redistribuição.

5. **Gravação de Arquivos de Rastro:**
   - Cada encomenda gera um arquivo `encomenda_N{numero}.txt`, contendo:
     - Número da encomenda,
     - Ponto de origem e destino,
     - Horários de chegada, carregamento e descarregamento,
     - Identificador do veículo responsável.

---

## **Estrutura do Código**
### **Classes**
1. **`Encomenda`:**
   - Representa uma encomenda e seu ciclo de vida (chegada ao ponto de origem, carregamento e descarregamento).
   - Registra logs em arquivos individuais.

2. **`Veiculo`:**
   - Representa um veículo que transporta encomendas entre pontos.
   - Contém métodos para carregar, descarregar e viajar entre pontos.

3. **`Redistribuicao`:**
   - Representa um ponto de redistribuição com fila de encomendas.
   - Gerencia o acesso dos veículos e processa suas cargas/descargas usando semáforos.

### **Funções Principais**
1. **`thread_encomenda`:**
   - Gera uma thread para registrar e adicionar encomendas à fila do ponto de origem.

2. **`thread_veiculo`:**
   - Gera uma thread para gerenciar o ciclo de vida de um veículo:
     - Carregar encomendas disponíveis,
     - Descarregar encomendas no destino,
     - Circular entre os pontos.

3. **`thread_ponto`:**
   - Gera uma thread para monitorar as filas de um ponto de redistribuição e processar encomendas.

4. **`main`:**
   - Configura os parâmetros de entrada,
   - Gera objetos de encomendas, veículos e pontos,
   - Inicia as threads.

---

## **Execução do Programa**
### **Pré-requisitos**
- Python 3.x
- Sistema operacional compatível com threads (Linux, macOS ou Windows).

### **Instalação**
1. Clone o repositório do projeto:
   ```bash
   git clone https://github.com/seu-usuario/projeto-sistemas-operacionais.git
