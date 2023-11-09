import pygame
from kulibrat.const import *
from kulibrat.board import Board
from kulibrat.game import Game
from kulibrat.minimax1 import *
from kulibrat.minimax2 import *
import  random


pygame.display.set_caption('Kulibrat')

def get_mouse_pos(pos):
    x, y = pos
    row = y//SQUARE_SIZE
    col = x//SQUARE_SIZE
    return row, col

def main ():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)
        
        if game.winner() != None:
            game.print_winner(WIN)
            pygame.time.delay(3000)
            game.reset()
        
        if game.turn==None:
            player = random.randint(0, 1)
            if player == 1: 
                game.turn = RED
            else: 
                game.turn = BLUE
            
            game.update()

        if game.turn == BLUE:
            game.ai_move1()
            game.update()

      
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_pos(pos)
                game.select(row,col)
        
        game.update()

    pygame.quit()

main()

