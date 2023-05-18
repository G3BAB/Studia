import sys
import time
import pygame
from pygame.locals import *


def create_board(size):
    board = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append('-')
        board.append(row)
    return board


pygame.init()
screen = pygame.display.set_mode((200, 200), 0, 32)
pygame.display.set_mode()
pygame.sprite.Sprite
pygame.SHOWN


# pygame.screen.fill(255, 255, 255)
time.sleep(20)
symbols = {0: 'O', 1: 'X'}
