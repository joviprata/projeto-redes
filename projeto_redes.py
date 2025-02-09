from collections import defaultdict, deque
from matplotlib import pylab as pl
import matplotlib.pyplot as plt
import networkx as nx


class Tree:
    def __init__(self):
        self.graph = defaultdict(list)
        self.ip_map = {}  # Armazena os endereços IP dos nós
        self.traceroute = []

    def add_edge(self, u, v, weight):
        # Define o estado de visita inicial do nó como False
        if u not in self.graph:
            self.graph[u] = [False]
        if v not in self.graph:
            self.graph[v] = [False]

        # Adiciona a aresta ao nó
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))

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
        
        for neighbor, _ in self.graph[no_atual][1:]:
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
            node, distance = queue.popleft()

            if node == y:
                return distance  # Encontramos Y, retornamos a distância

            for neighbor, weight in self.graph[node][1:]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, distance + weight))

        return -1  # Caso não encontre um caminho

    def assign_host_ips(self): 
        subnet_map = {}

        for node in self.graph:
            if node.startswith('h'): #verifica se é host
                for neighbor, _ in self.graph[node][1:]: #encontra roteador ao qual está conectado
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

"""
# Lendo as arestas
while True:
    try:
        line = input().strip()
        if not line:
            continue
        parts = line.split()

        if len(parts) == 3:  # Entrada de aresta (nó1 nó2 peso)
            u, v, weight = parts
            tree.add_edge(u, v, int(weight))
            grafo.add_edge(u, v, weight=int(weight))
        elif len(parts) == 2:  # Entrada de endereço IP (nó ip)
            node, ip = parts
            tree.add_ip(node, ip)
        else:
            # Últimos dois inputs são os nós X e Y
            x = parts[0]
            y = input().strip()
            break
    except EOFError:
        break
"""

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
distancia = tree.find_distance(x, y)

# Obtendo endereços IP
ip_x = tree.ip_map.get(x, "IP desconhecido")
ip_y = tree.ip_map.get(y, "IP desconhecido")

# Exibindo resultado
print(f"Endereço IP de {x}: {ip_x}")
print(f"Endereço IP de {y}: {ip_y}\n")
#print(traceroute)
print(f"Tempo de ping esperado: {distancia} ms.")
print(f"Rota realizada: {' -> '.join(traceroute) if traceroute else 'Caminho não encontrado'}")


pos = nx.spring_layout(grafo)
plt.figure(figsize=(10, 10))

# Desenhando o grafo
nx.draw(grafo, pos, with_labels=True, node_size=500, 
        node_color="skyblue", font_size=10, font_color="black", 
        font_weight="bold", arrows=True)
plt.show()