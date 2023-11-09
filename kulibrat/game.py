import pygame
from .const import*
from .board import Board
from .minimax1 import *
from .minimax2 import *
import pygame.freetype
import sys
import os
import random

class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        self.print_score(WIN)
        self.print_winner(WIN)
        pygame.time.delay(100)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.turn=None
        self.board = Board()
        self.valid_moves = []

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row,col)
        else:
            piece = self.board.get_piece(row, col)
            if piece != 0 and piece.color == self.turn:
                self.selected = piece
                self.valid_moves = self.board.get_valid_moves(piece)
                return True
        
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and (piece != self.selected.color or piece==0) and (row, col) in self.valid_moves: #(piece.color != self.selected.color or piece==0)
            if (piece != self.selected.color and piece != 0):
                self.board.return_start(piece)
            self.board.move(self.selected, row, col)
            self.valid_moves = []
            if  row == 1 or row == 6:
                piece = self.board.get_piece(row, col)
                self.board.return_start(piece)
            self.change_turn()
            self.check_turn()
        else:
            return False
 
        return True

    def change_turn(self):
        if self.turn==BLUE:
            self.turn = RED
        else:
            self.turn = BLUE

    def check_turn(self):
        total_moves = []
        for piece in self.board.get_all_pieces(self.turn):
            total_moves.extend(self.board.get_valid_moves(piece))

        if len(total_moves) < 1:
            self.change_turn()
        else:
            pass

    def draw_valid_moves(self, moves):
        for i in range(len(moves)):
            row, col = moves[i]
            pygame.draw.circle(self.win, WHITE, (col*SQUARE_SIZE + SQUARE_SIZE//2, row*SQUARE_SIZE + SQUARE_SIZE//2), 5)

    def print_score(self,win):
        tx = 64
        ty = 64

        if self.turn == RED:
            turn = "Red"
        elif self.turn == BLUE:
            turn = "Blue"

        font_size = tx
        pygame.freetype.init()
        myfont = pygame.freetype.Font('fonts/Bebas-Regular.ttf', font_size)
        myfont.render_to(win, (412, 25), "Score: "+str(self.board.score_red), RED, None, size=45)
        myfont.render_to(win, (412, 580), "Score: "+str(self.board.score_blue), BLUE, None, size=45)
        myfont.render_to(win, (412, 325), "Reach " +str(SCORE)+ " to win", BLACK, None, size=25)
        if self.turn != None:
            myfont.render_to(win, (415, 290), "Turn: "+ turn, self.turn, None, size=35)
        

    def print_winner(self, win):
        tx = 64
        ty = 64
        found = False
        
        if self.board.score_red == SCORE:
            winner = "Red"
            found = True
            color= RED
        elif self.board.score_blue == SCORE:
            winner = "Blue"
            found = True
            color= BLUE

        if found:
            font_size = tx
            pygame.freetype.init()
            pygame.draw.rect(win, WHITE, (1, 265, 559, 100))
            pygame.draw.rect(win, BLACK, (0, 264, 560, 101), width=4)
            myfont = pygame.freetype.Font('fonts/Bebas-Regular.ttf', font_size)
            myfont.render_to(win, (100, 290), "The winner is "+ winner, color , None, size=55)
            
    def winner(self):
        return self.board.winner()

    def get_board(self):
        return self.board

    def ai_move2(self):
        pieceAndMove = []
        board_result = minimax2(self.board,5, RED, float('-inf'), float('inf'))[1]
        pieceAndMove = self.find_moves2(board_result)

        piece1 = self.board.get_piece( pieceAndMove[1][0], pieceAndMove[1][1])
        if (piece1 != 0):
                self.board.return_start(piece1)
        self.board.move(pieceAndMove[0], pieceAndMove[1][0], pieceAndMove[1][1])
        
        self.valid_moves = []
        if  pieceAndMove[1][0] == 1 or pieceAndMove[1][0] == 6:
            piece2 = self.board.get_piece( pieceAndMove[1][0], pieceAndMove[1][1])
            self.board.return_start(piece2)
        
        self.change_turn()
        self.check_turn()
            

    def find_moves2(self, new_board):
        move = []
        for row in range(8):
            for col in range(5):
                if self.board.board[row][col] != new_board.board[row][col]:
                    if self.board.board[row][col] != 0 and new_board.board[row][col] ==0 :
                        piece = self.board.get_piece(row,col)
                    if (self.board.board[row][col] == 0 and new_board.board[row][col]!=0):
                        move.append((row,col))
                        
                    if (self.board.board[row][col] !=0 and new_board.board[row][col] != 0 ):
                        if (self.board.board[row][col].color != new_board.board[row][col].color):
                            move.append((row,col))
                                   
        return [piece, move[0]]
  
    def ai_move1(self):
        pieceAndMove = []
        board_result = minimax1(self.board,5, BLUE, float('-inf'), float('inf'))[1]
        pieceAndMove = self.find_moves1(board_result)

        piece1 = self.board.get_piece( pieceAndMove[1][0], pieceAndMove[1][1])
        if (piece1 != 0):
                self.board.return_start(piece1)
        self.board.move(pieceAndMove[0], pieceAndMove[1][0], pieceAndMove[1][1])
        
        self.valid_moves = []
        if  pieceAndMove[1][0] == 1 or pieceAndMove[1][0] == 6:
            piece2 = self.board.get_piece( pieceAndMove[1][0], pieceAndMove[1][1])
            self.board.return_start(piece2)
        
        self.change_turn()
        self.check_turn()
        
    def find_moves1(self, new_board):
        move = []
        for row in range(7,0,-1):
            for col in range(5):
                if self.board.board[row][col] != new_board.board[row][col]:
                    if self.board.board[row][col] != 0 and new_board.board[row][col] ==0 :
                        piece = self.board.get_piece(row,col)
                    if (self.board.board[row][col] == 0 and new_board.board[row][col]!=0):
                        move.append((row,col))
                        
                    if (self.board.board[row][col] !=0 and new_board.board[row][col] != 0 ):
                        if (self.board.board[row][col].color != new_board.board[row][col].color):
                            move.append((row,col))

        return [piece, move[0]]