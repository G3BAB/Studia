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

    potentialGraph = None

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
    def dfs(input_graph, vertex, is_visited):
        is_visited.add(vertex)
        for neighbor, _ in input_graph[vertex]:
            if neighbor not in is_visited:
                dfs(input_graph, neighbor, is_visited)

    connectivityCheck = set()
    while len(connectivityCheck) != numVertices:
        potentialGraph = randomizer(numVertices, numEdges, weights)
        visited = set()
        dfs(potentialGraph.graph, 'A', visited)
        connectivityCheck = visited

    return potentialGraph


def dijkstra(input_graph, source):
    distances = {vertex: float('inf') for vertex in input_graph}
    distances[source] = 0

    priority_queue = [(0, source)]
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, edge_weight in input_graph[current_vertex]:
            distance = current_distance + edge_weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances


def kruskal(input_graph):
    edges = []
    for vertex in input_graph.graph:
        for neighbor, edge_weight in input_graph.graph[vertex]:
            edges.append((edge_weight, vertex, neighbor))

    edges.sort()
    parent = {vertex: vertex for vertex in input_graph.graph}
    tree = []

    def find(input_parent, input_vertex):
        if input_parent[input_vertex] != input_vertex:
            input_parent[input_vertex] = find(input_parent, input_parent[input_vertex])
        return input_parent[input_vertex]

    def union(input_parent, input_rank, vert_1, vert_2):
        root1 = find(input_parent, vert_1)
        root2 = find(input_parent, vert_2)
        if input_rank[root1] < input_rank[root2]:
            input_parent[root1] = root2
        elif input_rank[root1] > input_rank[root2]:
            input_parent[root2] = root1
        else:
            input_parent[root2] = root1
            rank[root1] += 1

    rank = {vertex: 0 for vertex in input_graph.graph}
    for edge in edges:
        weight, vertex1, vertex2 = edge
        if find(parent, vertex1) != find(parent, vertex2):
            union(parent, rank, vertex1, vertex2)
            tree.append(edge)

    return tree


def prim(input_graph):
    tree = []
    visited = set()
    start_vertex = next(iter(input_graph.graph))

    priority_queue = [(0, start_vertex)]
    while priority_queue:
        current_weight, current_vertex = heapq.heappop(priority_queue)
        if current_vertex in visited:
            continue
        visited.add(current_vertex)

        for neighbor, edge_weight in input_graph.graph[current_vertex]:
            if neighbor not in visited:
                heapq.heappush(priority_queue, (edge_weight, neighbor))
                tree.append((current_vertex, neighbor, edge_weight))

    return tree


def time_measure():
    n_vector = [5, 10, 15, 20]
    time_results = [[], []]

    for element in n_vector:
        time_kruskal = 0
        time_prim = 0
        for i in range(1, 100):
            rand_graph = randomGraph(element, element, element)
            start = time.perf_counter_ns()
            kruskal(rand_graph)
            stop = time.perf_counter_ns()
            time_kruskal += (stop - start)

            start = time.perf_counter_ns()
            prim(rand_graph)
            stop = time.perf_counter_ns()
            time_prim += (stop - start)

        time_results[0].append(time_kruskal / 100)
        time_results[1].append(time_prim / 100)

    return time_results


results = time_measure()


def plot_execution_time(input_results):
    n_vector = [5, 10, 15, 20]
    labels = ['Kruskal', 'Prim']

    for i, input_results in enumerate(input_results):
        plot.plot(n_vector, input_results, label=labels[i])

    plot.xlabel('Liczba węzłów')
    plot.ylabel('Czas wykonania [ns]')
    plot.title('Algorytm Prima i Kruskala - Porównanie')
    plot.legend()
    plot.grid(True)
    plot.show()


print(results)
plot_execution_time(results)


def calculate_shortest_routes(input_graph):
    routes = {}
    vertices = list(input_graph.graph.keys())

    for source in vertices:
        distances = dijkstra(input_graph.graph, source)
        for destination in vertices:
            if source != destination:
                routes[(source, destination)] = distances[destination]

    return routes


def display_shortest_routes(route_results):
    print("Najkrótsze trasy:")
    for (source, destination), distance in route_results.items():
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
