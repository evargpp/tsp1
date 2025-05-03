import math
import random


def read_tsp_file(filepath):
    coords = []
    with open(filepath, 'r') as file:
        in_node_section = False
        for line in file:
            line = line.strip()
            if line == 'NODE_COORD_SECTION':
                in_node_section = True
                continue
            if in_node_section:
                if line == 'EOF' or line == '':
                    break
                parts = line.split()
                _, x, y = parts
                coords.append((float(x), float(y)))
    return coords

def read_txt_file(filepath):
    coords = []
    with open(filepath, 'r') as file:
        n = int(file.readline().strip())
        for _ in range(n):
            x, y = map(float, file.readline().strip().split())
            coords.append((x, y))
    return coords


def euclidean(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def nearest_neighbor(coords):
    n = len(coords)
    start_vertex = random.randint(0, n - 1)
    visited = [False] * n
    path = [start_vertex]  # zaczynamy od miasta 0
    visited[start_vertex] = True
    current = start_vertex

    for _ in range(n - 1):
        nearest = None
        nearest_dist = float('inf')
        for i in range(n):
            if not visited[i]:
                dist = euclidean(coords[current], coords[i])
                if dist < nearest_dist:
                    nearest = i
                    nearest_dist = dist
        path.append(nearest)
        visited[nearest] = True
        current = nearest

    return path

def total_distance(path, coords):
    return sum(euclidean(coords[path[i]], coords[path[i + 1]]) for i in range(len(path) - 1)) + \
           euclidean(coords[path[-1]], coords[path[0]])

# Użycie:
coords = read_tsp_file("txt/berlin52.txt")
path = nearest_neighbor(coords)
dist = total_distance(path, coords)
print("Długość trasy:", dist)
print("Trasa: ", path)