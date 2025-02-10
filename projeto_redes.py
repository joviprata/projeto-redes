from collections import defaultdict, deque
from matplotlib import pylab as pl
import matplotlib.pyplot as plt
import networkx as nx


class Tree:
    def __init__(self):
        self.graph = defaultdict(list)
        self.ip_map = {}  # Armazena os endereços IP dos nós
        self.traceroute = []
        self.speed_map = { #velocidade do meio físico (km/s)
            "fibra": 200000,
            "coaxial": 100000,
            "par_trancado": 50000,
        }
        self.base_latencia = {
            "fibra": 5e-3,
            "coaxial": 2e-3,
            "par_trancado": 1e-3,
        }
    def cable_type_def(self, u, v):
        if u.startswith('h') or v.startswith('h'):
            return "par_trancado" 
        elif u.startswith('e') or v.startswith('e'):
            return "coaxial"
        else:
            return "fibra"

    def real_distance_def(self, tipo_cabo):
        if tipo_cabo == "fibra":
            return 10000 #simula link transoceânico
        elif tipo_cabo == "coaxial":
            return 200 #simula link de longa distância
        else:
            return 100 #simula conexões residenciais
        return 10
    
    def add_edge(self, u, v, weight=None):
        tipo_cabo = self.cable_type_def(u, v)
        # Define o estado de visita inicial do nó como False

        if weight is None:
            weight = self.real_distance_def(tipo_cabo)

        if u not in self.graph:
            self.graph[u] = [False]
        if v not in self.graph:
            self.graph[v] = [False]

        # Adiciona a aresta ao nó
        self.graph[u].append((v, int(weight), tipo_cabo))
        self.graph[v].append((u, int(weight), tipo_cabo))
    

    def add_ip(self, node, ip):
        self.ip_map[node] = ip

    def set_nodes_visited(self):
        for node in self.graph:
            node[0] = False

    def find_traceroute(self, no_atual, no_destino, path=None):
        if path is None:
            path = []
        
        path.append(no_atual)
        self.graph[no_atual][0] = True

        if no_atual == no_destino:
            return path
        
        for neighbor, _, tipo_cabo in self.graph[no_atual][1:]:
            if not self.graph[neighbor][0]:
                result = self.find_traceroute(neighbor, no_destino, path[:])
                if result:
                    return result
            
        return None


    def find_distance(self, x, y):
        queue = deque([(x, 0)])  # (nó atual, distância acumulada)
        visited = set()
        visited.add(x)

        while queue:
            node, tempo_acumulado = queue.popleft()

            if node == y:
                return tempo_acumulado  

            for neighbor, distancia, tipo_cabo in self.graph[node][1:]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    velocidade = self.speed_map[tipo_cabo]
                    tempo_transmissao = distancia / velocidade
                    latencia_adicional= self.base_latencia[tipo_cabo] #latencia adicional do meio físico e equipamento
                    queue.append((neighbor, tempo_acumulado + tempo_transmissao + latencia_adicional))

        return -1  # Caso não encontre um caminho

    def assign_host_ips(self): 
        subnet_map = {}

        for node in self.graph:
            if node.startswith('h'): #verifica se é host
                for neighbor, _, _ in self.graph[node][1:]: #encontra roteador ao qual está conectado
                    if neighbor in self.ip_map: #verifica se vizinho tem ip
                        base_ip = self.ip_map[neighbor].rsplit('.', 1)[0] #pega o ip do roteador e sua sub-red
                        if neighbor not in subnet_map:
                            subnet_map[neighbor]= 1
                        else:
                            subnet_map[neighbor] += 1
                        
                        host_ip=f"{base_ip}.{subnet_map[neighbor]}"
                        self.add_ip(node, host_ip)


# Criando a árvore
tree = Tree()

grafo = nx.Graph()

def le_arquivo(arquivo):
    with open(arquivo, 'r') as f:
        for line in f:
            parts = line.split()

            if len(parts) == 3:  # Entrada de aresta (nó1 nó2 peso)
                u, v, weight = parts
                tree.add_edge(u, v, int(weight))
                grafo.add_edge(u, v, weight=int(weight))
            elif len(parts) == 2:  # Entrada de endereço IP (nó ip)
                node, ip = parts
                tree.add_ip(node, ip)


# Lendo arquivo
le_arquivo('exemplo-de-input.txt')

#adiciona ips aos hosts
tree.assign_host_ips()

# Adiciona origem e destino
x = input("Digite o nó de origem: ").strip()
y = input("Digite o nó de destino: ").strip()

# Calculando a distância entre X e Y
#ping, traceroute = tree.find_distance(x, y)
traceroute = tree.find_traceroute(x, y)
tempo_ping = tree.find_distance(x, y)

# Obtendo endereços IP
ip_x = tree.ip_map.get(x, "IP desconhecido")
ip_y = tree.ip_map.get(y, "IP desconhecido")

# Exibindo resultado
print(f"Endereço IP de {x}: {ip_x}")
print(f"Endereço IP de {y}: {ip_y}\n")
#print(traceroute)
print(f"Tempo de ping esperado: {tempo_ping:.6f} s")

if traceroute:
    caminho = []
    for i in range(len(traceroute) - 1):
        u, v = traceroute[i], traceroute[i + 1]
        for vizinho, _, tipo_cabo in tree.graph[u][1:]:
            if vizinho == v:
                caminho.append(f"{u} -({tipo_cabo})-> {v}")
                break
    print(f"Rota realizada: {' -> '.join(caminho)}")
else:
    print("Caminho não encontrado")

def desenhar_topologia():
    pos = nx.spring_layout(grafo)
    plt.figure(figsize=(10, 10))

    cabos_cores = {"fibra": "blue", "coaxial": "red", "par_trancado": "green"}
    cores= []

    for u,v in grafo.edges():
        tipo_cabo = tree.cable_type_def(u, v)
        cores.append(cabos_cores[tipo_cabo])

    # Desenhando o grafo
    nx.draw(grafo, pos, with_labels=True, node_size=500, 
            node_color="skyblue", font_size=10, font_color="black", 
            font_weight="bold", arrows=True, edge_color=cores)
    plt.show()



desenhar_topologia()
