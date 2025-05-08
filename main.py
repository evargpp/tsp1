import math
import random
import matplotlib.pyplot as plt
import networkx as nx

def read_points_file(filepath):
    coords = []
    with open(filepath, 'r') as file:
        n = int(file.readline().strip())
        for _ in range(n):
            id, x, y = map(float, file.readline().strip().split())
            coords.append((x, y))
    return coords

def euclidean(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def build_graph(coords):
    G = nx.Graph()
    for i, coord in enumerate(coords):
        G.add_node(i, pos=coord)
    n = len(coords)
    for i in range(n):
        for j in range(i + 1, n):
            dist = euclidean(coords[i], coords[j])
            G.add_edge(i, j, weight=dist, pheromone=1.0)
    return G

def choose_next_node(G, current, visited, alpha=1.0, beta=2.0):
    neighbors = [(nbr, G[current][nbr]['pheromone'], G[current][nbr]['weight'])
                 for nbr in G.neighbors(current) if nbr not in visited]
    if not neighbors:
        return None

    # Probabilistyczny wybór na podstawie feromonu i odwrotności odległości
    total = sum((pheromone ** alpha) * ((1.0 / dist) ** beta) for _, pheromone, dist in neighbors)
    probabilities = [((pheromone ** alpha) * ((1.0 / dist) ** beta)) / total for _, pheromone, dist in neighbors]
    choices = [nbr for nbr, _, _ in neighbors]
    return random.choices(choices, weights=probabilities, k=1)[0]

def build_path(G, start):
    visited = {start}
    path = [start]
    current = start

    while len(visited) < len(G.nodes):
        next_node = choose_next_node(G, current, visited)
        if next_node is None:
            break
        path.append(next_node)
        visited.add(next_node)
        current = next_node

    return path

def total_path_length(G, path):
    dist = 0
    for i in range(len(path) - 1):
        dist += G[path[i]][path[i + 1]]['weight']
    dist += G[path[-1]][path[0]]['weight']  # powrót
    return dist

def update_pheromones(G, all_paths, evaporation=0.5, Q=100.0):
    # Parowanie feromonów
    for u, v in G.edges:
        G[u][v]['pheromone'] *= (1 - evaporation)

    # Dodanie nowego feromonu na podstawie jakości ścieżek
    for path, length in all_paths:
        contribution = Q / length
        for i in range(len(path)):
            u = path[i]
            v = path[(i + 1) % len(path)]
            if G.has_edge(u, v):
                G[u][v]['pheromone'] += contribution

def ant_colony_optimization(G, n_ants=20, n_iterations=100, alpha=1.0, beta=2.0, evaporation=0.5, Q=100.0):
    best_path = None
    best_length = float('inf')

    for iteration in range(n_iterations):
        all_paths = []
        for _ in range(n_ants):
            start = random.choice(list(G.nodes))
            path = build_path(G, start)
            if len(path) != len(G.nodes):
                continue  # ścieżka niepełna — pomijamy
            length = total_path_length(G, path)
            all_paths.append((path, length))
            if length < best_length:
                best_length = length
                best_path = path

        update_pheromones(G, all_paths, evaporation, Q)
        print(f"Iteracja {iteration+1}: najlepsza długość = {best_length:.2f}")
        draw_path(coords, best_path, f"Berlin52 iteracja: {iteration}", f"Berlin52-it {iteration}.png")

    return best_path, best_length

def draw_path(coords, path, title="Najlepsza trasa", save_to_file=None):
    x = [coords[i][0] for i in path] + [coords[path[0]][0]]
    y = [coords[i][1] for i in path] + [coords[path[0]][1]]

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'o-', color='blue')
    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    for i, idx in enumerate(path):
        plt.text(coords[idx][0], coords[idx][1], str(idx), fontsize=8)

    if save_to_file:
        plt.savefig(save_to_file, dpi=300)
        print(f"Zapisano wykres do pliku: {save_to_file}")
    else:
        plt.show()

    plt.close()  # ważne przy wielu wykresach – zwalnia pamięć

# Przykład użycia
coords = read_points_file("txt/berlin52.txt")
G = build_graph(coords)
best_path, best_dist = ant_colony_optimization(G, n_ants=30, n_iterations=30)
print("\nNajlepsza długość trasy:", best_dist)
print("Trasa (początek):", best_path[:10], "...")
# draw_path(coords, best_path)