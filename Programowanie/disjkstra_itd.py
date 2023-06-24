import heapq
import random
import string
import time
import matplotlib.pyplot as plot


class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, source, destination, weight):
        if source not in self.graph:
            self.graph[source] = []
        if destination not in self.graph:
            self.graph[destination] = []

        self.graph[source].append((destination, weight))
        self.graph[destination].append((source, weight))


def randomGraph(numVertices, numEdges, weights=10):
    """Generates a random graph with 'numVertices' vertices and at least 'numEdges' edges.
       Ensures that:
       1. The graph has 'numVertices' vertices and a minimum of 'numEdges' edges.
       2. Vertex pairs are unique (no duplicate edges).
       3. All elements of the graph are connected, i.e., from any element, you can reach any other element."""

    def randomizer(nVertices, nEdges, weight_pool):
        rGraph = Graph()
        handled = []

        vertices = list(string.ascii_uppercase)[:nVertices]

        for i in range(nEdges):
            a = random.choice(vertices)
            b = random.choice(vertices)
            if a == b:
                nEdges += 1
            else:
                if [a, b] in handled or [b, a] in handled:
                    nEdges += 1
                else:
                    weight = random.randint(1, weight_pool)
                    rGraph.add_edge(a, b, weight)
                    handled.append([a, b])

        for i in range(nVertices):
            if [vertices[i], vertices[i]] not in handled:
                b = random.choice(vertices)
                weight = random.randint(1, weight_pool)
                rGraph.add_edge(vertices[i], b, weight)
                handled.append([vertices[i], b])

        return rGraph

    # Check connectivity to ensure a fully connected graph
    def dfs(graph, vertex, visited):
        visited.add(vertex)
        for neighbor, _ in graph[vertex]:
            if neighbor not in visited:
                dfs(graph, neighbor, visited)

    connectivityCheck = set()
    while len(connectivityCheck) != numVertices:
        potentialGraph = randomizer(numVertices, numEdges, weights)
        visited = set()
        dfs(potentialGraph.graph, 'A', visited)  # Start with 'A'
        connectivityCheck = visited

    return potentialGraph


def dijkstra(graph, source):
    distances = {vertex: float('inf') for vertex in graph}
    distances[source] = 0

    priority_queue = [(0, source)]
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, edge_weight in graph[current_vertex]:
            distance = current_distance + edge_weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances


def kruskal(graph):
    edges = []
    for vertex in graph.graph:  # Access the 'graph' attribute
        for neighbor, edge_weight in graph.graph[vertex]:  # Access the 'graph' attribute
            edges.append((edge_weight, vertex, neighbor))

    edges.sort()
    parent = {vertex: vertex for vertex in graph.graph}
    tree = []

    def find(parent, vertex):
        if parent[vertex] != vertex:
            parent[vertex] = find(parent, parent[vertex])
        return parent[vertex]

    def union(parent, rank, vertex1, vertex2):
        root1 = find(parent, vertex1)
        root2 = find(parent, vertex2)
        if rank[root1] < rank[root2]:
            parent[root1] = root2
        elif rank[root1] > rank[root2]:
            parent[root2] = root1
        else:
            parent[root2] = root1
            rank[root1] += 1

    rank = {vertex: 0 for vertex in graph.graph}
    for edge in edges:
        weight, vertex1, vertex2 = edge
        if find(parent, vertex1) != find(parent, vertex2):
            union(parent, rank, vertex1, vertex2)
            tree.append(edge)

    return tree


def prim(graph):
    tree = []
    visited = set()
    start_vertex = next(iter(graph.graph))  # Access the 'graph' attribute

    priority_queue = [(0, start_vertex)]
    while priority_queue:
        current_weight, current_vertex = heapq.heappop(priority_queue)
        if current_vertex in visited:
            continue
        visited.add(current_vertex)

        for neighbor, edge_weight in graph.graph[current_vertex]:  # Access the 'graph' attribute
            if neighbor not in visited:
                heapq.heappush(priority_queue, (edge_weight, neighbor))
                tree.append((current_vertex, neighbor, edge_weight))

    return tree


def time_measure():
    n_vector = [5, 10, 15, 20]
    results = [[], []]

    for element in n_vector:
        time_kruskal = 0
        time_prim = 0
        for i in range(1, 100):
            graph = randomGraph(element, element, element)
            start = time.perf_counter_ns()
            kruskal(graph)
            stop = time.perf_counter_ns()
            time_kruskal += (stop - start)

            start = time.perf_counter_ns()
            prim(graph)
            stop = time.perf_counter_ns()
            time_prim += (stop - start)

        results[0].append(time_kruskal / 100)
        results[1].append(time_prim / 100)

    return results


results = time_measure()


def plot_execution_time(results):
    n_vector = [5, 10, 15, 20]
    labels = ['Kruskal', 'Prim']

    for i, result in enumerate(results):
        plot.plot(n_vector, result, label=labels[i])

    plot.xlabel('Liczba węzłów')
    plot.ylabel('Czas wykonania [ns]')
    plot.title('Algorytm Prima i Kruskala - Porównanie')
    plot.legend()
    plot.grid(True)
    plot.show()


print(results)
plot_execution_time(results)


def calculate_shortest_routes(graph):
    shortest_routes = {}
    vertices = list(graph.graph.keys())

    for source in vertices:
        distances = dijkstra(graph.graph, source)
        for destination in vertices:
            if source != destination:
                shortest_routes[(source, destination)] = distances[destination]

    return shortest_routes


def display_shortest_routes(shortest_routes):
    print("Najkrótsze trasy:")
    for (source, destination), distance in shortest_routes.items():
        print(f"{source} - {destination}: {distance}")

graph = Graph()
graph.add_edge('A', 'G', 5)
graph.add_edge('A', 'B', 5)
graph.add_edge('B', 'G', 5)
graph.add_edge('G', 'F', 5)
graph.add_edge('F', 'E', 2)
graph.add_edge('E', 'D', 5)
graph.add_edge('D', 'C', 1)
graph.add_edge('C', 'B', 3)
graph.add_edge('D', 'G', 3)
graph.add_edge('D', 'B', 3)
graph.add_edge('D', 'F', 4)


shortest_routes = calculate_shortest_routes(graph)
display_shortest_routes(shortest_routes)