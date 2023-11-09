import pygame
from .const import *

class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.on_board = False
        
        if self.color == RED:
            self.direction = 1
        else:
            self.direction = -1
        
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE//2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE//2

    def draw(self, win):
        pygame.draw.circle(win, BLACK, (self.x, self.y), (SQUARE_SIZE//2) - LATERAL_PAD + 3)
        pygame.draw.circle(win, self.color, (self.x, self.y), (SQUARE_SIZE//2) - LATERAL_PAD)

    def __repr__(self):
        return str(self.color)

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

