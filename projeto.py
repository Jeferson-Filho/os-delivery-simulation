# Projeto da Disciplina - Sistemas Operacionais I
    # Caio Bohlhalter de Souza
    # Jeferson Patrick Dietrich

import random
import sys
import threading
import time
from datetime import datetime
from queue import Queue

# Variável global para rastrear encomendas restantes
encomendas_restantes = 0
lock_encomendas = threading.Lock()


# Classe para representar uma encomenda
class Encomenda:
    def __init__(self, numero, ponto_origem, ponto_destino):
        self.numero = numero
        self.ponto_origem = ponto_origem
        self.ponto_destino = ponto_destino
        self.hora_chegada_origem = None
        self.hora_carregada = None
        self.veiculo = None  # Alterado de veiculo_id para veiculo
        self.hora_descarregada = None

    def registrar_encomenda(self):
        self.hora_chegada_origem = datetime.now()
        log = f"Encomenda {self.numero}: Chegada ao ponto de origem {self.ponto_origem} em {self.hora_chegada_origem}"
        print(log)
        with open(f"encomenda_N{self.numero}.txt", 'w') as file:
            file.write(log)

    def carregar(self, veiculo):
        self.hora_carregada = datetime.now()
        self.veiculo = veiculo  # Agora armazenando o objeto veiculo, não o id
        log = f"Encomenda {self.numero}: Carregada no veículo {veiculo.id} em {self.hora_carregada}"
        print(log)
        with open(f"encomenda_N{self.numero}.txt", 'a') as file:
            file.write("\n" + log)

    def descarregar(self):
        self.hora_descarregada = datetime.now()
        log = f"Encomenda {self.numero}: Descarregada no ponto de destino {self.ponto_destino} em {self.hora_descarregada}"
        print(log)
        with open(f"encomenda_N{self.numero}.txt", 'a') as file:
            file.write("\n" + log)


# Classe para representar um veículo
class Veiculo:
    def __init__(self, id_veiculo, capacidade, ponto_inicial):
        self.id = id_veiculo
        self.capacidade = capacidade
        self.carga = []
        self.ponto_atual = ponto_inicial

    def carregar(self, encomenda):
        if len(self.carga) < self.capacidade:
            self.carga.append(encomenda)
            encomenda.carregar(self)
            print(f"Veículo {self.id}: Carregou a encomenda {encomenda.numero} no ponto {self.ponto_atual}.")
            return True
        else:
            print(f"Veículo {self.id}: Capacidade máxima atingida.")
            return False

    def descarregar(self, ponto_atual):
        global encomendas_restantes
        descarregadas = [e for e in self.carga if e.ponto_destino == ponto_atual]
        for encomenda in descarregadas:
            self.carga.remove(encomenda)
            encomenda.descarregar()
            print(f"Veículo {self.id}: Descarregou a encomenda {encomenda.numero} no ponto {ponto_atual}.")
            # Atualizar contador de encomendas restantes
            with lock_encomendas:
                encomendas_restantes -= 1

    def viajar_para(self, proximo_ponto):
        tempo_viagem = random.uniform(0.5, 2.0)  # Tempo aleatório entre 0.5 e 2.0 segundos
        time.sleep(tempo_viagem)
        print(f"Veículo {self.id}: Viajou do ponto {self.ponto_atual} para o ponto {proximo_ponto} (tempo: {tempo_viagem:.2f}s).")
        self.ponto_atual = proximo_ponto


# Classe para representar um ponto de redistribuição de encomendas
class Redistribuicao:
    def __init__(self, id_ponto):
        self.id = id_ponto
        self.fila_encomendas = Queue()
        self.semaforo = threading.Semaphore(1)

    def adicionar_encomenda(self, encomenda):
        self.fila_encomendas.put(encomenda)
        print(f"Ponto {self.id}: Encomenda {encomenda.numero} adicionada à fila.")

    def processar_veiculo(self, veiculo):
        # Descarregar encomendas do veículo
        veiculo.descarregar(self.id)

        # Carregar encomendas no veículo
        while not self.fila_encomendas.empty() and len(veiculo.carga) < veiculo.capacidade:
            encomenda = self.fila_encomendas.get()
            if encomenda:
                veiculo.carregar(encomenda)

    def manutencao_fila(self, veiculo):
        # Aguarda o semáforo para ter acesso ao ponto
        self.semaforo.acquire()
        try:
            self.processar_veiculo(veiculo)
        finally:
            self.semaforo.release()


