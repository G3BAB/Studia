# Jakub Opyrchał (266252)
# Algorytmy i Struktury Danych
# 27.04.2023 r.

import random
import itertools
import time as tm
from collections import deque


def deckShuffle():
    """Tasowanie kart"""
    names = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    symbols = ['Pik', 'Kier', 'Karo', 'Trefl']

    deck = list(itertools.product(names, symbols))
    deck.append((15, 'Czarny'))
    deck.append((15, 'Czerwony'))

    random.shuffle(deck)
    return deck


def dealCards():
    """Rozdanie kart"""
    deck = deckShuffle()
    deck1 = deque()
    deck2 = deque()

    for i in range(1, 27):
        deck1.append(deck.pop())
        deck2.append(deck.pop())

    return deck1, deck2


def decode(value):
    """Dekodowanie wartości kart"""
    encodeDict = {
        11: 'Walet',
        12: 'Dama',
        13: 'Król',
        14: 'As',
        15: 'JOKER'
    }

    name = encodeDict[value]
    return name


def announce(P1, P2, war):
    """Status rozgrywki"""

    if war == 0:
        print('\n~~~~~~~~KARTY~~~~~~~~')

    if war == 0:
        if P1[0] >= 11:
            name = decode(P1[0])
            print('{}{}{}{}'.format("Karta Gracza 1: ", name, ' ', P1[1]))
        else:
            print('{}{}{}{}'.format("Karta Gracza 1: ", P1[0], ' ', P1[1]))

    elif war == 1:
        if P1[0] >= 11:
            name = decode(P1[0])
            print('{}{}{}{}'.format("   Karta Gracza 1: ", name, ' ', P1[1]))
        else:
            print('{}{}{}{}'.format("   Karta Gracza 1: ", P1[0], ' ', P1[1]))

    if war == 0:
        if P2[0] >= 11:
            name = decode(P2[0])
            print('{}{}{}{}'.format("Karta Gracza 2: ", name, ' ', P2[1]))
        else:
            print('{}{}{}{}'.format("Karta Gracza 2: ", P2[0], ' ', P2[1]))

    elif war == 1:
        if P2[0] >= 11:
            name = decode(P2[0])
            print('{}{}{}{}'.format("   Karta Gracza 2: ", name, ' ', P2[1]))
        else:
            print('{}{}{}{}'.format("   Karta Gracza 2: ", P2[0], ' ', P2[1]))


def play(timeDelay):
    """Przeprowadzenie gry"""
    Player1, Player2 = dealCards()
    result = 0
    counter = 0

    while len(Player1) > 0 and len(Player2) > 0:
        counter += 1
        result = 0
        print(f"\nWynik: {len(Player1)}:{len(Player2)}")
        append = random.randint(0, 1)  # zapewnia losowość kolejności odkładania kart do talii

        P1 = Player1.pop()
        P2 = Player2.pop()
        announce(P1, P2, 0)
        tm.sleep(timeDelay)

        if P1[0] > P2[0]:
            if append == 1:
                Player1.appendleft(P1)
                Player1.appendleft(P2)
            else:
                Player1.appendleft(P2)
                Player1.appendleft(P1)

            print("\nGracz 1 Zabiera Karty!")
            tm.sleep(timeDelay)

        elif P1[0] < P2[0]:
            if append == 1:
                Player2.appendleft(P1)
                Player2.appendleft(P2)
            else:
                Player2.appendleft(P2)
                Player2.appendleft(P1)
            print("\nGracz 2 Zabiera Karty!")
            tm.sleep(timeDelay)

        elif P1[0] == P2[0]:
            print("\n   !!! WOJNA !!!")

            warDeck1 = []
            warDeck2 = []

            warDeck1.append(P1)
            warDeck2.append(P2)
            tm.sleep(timeDelay)

            topCard1 = 0
            topCard2 = 0

            while topCard1 == topCard2:
                if len(Player1) < 2:
                    result = 2
                    topCard1 = 0
                    topCard2 = 1

                elif len(Player2) < 2:
                    result = 1
                    topCard2 = 0
                    topCard1 = 1

                else:
                    for i in range(2):
                        warDeck1.append(Player1.pop())
                        warDeck2.append(Player2.pop())

                    topCard1 = warDeck1.pop()
                    warDeck1.append(topCard1)

                    topCard2 = warDeck2.pop()
                    warDeck2.append(topCard2)

                    tm.sleep(timeDelay)
                    announce(topCard1, topCard2, 1)
                    tm.sleep(timeDelay)

                    topCard1 = topCard1[0]
                    topCard2 = topCard2[0]

                if topCard1 > topCard2:
                    print("\nGracz 1 Zabiera Karty!")
                    if append == 1:
                        for element in warDeck1:
                            Player1.appendleft(element)
                        for element in warDeck2:
                            Player1.appendleft(element)
                    else:
                        for element in warDeck2:
                            Player1.appendleft(element)
                        for element in warDeck1:
                            Player1.appendleft(element)

                elif topCard1 < topCard2:
                    print("\nGracz 2 Zabiera Karty!")
                    if append == 1:
                        for element in warDeck1:
                            Player2.appendleft(element)
                        for element in warDeck2:
                            Player2.appendleft(element)
                    else:
                        for element in warDeck2:
                            Player2.appendleft(element)
                        for element in warDeck1:
                            Player2.appendleft(element)

                elif topCard1 == topCard2:
                    print("\n   WOJNA TRWA...")
                    tm.sleep(timeDelay)

    if len(Player1) < 1:
        result = 2
    elif len(Player2) < 1:
        result = 1

    if result == 1:
        print("\n\n~~~~WYGRYWA GRACZ 1!~~~~")
    elif result == 2:
        print("\n\n~~~~WYGRYWA GRACZ 2!~~~~")

    print(f"Ilość iteracji: {counter}")


play(0)  # Argument: czas między komunikatami w sekundach
