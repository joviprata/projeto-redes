from collections import defaultdict, deque
from matplotlib import pylab as pl
import matplotlib.pyplot as plt
import networkx as nx


class Tree:
    def __init__(self):
        self.graph = defaultdict(list)
        self.ip_map = {}  # Armazena os endereços IP dos nós

    def add_edge(self, u, v, weight):
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))

    def add_ip(self, node, ip):
        self.ip_map[node] = ip

    def find_distance(self, x, y):
        queue = deque([(x, 0)])  # (nó atual, distância acumulada)
        visited = set()
        visited.add(x)

        while queue:
            node, distance = queue.popleft()

            if node == y:
                return distance  # Encontramos Y, retornamos a distância

            for neighbor, weight in self.graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, distance + weight))

        return -1  # Caso não encontre um caminho

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

# Adiciona origem e destino
x = input().strip()
y = input().strip()

# Calculando a distância entre X e Y
distance = tree.find_distance(x, y)

# Obtendo endereços IP
ip_x = tree.ip_map.get(x, "IP desconhecido")
ip_y = tree.ip_map.get(y, "IP desconhecido")

# Exibindo resultado
print(f"Tempo de ping esperado: {distance} ms.")
print(f"Endereço IP de {x}: {ip_x}")
print(f"Endereço IP de {y}: {ip_y}\n")










pos = nx.spring_layout(grafo)
plt.figure(figsize=(10, 10))

# Desenhando o grafo
nx.draw(grafo, pos, with_labels=True, node_size=500, 
        node_color="skyblue", font_size=10, font_color="black", 
        font_weight="bold", arrows=True)
plt.show()

