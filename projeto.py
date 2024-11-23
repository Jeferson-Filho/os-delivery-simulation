#Caio Bohlhalter de Souza
#Jeferson Patrick Dietrich
import random
import sys
import threading
import time
from datetime import datetime

# Classe para representar uma encomenda
class Encomenda:
    def __init__(self, numero, ponto_origem, ponto_destino):
        self.numero = numero
        self.ponto_origem = ponto_origem
        self.ponto_destino = ponto_destino
        self.hora_chegada_origem = None
        self.hora_carregada = None
        self.veiculo_id = None
        self.hora_descarregada = None
    
    def registrar_encomenda(self):
        self.hora_chegada_origem = datetime.now()
        log = f"Encomenda {self.numero}: Chegada ao ponto de origem {self.ponto_origem} em {self.hora_chegada_origem}"
        print(log)
        with open(f"encomenda_N{self.numero}.txt", 'w') as file:
            file.write(log)
    
    def carregar(self, veiculo_id):
        self.hora_carregada = datetime.now()
        self.veiculo_id = veiculo_id
        log = f"Encomenda {self.numero}: Carregada no veiculo {veiculo_id} em {self.hora_carregada}"
        print(log)
        with open(f"encomenda_N{self.numero}.txt", 'a') as file:
            file.write("\n" +log)
    
    def descarregar(self):
        self.hora_descarregada = datetime.now()
        log = f"Encomenda {self.numero}: Descarregada no ponto de destino {self.ponto_destino} em {self.hora_descarregada}"
        print(log)
        with open(f"encomenda_N{self.numero}.txt", 'a') as file:
            file.write("\n" + log)


# Funções para simular as operações de cada thread
def thread_encomenda(encomenda):
    # Registrando o ciclo da encomenda
    encomenda.registrar_encomenda()
    time.sleep(1)  # Simulando tempo de espera
    encomenda.carregar(encomenda.numero)  # Usando o número da encomenda como ID do veículo para simplicidade
    time.sleep(1)  # Simulando tempo de carregamento
    encomenda.descarregar()

def thread_veiculo():
    print("")

def thread_ponto():
    print("")

def main():
    # Verificando se o número correto de argumentos foi passado
    if len(sys.argv) != 5:
        print("Uso incorreto. O programa deve receber exatamente 4 argumentos.")
        print("Formato: python seu_script.py S C P A")
        return
    
    try:
        # Extraindo os argumentos e convertendo para inteiros
        S = int(sys.argv[1])  # Número de pontos de redistribuição
        C = int(sys.argv[2])  # Número de veículos
        P = int(sys.argv[3])  # Número de encomendas
        A = int(sys.argv[4])  # Espaços de carga em cada veículo
    except ValueError:
        print("Todos os argumentos devem ser numeros inteiros.")
        return
    
    # Verificando a condição P >> A >> C
    if not (P > A > C):
        print("A condicao P >> A >> C nao foi atendida.")
        return

    # Criando as encomendas
    encomendas = []
    for i in range(1, P + 1):
        ponto_origem = random.randint(1, S)
        ponto_destino = random.randint(1, S)
        while ponto_destino == ponto_origem:
            ponto_destino = random.randint(1, S)
        encomenda = Encomenda(i, ponto_origem, ponto_destino)
        encomendas.append(encomenda)

    # Criando e iniciando threads para encomendas
    encomenda_threads = []
    for encomenda in encomendas:
        t = threading.Thread(target=thread_encomenda, args=(encomenda,))
        encomenda_threads.append(t)
        t.start()

    # Criando e iniciando threads para veículos
    veiculo_threads = []
    for i in range(1, C + 1):
        t = threading.Thread(target=thread_veiculo, args=())
        veiculo_threads.append(t)
        t.start()

    # Criando e iniciando threads para pontos de redistribuição
    redistribuicao_threads = []
    for i in range(1, S + 1):
        t = threading.Thread(target=thread_ponto, args=())
        redistribuicao_threads.append(t)
        t.start()

    # Esperando as threads terminarem
    for t in encomenda_threads + veiculo_threads + redistribuicao_threads:
        t.join()

if __name__ == "__main__":
    main()

