import pygame
from .const import*
from .board import Board
import copy
from .piece import Piece
from .game import *
from .field import *

def simulate_move(board, piece, row, col):
    temp = board.get_piece(row,col)
    if temp != 0:
        if temp != piece:
            board.return_start(temp)

    if piece !=0:
        board.board[piece.row][piece.col],  board.board[row][col] = board.board[row][col], board.board[piece.row][piece.col]

    if row == 1:
        board.score_blue += 1
    if row == 6:
        board.score_red +=1
    
    return board

def get_all_moves(board, color):
    moves = []
    for col in range(1,4):
        piece_b = board.get_piece(1,col)
        piece_r = board.get_piece(6,col)
        if piece_r != 0:
            board.return_start(piece_r)
            
        if piece_b != 0:
            board.return_start(piece_b)

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move in valid_moves:
            temp_board = copy.deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_board, temp_piece, move[0], move[1])
            moves.append(new_board)
    
    return moves

def minimax1(board, depth, max_player, alpha, beta):
    if depth == 0  or board.winner() != None :
        return evaluate1(board), board
    
    if max_player==BLUE:
        max_eval = float('-inf')
        best_move = None
        for move in get_all_moves(board, BLUE):
            evaluation = minimax1(move, depth-1, RED, alpha, beta)[0]
            max_eval = max(max_eval, evaluation)
            if max_eval == evaluation:
                best_move = move
            if winning_stack1(move) or winning_row1(move):
                return 1000, move
                break
            
        return max_eval, best_move

    elif max_player==RED:
        min_eval = float('inf')
        best_move = None 
        for move in get_all_moves(board, RED):
            evaluation = minimax1(move, depth-1, BLUE, alpha, beta)[0]
            min_eval = min(min_eval, evaluation)
            if min_eval == evaluation:
                best_move = move
            if winning_stack1(move) or winning_row1(move):
                return -1000, move
                break

        return min_eval, best_move

def winning_stack1(board):
    red1 = board.get_piece(2,2)
    red2 = board.get_piece(3,2)
    red3 = board.get_piece(4,2)

    if red1 != 0 and red2 != 0 and red3 != 0: 
        if red1.color == BLUE and red2.color == BLUE and red3.color == BLUE: 
            return True
    else:
        return False

def winning_row1(board):
    red1 = board.get_piece(2,1)
    red2 = board.get_piece(2,2)
    red3 = board.get_piece(2,3)

    if red1 != 0 and red2 != 0 and red3 != 0:
        if red1.color == BLUE and red2.color == BLUE and red3.color == BLUE:
            return True
    else:
        return False

def evaluate1(board):
        pointsplay = 0
        
        goal_b = 1
        goal_r =  1
       
        if board.score_red >=  SCORE-1:
            goal_r = 500
        if board.score_blue >= SCORE-1:
            goal_b = 5000
        
        r=0
        b=0
        sumred= 0
        sumblue= 0

        A_red = [[0, 0, 0],[4, 6, 4],[7, 5, 7], [11, 20, 11], [28, 28, 28], [goal_r, goal_r, goal_r]]
        A_blue = [[goal_b, goal_b, goal_b],[18, 18, 18], [11, 15, 11], [7, 5, 7], [4, 6, 4],[0, 0, 0]]

        for row in range(6):
            for col in range(3):
                piece = board.get_piece(row+1,col+1)
                if piece != 0:
                    if piece.color == RED:
                        r+=1
                        sumred = sumred + (A_red[row][col])
                    if piece.color == BLUE:
                        b+=1
                        sumblue = sumblue + (A_blue[row][col])

        pointsplay = sumblue - sumred 
  
        return pointsplay