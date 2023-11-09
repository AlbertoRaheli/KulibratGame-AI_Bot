import pygame

WIDTH, HEIGHT = 560, 640
ROWS, COLS = 8, 7
SQUARE_SIZE = WIDTH//COLS
LATERAL_PAD = SQUARE_SIZE//6
SCORE = 5

#COLORS
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

