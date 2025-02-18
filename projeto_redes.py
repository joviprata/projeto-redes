from collections import defaultdict, deque
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

class Tree:
    def __init__(self):
        self.graph = defaultdict(list)
        self.ip_map = {}
        self.speed_map = {
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
        return {"fibra": 10000, "coaxial": 200, "par_trancado": 100}.get(tipo_cabo, 10)

    def add_edge(self, u, v, weight=None):
        tipo_cabo = self.cable_type_def(u, v)
        if weight is None:
            weight = self.real_distance_def(tipo_cabo)
        self.graph[u].append((v, int(weight), tipo_cabo))
        self.graph[v].append((u, int(weight), tipo_cabo))

    def add_ip(self, node, ip):
        self.ip_map[node] = ip

    def find_all_paths(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        paths = []
        for neighbor, _, _ in self.graph[start]:
            if neighbor not in path:
                new_paths = self.find_all_paths(neighbor, end, path)
                for p in new_paths:
                    paths.append(p)
        return paths

    def calculate_all_paths(self):
        nodes = list(self.graph.keys())
        all_paths = {}
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                start, end = nodes[i], nodes[j]
                paths = self.find_all_paths(start, end)
                if paths:
                    all_paths[(start, end)] = paths
        return all_paths

    def dijkstra(self, start):
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for neighbor, weight, tipo_cabo in self.graph[node]:
                velocidade = self.speed_map[tipo_cabo]
                latencia = weight / velocidade + self.base_latencia[tipo_cabo]
                if distances[node] + latencia < distances[neighbor]:
                    distances[neighbor] = distances[node] + latencia
                    queue.append(neighbor)
        return distances

tree = Tree()
grafo = nx.Graph()

def le_arquivo(arquivo):
    with open(arquivo, 'r') as f:
        for line in f:
            parts = line.split()
            if len(parts) == 3:
                u, v, weight = parts
                tree.add_edge(u, v, int(weight))
                grafo.add_edge(u, v, weight=int(weight))
            elif len(parts) == 2:
                node, ip = parts
                tree.add_ip(node, ip)

le_arquivo('exemplo-de-input.txt')
all_paths = tree.calculate_all_paths()

for (start, end), paths in all_paths.items():
    print(f"Caminhos de {start} para {end}:")
    for path in paths:
        print(" -> ".join(path))

# Ajustando layout para melhor organização
pos = nx.kamada_kawai_layout(grafo)  # Layout mais estável e organizado

# Definição de cores conforme o tipo de cabo
cabos_cores = {"fibra": "blue", "coaxial": "red", "par_trancado": "green"}
cores_arestas = [cabos_cores[tree.cable_type_def(u, v)] for u, v in grafo.edges()]

# Identificar nós folhas
nos_folhas = [node for node in grafo.nodes() if len(tree.graph[node]) == 1]

# Definição de cores dos nós
cores_nos = ["lightgreen" if node in nos_folhas else "skyblue" for node in grafo.nodes()]

# Mapear os rótulos dos nós para os endereços IP
rotulos_nos = {node: tree.ip_map.get(node, node) for node in grafo.nodes()}

# Desenha o layout do grafo corrigido
plt.figure(figsize=(10, 10))
nx.draw(
    grafo, pos, labels=rotulos_nos, with_labels=True, node_size=500, node_color=cores_nos, 
    font_size=10, font_color="black", font_weight="bold", arrows=True, edge_color=cores_arestas
)
plt.savefig('grafo_resultante.png', transparent=False, facecolor='w')
print("\nGrafo resultante:")
plt.show()

# Criar tabela de Dijkstra
todos_nos = list(tree.graph.keys())
dijkstra_tabela = pd.DataFrame(index=todos_nos, columns=todos_nos)
for node in todos_nos:
    distancias = tree.dijkstra(node)
    for destino, tempo in distancias.items():
        dijkstra_tabela.at[node, destino] = round(tempo, 6)

# Salvar tabela em CSV
dijkstra_tabela.to_csv('dijkstra_tabela.csv')

print("\nTabela de tempos de ping (Dijkstra):")
display(dijkstra_tabela)