# Funções para threads
def thread_encomenda(encomenda, pontos):
    ponto_origem = pontos[encomenda.ponto_origem - 1]
    encomenda.registrar_encomenda()
    ponto_origem.adicionar_encomenda(encomenda)


def thread_veiculo(veiculo, pontos):
    global encomendas_restantes
    num_pontos = len(pontos)

    while True:
        # Verificar se ainda há encomendas na rede
        with lock_encomendas:
            if encomendas_restantes == 0:
                print(f"Veículo {veiculo.id}: Todas as encomendas foram entregues, parando operação.")
                break

        ponto = pontos[veiculo.ponto_atual]

        # Processar encomendas no ponto de redistribuição
        ponto.manutencao_fila(veiculo)

        # Avançar para o próximo ponto circularmente
        proximo_ponto = (veiculo.ponto_atual + 1) % num_pontos
        veiculo.viajar_para(proximo_ponto)


def thread_ponto(ponto, pontos):
    global encomendas_restantes
    while True:
        time.sleep(2)  # Intervalo de tempo para verificar a fila de encomendas

        # Verificar se ainda há encomendas restantes para processar
        with lock_encomendas:
            if encomendas_restantes == 0:
                print(f"Ponto {ponto.id}: Todas as encomendas entregues, encerrando.")
                break  # Interromper o loop da thread do ponto

        # Processar encomendas se houver
        if not ponto.fila_encomendas.empty():
            encomenda = ponto.fila_encomendas.queue[0]  # Pegando a encomenda
            if encomenda.veiculo:  # Verificando se o veículo da encomenda está atribuído
                veiculo = encomenda.veiculo
                print(f"Ponto {ponto.id}: Tentando atender o veículo {veiculo.id}...")
                ponto.manutencao_fila(veiculo)
            else:
                print(f"Ponto {ponto.id}: Nenhum veículo atribuído à encomenda {encomenda.numero}.")
        else:
            print(f"Ponto {ponto.id}: Nenhuma encomenda para processar.")


# Função principal
def main():
    global encomendas_restantes

    if len(sys.argv) != 5:
        print("Uso incorreto. O programa deve receber exatamente 4 argumentos.")
        print("Formato: python seu_script.py S C P A")
        return

    try:
        S = int(sys.argv[1])  # Número de pontos de redistribuição
        C = int(sys.argv[2])  # Número de veículos
        P = int(sys.argv[3])  # Número de encomendas
        A = int(sys.argv[4])  # Espaços de carga em cada veículo
    except ValueError:
        print("Todos os argumentos devem ser números inteiros.")
        return

    if not (P > A > C):
        print("Erro: A condição P > A > C não foi atendida.")
        print(f"Valores fornecidos: P = {P}, A = {A}, C = {C}")
        print("Garanta que: P (encomendas) > A (espaços de carga) > C (veículos).")
        return
    
    # Criando os pontos de redistribuição
    pontos = [Redistribuicao(i) for i in range(1, S + 1)]

    # Criando os veículos
    veiculos = [Veiculo(i, A, random.randint(0, S - 1)) for i in range(1, C + 1)]

    # Criando as encomendas
    encomendas = []
    for i in range(1, P + 1):
        ponto_origem = random.randint(1, S)
        ponto_destino = random.randint(1, S)
        while ponto_destino == ponto_origem:
            ponto_destino = random.randint(1, S)
        encomendas.append(Encomenda(i, ponto_origem, ponto_destino))
        encomendas_restantes = len(encomendas)


    # Iniciar threads para encomendas, veículos e pontos
    for encomenda in encomendas:
        threading.Thread(target=thread_encomenda, args=(encomenda, pontos)).start()

    for veiculo in veiculos:
        threading.Thread(target=thread_veiculo, args=(veiculo, pontos)).start()

    for ponto in pontos:
        threading.Thread(target=thread_ponto, args=(ponto, pontos)).start()

if __name__ == "__main__":
    main()