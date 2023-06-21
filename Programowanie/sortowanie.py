# Jakub Opyrchał (266252)
# Algorytmy i Struktury Danych
# 16.03.2023 r.
"""Algorytmy Sortowania"""

import sys
import numpy as np
import time as tm
import matplotlib.pyplot as plot


def checkArray(arr):
    """Sprawdza czy w szeregu testowym łączone są liczby z tekstem"""
    hasNonNumeric = False
    for element in arr:
        if isinstance(element, str):
            hasNonNumeric = True
        elif not isinstance(element, (int, float)):
            print("Error: Cannot compare strings with numbers")
            sys.exit()
        elif hasNonNumeric:
            print("Error: Cannot compare strings with numbers")
            sys.exit()


def selectionSort(inputArray):
    """Sortowanie przez wybieranie"""
    size = len(inputArray)

    for i in range(size - 1):
        minVal = i

        for j in range(i + 1, size):
            if inputArray[j] < inputArray[minVal]:
                minVal = j
        inputArray[i], inputArray[minVal] = inputArray[minVal], inputArray[i]

    return inputArray


def insertionSort(inputArray):
    """Sortowanie przez wstawianie"""
    size = len(inputArray)

    for i in range(size):
        for j in range(size):
            if inputArray[j] > inputArray[i]:
                inputArray[j], inputArray[i] = inputArray[i], inputArray[j]

    return inputArray


def bubbleSort(inputArray):
    """Sortowanie bąbelkowe"""
    size = len(inputArray)
    for i in range(size - 1):
        for j in range(size - 1):
            if inputArray[j] > inputArray[j + 1]:
                inputArray[j + 1], inputArray[j] = inputArray[j], inputArray[j + 1]
    return inputArray


def radixSort(inputArray):
    """Sortowanie radix"""
    buf = [[], [], [], [], [], [], [], [], [], []]
    exponent = 1
    maxDigits = len(str(max(inputArray)))

    for i in range(maxDigits):
        for j in inputArray:
            if type(j) is not int:
                return "Non-int argument detected. Cannot perform Radix Sort"
            remain = (j // exponent) % 10
            buf[remain].append(j)

        inputArray = []
        for j in buf:
            inputArray.extend(j)
            j.clear()

        buf = [[], [], [], [], [], [], [], [], [], []]

        exponent *= 10
    return inputArray


def quickSort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]

    left, middle, right = [], [], []
    for x in arr:
        if x < pivot:
            left.append(x)
        elif x == pivot:
            middle.append(x)
        else:
            right.append(x)
    
    return quickSort(left) + middle + quickSort(right)


def mergeSort(arr):
    # print(arr)
    if len(arr) <= 1:
        return arr
    middle = len(arr) // 2
    left = arr[0:middle]
    right = arr[middle:]

    lSort = mergeSort(left)
    rSort = mergeSort(right)
    
    return merge(lSort, rSort)


def merge(lArr, rArr):
    debug = False
    mergedArr = []
    i = 0
    j = 0
    if debug:
        print("{}{}".format("LEFT SIDE: ", lArr))
        print("{}{}".format("RIGHT SIDE: ", rArr))
    while i < len(lArr) and j < len(rArr):
        if lArr[i] <= rArr[j]:
            mergedArr.append(lArr[i])
            i += 1
        else:
            mergedArr.append(rArr[j])
            j += 1

    if debug:
        print(mergedArr)
    if i < len(lArr):
        mergedArr.extend(lArr[i:])
    elif j < len(rArr):
        mergedArr.extend(rArr[j:])

    return mergedArr


def countingSort(arr):
    maxElement = max(arr)
    length = len(arr)
    countArr = [0] * (maxElement + 1)
    outputArr = [0] * len(arr)

    for i in range(0, length):
        countArr[arr[i]] += 1

    countArr[0] = 0
    for i in range(1, maxElement + 1):
        countArr[i] += countArr[i-1]

    for i in range(length):
        outputArr[countArr[arr[i]]-1] = arr[i]
        countArr[arr[i]] -= 1

    return outputArr


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
        for j in range (100):
            meanComponent += timeKeep(testedFunction, set[i], label)
            timeMeasure[i] = meanComponent / 100
    # print(timeMeasure)
    return timeMeasure


def scorePlot(score, n, tag):
    """Tworzy ploty dla poszczegolnych algorytmow"""
    XP = n
    YP = score
    plot.plot(XP, YP, label=tag)


n = [100, 500, 1000, 3000, 5000]
#n = [10, 50, 100, 300, 500]


labels = ["Quick Sort", "Merge Sort", "Counting Sort"]

testSet = [[]] * len(n)
for i in range(len(n)):
    testSet[i] = np.random.randint(0, 5000, n[i])
print(testSet[0])
scores = [timeTest(quickSort, testSet, labels[0]), timeTest(mergeSort, testSet, labels[1]), timeTest(countingSort, testSet, labels[2])]

for i in range(len(n)):
    testSet[i] = countingSort(testSet[i])
scoresOptim = [timeTest(quickSort, testSet, labels[0]), timeTest(mergeSort, testSet, labels[1]),
          timeTest(countingSort, testSet, labels[2])]

for i in range(len(n)):
    testSet[i] = sorted(testSet[i], reverse=True)
    print(testSet[i])
scoresPess = [timeTest(quickSort, testSet, labels[0]), timeTest(mergeSort, testSet, labels[1]),
          timeTest(countingSort, testSet, labels[2])]

for i in range(0, 3):
    scorePlot(scores[i], n, labels[i])

plot.xlabel('Rozmiar proby (n)')
plot.ylabel('Czas [ns]')
plot.legend()
plot.show()
for i in range(0, 3):
    plot.plot(n, scores[i], label='Losowy')
    plot.plot(n, scoresPess[i], label='Pesymistyczny')
    plot.plot(n, scoresOptim[i], label='Optymistyczny')
    plot.legend()
    plot.title(labels[i])
    plot.xlabel('Rozmiar proby (n)')
    plot.ylabel('Czas [ns]')
    plot.show()
