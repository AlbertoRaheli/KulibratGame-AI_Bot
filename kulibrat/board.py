import pygame
from .const import *
from .piece import Piece
import copy
from operator import itemgetter

class Board:
    def __init__(self):
        self.board = []
        self.score_blue = self.score_red = 0
        self.create_board()

    def draw_squares(self,win):
        win.fill(WHITE)
        for row in range(ROWS):
            for col in range(COLS):
                if col >=0 and col < 5:
                    if row == 1 or row == 6 :
                        pygame.draw.rect(win, GREEN, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                if col >0 and col <4:
                    if row > 1 and row < 6:
                        pygame.draw.rect(win, GREY, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        for row in range(ROWS):
            for col in range(COLS-2):
                pygame.draw.rect(win, BLACK, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), width=1)

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col >=0 and col < 4 and row ==0:
                    self.board[row].append(Piece(row, col, RED))
                elif col >=0  and col < 4 and row == 7:
                    self.board[row].append(Piece(row, col, BLUE))
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def move(self, piece, row, col):
        self.board[piece.row][piece.col],  self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == 1 and piece.color ==BLUE:
            self.score_blue += 1
        if row == 6 and piece.color == RED:
            self.score_red +=1
    
    def return_start(self, piece):
        if piece.color == RED:
            row = 0
        else:
            row = 7

        for col in range(4):
            current = self.get_piece(row, col)
            if current == 0:
                self.move(piece, row, col)
                break

    def get_piece(self, row, col):
        return  self.board[row][col]

    def get_valid_moves(self, piece):
        moves = []
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED:
            if piece.row == 0:
                moves.extend(self.join_board(piece))
            else:
                moves.extend(self.movements(piece))

        if piece.color == BLUE:
            if piece.row == 7:
                moves.extend(self.join_board(piece))
            else:
                moves.extend(self.movements(piece))

        return moves

    def join_board(self, piece):
        moves = []
        if piece.color == RED:
            row = 2
        else: 
            row = 5

        for col in range(1,4):
            current = self.get_piece(row,col)
            if current == 0:
                moves.append((row,col))

        return moves
    
    def movements(self, piece):
        moves = []
        if piece.color == RED:
            temp = BLUE
        else:
            temp = RED

        for col in range(1,4):
            row = piece.row + piece.direction
            current = self.get_piece(row,col)
            
            if (str(current) != str(piece.color)) and (current != 0) and (col == piece.col):
                moves.append((row,col))
                
                row_j = row + piece.direction
                current_j = self.get_piece(row_j,col)
                if current_j == 0:
                    moves.append((row_j, col))

                elif (str(current_j) != str(piece.color)):
                    row_2j = row_j + piece.direction
                    current_2j = self.get_piece(row_2j,col)
                    if current_2j == 0:
                        moves.append((row_2j, col))

            if (col == piece.col + piece.direction or col == piece.col - piece.direction)  and current == 0:
                moves.append((row,col))     

        moves.sort(key=itemgetter(0), reverse=True)
        return moves

    def winner(self):
        if self.score_blue >=SCORE:
            return BLUE
        elif self.score_red >=SCORE:
            return RED

        return None

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        
        return pieces

    
        
        
