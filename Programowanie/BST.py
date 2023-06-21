# Jakub Opyrchał (266252)
# Algorytmy i Struktury Danych
# 16.04.2023 r.
"""BST i przeszukiwanie binarne"""

import random
import time as tm
import matplotlib.pyplot as plot


class Node:
    """Definiuje strukture wezla"""
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


class BinarySearchTree:
    """Definiuje strukture drzewa i umozliwia insercje"""
    def __init__(self):
        self.root = None

    def insert(self, val):
        newNode = Node(val)
        if not self.root:
            self.root = newNode
            return

        currNode = self.root
        while True:
            if val < currNode.val:
                if currNode.left is None:
                    currNode.left = newNode
                    #print(newNode)
                    return
                currNode = currNode.left
            else:
                if currNode.right is None:
                    currNode.right = newNode
                    #print(newNode)
                    return
                currNode = currNode.right


# def Perform(num, bst):
#     """Wykonanie pojedynczego pomiaru"""
#     output = 1
#
#     start = tm.perf_counter_ns()
#     currNode = bst.root
#     while currNode:
#         if num == currNode.val:
#             if output == 1:
#                 print(f"Znaleziono {num}")
#             break
#         elif num < currNode.val:
#             currNode = currNode.left
#         else:
#             currNode = currNode.right
#     else:
#         # print(f"Nie znaleziono {num}")
#         pass
#     stop = tm.perf_counter_ns()
#     time = (stop - start)
#     return time


def timeTest(sampleSizes):
    """Seria pomiarow dla okreslonych rozmiarow probek"""
    debug = 0
    timeMeasure = []
    for sampleSize in sampleSizes:
        meanComponent = 0
        for j in range(100):
            nums = list(range(1, sampleSize + 1))
            random.shuffle(nums)
            bst = BinarySearchTree()    # Generowanie BST odbywa sie teraz w petli
            for num in nums:
                bst.insert(num)
            sampledNums = random.sample(nums, 10)
            start = tm.perf_counter_ns()
            for num in sampledNums:
                currNode = bst.root
                while currNode:
                    if num == currNode.val:
                        if debug == 1:
                            print(f"Znaleziono {num}")
                        break
                    elif num < currNode.val:
                        currNode = currNode.left
                    else:
                        currNode = currNode.right
                else:
                    print("FAILURE")
                    pass
                stop = tm.perf_counter_ns()
                time = (stop - start)
                meanComponent += time
        timeMeasure.append(meanComponent / 100)
    return timeMeasure


sampleSizes = [100, 500, 1000, 2000]
results = timeTest(sampleSizes)
print(results)

XP = sampleSizes
YP = results
plot.plot(XP, YP, label='Czas wykonania')
plot.xlabel('Rozmiar proby (n)')
plot.ylabel('Czas [ns]')
plot.legend()
plot.show()