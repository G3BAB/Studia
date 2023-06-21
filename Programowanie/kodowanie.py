
class Node:
    def __init__(self, qty, symbol, left, right):
        self.qty = qty
        self.symbol = symbol
        self.left = None
        self.right = None
        self.code = ''


def Count(text):
    symbols = {}
    for i in text:
        if i in symbols:
            symbols[i] += 1
        else:
            symbols[i] = 1
    return symbols

def Encode(symbols):
    nodes = []
    for symbol, qty in symbols.items():
        nodes.append(Node(qty, symbol, None, None))

    while len(nodes) > 1:
        min1, min2 = Node(float('inf'), None, None, None), Node(float('inf'), None, None, None)
        for node in nodes:
            if node.qty < min1.qty:
                min2 = min1
                min1 = node
            elif node.qty < min2.qty:
                min2 = node

        parent = Node(min1.qty + min2.qty, None, min1, min2)

        nodes.remove(min1)
        nodes.remove(min2)
        nodes.append(parent)

    root = nodes[0]

    def assign_code(node, code):
        if node is None:
            return
        node.code = code
        assign_code(node.left, code + '0')
        assign_code(node.right, code + '1')

    assign_code(root, '')

    codes = {}
    for symbol, node in symbols.items():
        print(node.code)
        codes[symbol] = node.code

    return codes



def Decode(string):
    return string


String = "Hello World!"
symbols = Count(String)
codes = Encode(symbols)
print(symbols)
print(codes)
