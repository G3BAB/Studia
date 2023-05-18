import random


class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, a, b):
        if a in self.graph:
            self.graph[a].append(b)
        else:
            self.graph[a] = [b]


def randomGraph(nVertices, nEdges):
    graph = Graph()

    for i in range(nEdges):
        a = random.randint(0, nVertices - 1)
        b = random.randint(0, nVertices - 1)
        graph.add_edge(a, b)

    return graph

