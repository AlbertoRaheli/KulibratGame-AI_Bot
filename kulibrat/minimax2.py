import pygame
from .const import*
from .board import Board
import copy
from .piece import Piece
from .game import *
from .field import *


f1 = field(1, 1, 4, 1)
f2 = field(1, 2, 6, 2)
f3 = field(1, 3, 4, 1)
f4 = field(2, 1, 7, 2)
f5 = field(2, 2, 5, 1)
f6 = field(2, 3, 7, 2)
f7 = field(3, 1, 11, 1)
f8 = field(3, 2, 15, 2)
f9 = field(3, 3, 11, 1)
f10 = field(4, 1, 18, 2)
f11 = field(4, 2, 18, 1)
f12 = field(4, 3, 18, 2)
f13 = field(5, 1, 1, 1)
f14 = field(5, 2, 1, 2)
f15 = field(5, 3, 1, 1)

fields = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14, f15]

#amount of points in penalty for each missing piece from the board
missingPiecePenaltyMultiplier = 2
#farther away the pieces are, the larger the penalty is
proximityPenaltyMultiplier = 1
#amount of points as penalty for difference in the amount of figures in the pathways
pathwayPenaltyMultiplier = 1


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

def minimax2(board, depth, max_player, alpha, beta):
    if depth == 0  or board.winner() != None :
        return evaluate2(board), board
    
    if max_player==RED:
        max_eval = float('-inf')
        best_move = None
        for move in get_all_moves(board, RED):
            evaluation = minimax2(move, depth-1, BLUE, alpha, beta)[0]
            max_eval = max(max_eval, evaluation)
            if max_eval == evaluation:
                best_move = move
            if winning_stack2(move) or winning_row2(move):
                return 1000, move
                break
            
        return max_eval, best_move

    elif max_player==BLUE:
        min_eval = float('inf')
        best_move = None 
        for move in get_all_moves(board, BLUE):
            evaluation = minimax2(move, depth-1, RED, alpha, beta)[0]
            min_eval = min(min_eval, evaluation)
            if min_eval == evaluation:
                best_move = move
            if winning_stack2(move) or winning_row2(move):
                return -1000, move
                break
    
        return min_eval, best_move

def winning_stack2(board):
    red1 = board.get_piece(5,2)
    red2 = board.get_piece(4,2)
    red3 = board.get_piece(3,2)

    if red1 != 0 and red2 != 0 and red3 != 0: 
        if red1.color == RED and red2.color == RED and red3.color == RED: 
            return True
    else:
        return False

def winning_row2(board):
    red1 = board.get_piece(5,1)
    red2 = board.get_piece(5,2)
    red3 = board.get_piece(5,3)

    if red1 != 0 and red2 != 0 and red3 != 0:
        if red1.color == RED and red2.color == RED and red3.color == RED:
            return True
    else:
        return False


def calculatePathwayPenaltyBlue(blue_pieces):
    pathway1 = 0
    pathway2 = 0
    pathwaypenalty = 0
    for piece in blue_pieces:
        for field in fields:
            if piece.row == field.row and piece.col == field.col:
                if field.pathway == 1:
                    pathway1 = pathway1 + 1
                
                else:
                    pathway2 = pathway2 + 1
    # *2 to increase the penalty to two points
    pathwaypenalty = abs(pathway1 - pathway2) * pathwayPenaltyMultiplier
    return pathwaypenalty

def calculatePathwayPenaltyRed(red_pieces):
    pathway1 = 0
    pathway2 = 0
    pathwaypenalty = 0
    for piece in red_pieces:
        for field in fields:
            if piece.row == field.row and piece.col == field.col:
                if field.pathway == 1:
                    pathway1 = pathway1 + 1
                
                else:
                    pathway2 = pathway2 + 1
    # *2 to increase the penalty to two points
    pathwaypenalty = abs(pathway1 - pathway2) * pathwayPenaltyMultiplier
    return pathwaypenalty
    
def proximityBonusBlue(blue_pieces):
    #calculate distance between every piece, take average of all distance
    proximityBonus = 0
    iteration2 = 0
    distanceSum = 0
    iterationTotal = 0
    for piece1 in blue_pieces:
        iteration = 0
        for piece2 in blue_pieces:
            if iteration2 == iteration:
                continue

            distance = ((piece1.row - piece2.row) ** 2 + (piece1.col - piece2.col) ** 2 ) ** 0.5
            iteration = iteration + 1
            iterationTotal += 1
            distanceSum = distanceSum + distance
        
        iteration2 += 1
    if iterationTotal != 0:
        proximityBonus = distanceSum / iterationTotal
    #add -2 penalty for each missing piece
    proximityBonus = proximityBonus * proximityPenaltyMultiplier + (4 - len(blue_pieces)) * missingPiecePenaltyMultiplier
    return proximityBonus

def proximityBonusRed(red_pieces):
    #calculate distance between every piece, take average of all distance
    proximityBonus = 0
    iteration2 = 0
    distanceSum = 0
    iterationTotal = 0
    for piece1 in red_pieces:
        iteration = 0
        for piece2 in red_pieces:
            if iteration2 == iteration:
                continue

            distance = ((piece1.row - piece2.row) ** 2 + (piece1.col - piece2.col) ** 2 ) ** 0.5
            iteration = iteration + 1
            iterationTotal += 1
            distanceSum = distanceSum + distance
        
        iteration2 += 1
    if iterationTotal != 0:
        proximityBonus = distanceSum / iterationTotal
    #add -2 penalty for each missing piece
    proximityBonus = proximityBonus * proximityPenaltyMultiplier + (4 - len(red_pieces)) * missingPiecePenaltyMultiplier
    return proximityBonus
    

