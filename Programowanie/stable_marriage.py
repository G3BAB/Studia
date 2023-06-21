class Graph:
    def __init__(self):
        self.graph = {}

    def addEdge(self, vertex, edge):
        if vertex not in self.graph:
            self.graph[vertex] = []
        self.graph[vertex].append(edge)


def stableMarriage(graph):
    preferences = {vertex: list(edges) for vertex, edges in graph.graph.items()}
    matching = {}

    for woman in preferences.keys():
        matching[woman] = None

    while None in matching.values():
        for woman in preferences.keys():
            if matching[woman] is None:
                man = preferences[woman].pop(0)
                if man not in matching.values():
                    matching[woman] = man

    return matching


def get_partner(matching, man):
    for woman, partner in matching.items():
        if partner == man:
            return woman
    return None


preferences = {
    'women': ["Krysia", "Gienia", "Janina", "Zygfryda", "Aurelia"],
    'men': ["Zygmunt", "Ferdek", "Andrzej", "Janusz", "Gienek"],

    'preferences': {
        "Krysia": ["Andrzej", "Janusz", "Ferdek", "Zygmunt"],
        "Gienia": ["Ferdek", "Zygmunt", "Janusz", "Andrzej"],
        "Janina": ["Ferdek", "Zygmunt", "Andrzej", "Janusz"],
        "Zygfryda": ["Andrzej", "Ferdek", "Janusz", "Zygmunt"],
        "Aurelia": ["Gienek", "Janusz", "Ferdek", "Zygmunt"]
    }
}


def createGraph(preferences):
    graph = Graph()

    for woman, men in preferences['preferences'].items():
        for man in men:
            graph.addEdge(woman, man)

    return graph


graph = createGraph(preferences)
matching = stableMarriage(graph)

print("Dopasowanie:")
print(matching)
for woman, man in matching.items():
    print(f"{woman} i {man}")
