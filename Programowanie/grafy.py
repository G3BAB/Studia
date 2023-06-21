# Jakub Opyrchał (266252)
# LAB 18.05.2023
# Algorytmy i Struktury Danych
from collections import deque
import random


class Graph:
    def __init__(self):
        self.graph = {}

    def addEdge(self, vertex, edge):
        if vertex not in self.graph:
            self.graph[vertex] = []
        self.graph[vertex].append(edge)

    def getPreferences(self, vertex):
        if vertex in self.graph:
            return self.graph[vertex]
        return []


def dfs(graph, start):
    visitOrder = []

    def dfsVisit(handledGraph, vertex, visit):
        visit.add(vertex)
        nonlocal visitOrder
        visitOrder.append(vertex)

        if vertex in handledGraph:
            for neighbor in handledGraph[vertex]:
                if neighbor not in visit:
                    dfsVisit(handledGraph, neighbor, visit)
    visited = set()
    dfsVisit(graph, start, visited)

    return visitOrder


def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visitOrder = []

    while queue:
        vertex = queue.popleft()
        if vertex not in visited:
            visitOrder.append(vertex)
            visited.add(vertex)

            if vertex in graph:
                for neighbor in graph[vertex]:
                    if neighbor not in visited:
                        queue.append(neighbor)

    return visitOrder


def randomGraph(numVertices, numEdges):
    """Zawiła i niezgrabna funkcja generująca losowy graf, która zapewnia że:
        1. graf ma 'a' węzłów i minimum 'b' krawędzi,
        2. pary węzłów się nie powtarzają,
        3. wszystkie elementy grafu są połączone, tj. z dowolnego
           elementu można dostać się pośrednio do każdego innego"""

    def randomizer(nVertices, nEdges):
        rGraph = Graph()
        handled = []

        vertices = list(range(1, nVertices + 1))

        for i in range(nEdges):
            a = random.choice(vertices)
            b = random.choice(vertices)
            if a == b:
                nEdges += 1
            else:
                if [a, b] in handled or [b, a] in handled:
                    nEdges += 1
                else:
                    rGraph.addEdge(a, b)
                    handled.append([a, b])

        for i in range(nVertices):
            if i not in handled:
                b = random.choice(vertices)
                rGraph.addEdge(i, b)
                handled.append([i, b])

        # print(handled)
        return rGraph

    # mało eleganckie podejście 'brute force' żeby dostać w pełni połączony graf
    # (powoduje to, że generowanie grafów a > 20 jest niepraktyczne)

    connectivityCheck = []
    while connectivityCheck != numVertices:
        potentialGraph = randomizer(numVertices, numEdges)
        result = dfs(potentialGraph.graph, 1)
        connectivityCheck = len(result)

    return potentialGraph


def stable_marriage(males, females):
    unengaged_males = set(males.keys())
    engagements = {}

    while unengaged_males:
        male = unengaged_males.pop()
        preferences = males[male].copy()

        for female in preferences:
            if female not in engagements:
                engagements[female] = male
                break
            else:
                current_engagement = engagements[female]
                female_preferences = females[female]

                if female_preferences.index(male) < female_preferences.index(current_engagement):
                    engagements[female] = male
                    unengaged_males.add(current_engagement)
                    break

    return engagements


males = {
    'Janusz': ['Danuta', 'Gienia', 'Stasia', 'Judyta'],
    'Stanisław': ['Gienia', 'Stasia', 'Danuta', 'Judyta'],
    'Gienio': ['Judyta', 'Stasia', 'Gienia', 'Danuta'],
    'Kazimierz': ['Stasia', 'Danuta', 'Gienia', 'Judyta']
}

females = {
    'Danuta': ['Stanisław', 'Janusz', 'Gienio', 'Kazimierz'],
    'Judyta': ['Kazimierz', 'Gienio', 'Stanisław', 'Janusz'],
    'Gienia': ['Janusz', 'Stanisław', 'Gienio', 'Kazimierz'],
    'Stasia': ['Gienio', 'Janusz', 'Stanisław', 'Kazimierz']
}

engagements = stable_marriage(males, females)

for female, male in engagements.items():
    print(f"{male} engaged to {female}")
