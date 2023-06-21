import numpy as np
import time as tm
import matplotlib.pyplot as plot

def heapSort(arr):
    length = len(arr)

    for i in range(length // 2 - 1, -1, -1):
        arr2heap(arr, length, i)

    for i in range(length - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        length = length - 1
        arr2heap(arr, length, 0)

    return arr


def arr2heap(arr, length, i):
    lChild = 2 * i + 1
    rChild = 2 * i + 2
    top = i

    if lChild < length and arr[lChild] < arr[top]:
        top = lChild

    if rChild < length and arr[rChild] < arr[top]:
        top = rChild

    if top != i:
        arr[i], arr[top] = arr[top], arr[i]
        arr2heap(arr, length, top)



def timeKeep(func, tSet, label):
    """Wykonuje pojedynczy pomiar"""
    start = tm.perf_counter_ns()
    temp = func(tSet)
    stop = tm.perf_counter_ns()
    time = (stop - start)
    #print("{}{}{}{}".format(label, " posortowany: ", func(tSet), "\n"))
    return time


def timeTest(func, set, label):
    """Przeprowadza serie pomiarow"""
    timeMeasure = [0, 0, 0, 0, 0]
    testedFunction = func
    meanComponent = 0
     #print('{}{}'.format("SET: ", set))
    for i in range(len(n)):
        for j in range(100):
            meanComponent += timeKeep(testedFunction, set[i], label)
        timeMeasure[i] = meanComponent / 100
    # print(timeMeasure)
    return timeMeasure


def scorePlot(score, n, tag):
    """Tworzy ploty dla poszczegolnych algorytmow"""
    XP = n
    YP = score
    print(score)
    plot.plot(XP, YP, label=tag)


n = [0, 100, 500, 1000, 2000]
labels = ["Heap Sort"]

# GENEROWANIE WYNIKOW
testSet = [[]] * len(n)
for i in range(len(n)):
    testSet[i] = np.random.randint(0, 5000, n[i])
scores = [timeTest(heapSort, testSet, labels[0])]

for i in range(len(n)):
    testSet[i] = heapSort(testSet[i])
scoresOptim = [timeTest(heapSort, testSet, labels[0])]

for i in range(len(n)):
    testSet[i] = sorted(testSet[i], reverse=True)
scoresPess = [timeTest(heapSort, testSet, labels[0])]


# PLOT
for i in range(0, 1):
    scorePlot(scores[i], n, labels[i])

plot.xlabel('Rozmiar proby (n)')
plot.ylabel('Czas [ns]')
plot.legend()
plot.show()
for i in range(0, 1):
    plot.plot(n, scores[i], label='Losowy')
    plot.plot(n, scoresPess[i], label='Pesymistyczny')
    plot.plot(n, scoresOptim[i], label='Optymistyczny')
    plot.legend()
    plot.title(labels[i])
    plot.xlabel('Rozmiar proby (n)')
    plot.ylabel('Czas [ns]')
    plot.show()