def evaluate2(board):
        pointsplay = 0
        
        goal_b = 1
        goal_r =  1

        red1 = board.get_piece(5,2)
        red2 = board.get_piece(4,2)

        if red1 !=0 and red2!=0:
            if red1.color == RED and red2.color == RED:
                t=1000
                q=100
       
        if board.score_red >= SCORE-1:
            goal_r = float('inf')
        if board.score_blue >= SCORE-1:
            goal_b = 5000
       
        
        r=0
        b=0
        sumred= 0
        sumblue= 0
        red_pieces = proper_get_all_pieces(board, RED)
        blue_pieces = proper_get_all_pieces(board,BLUE)
        
        pathwayPenaltyBlue = calculatePathwayPenaltyBlue(blue_pieces) - calculatePathwayPenaltyRed(red_pieces)
        pathwayPenaltyRed = calculatePathwayPenaltyRed(red_pieces) - calculatePathwayPenaltyBlue(blue_pieces)
        proxyBonusBlue = proximityBonusBlue(blue_pieces) - proximityBonusRed(red_pieces)
        proxyBonusRed = proximityBonusRed(red_pieces) - proximityBonusBlue(blue_pieces)

        f1Scorer = f1.getScore(pathwayPenaltyRed, proxyBonusRed)
        f2Scorer = f2.getScore(pathwayPenaltyRed,  proxyBonusRed)
        f3Scorer = f3.getScore(pathwayPenaltyRed,  proxyBonusRed)
        f4Scorer = f4.getScore(pathwayPenaltyRed,  proxyBonusRed)
        f5Scorer = f5.getScore(pathwayPenaltyRed,  proxyBonusRed)
        f6Scorer = f6.getScore(pathwayPenaltyRed,  proxyBonusRed)
        f7Scorer = f7.getScore(pathwayPenaltyRed,  proxyBonusRed)
        f8Scorer = f8.getScore(pathwayPenaltyRed,  proxyBonusRed)
        f9Scorer = f9.getScore(pathwayPenaltyRed,  proxyBonusRed)
        f10Scorer = f10.getScore(pathwayPenaltyRed,  proxyBonusRed)
        f11Scorer = f11.getScore(pathwayPenaltyRed,  proxyBonusRed)
        f12Scorer = f12.getScore(pathwayPenaltyRed,  proxyBonusRed)
        f13Scorer = goal_r
        f14Scorer = goal_r
        f15Scorer = goal_r

        A_red = [[0, 0, 0],
        [f1Scorer, f2Scorer, f3Scorer],
          [f4Scorer, f5Scorer, f6Scorer],
          [f7Scorer, f8Scorer, f9Scorer],
          [f10Scorer, f11Scorer, f12Scorer], 
          [f13Scorer, f14Scorer, f15Scorer]]
          
        f1Scoreb = f1.getScore(pathwayPenaltyBlue,  proxyBonusBlue)
        f2Scoreb = f2.getScore(pathwayPenaltyBlue,  proxyBonusBlue)
        f3Scoreb = f3.getScore(pathwayPenaltyBlue,  proxyBonusBlue)
        f4Scoreb = f4.getScore(pathwayPenaltyBlue,  proxyBonusBlue)
        f5Scoreb = f5.getScore(pathwayPenaltyBlue,  proxyBonusBlue)
        f6Scoreb = f6.getScore(pathwayPenaltyBlue,  proxyBonusBlue)
        f7Scoreb = f7.getScore(pathwayPenaltyBlue,  proxyBonusBlue)
        f8Scoreb = f8.getScore(pathwayPenaltyBlue,  proxyBonusBlue)
        f9Scoreb = f9.getScore(pathwayPenaltyBlue,  proxyBonusBlue)
        f10Scoreb = f10.getScore(pathwayPenaltyBlue,  proxyBonusBlue)
        f11Scoreb = f11.getScore(pathwayPenaltyBlue,  proxyBonusBlue)
        f12Scoreb = f12.getScore(pathwayPenaltyBlue,  proxyBonusBlue)
        f13Scoreb = goal_b
        f14Scoreb = goal_b
        f15Scoreb = goal_b

        A_blue = [[f13Scoreb, f14Scoreb, f15Scoreb],
        [f10Scoreb, f11Scoreb, f12Scoreb], 
        [f7Scoreb, f8Scoreb, f9Scoreb], 
        [f4Scoreb, f5Scoreb, f6Scoreb], 
        [f1Scoreb, f2Scoreb, f3Scoreb],
        [0, 0, 0]]
        
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

        pointsplay = sumred - sumblue 
        
        return pointsplay

def proper_get_all_pieces(board, color):
        pieces = []
        rownum = -2
        for row in board.board:
            rownum = rownum + 1
            colwnum = -1
            for piece in row:
                colwnum = colwnum + 1
                if piece != 0 and piece.color == color and rownum != -1 and rownum != 6:
                    pieceObj = Piece(rownum,colwnum,color)
                    pieces.append(pieceObj)
        
        return pieces

