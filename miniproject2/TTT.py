# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 23:28:36 2014

@author: zhihuixie
"""

"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 100    # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player
    
# Add your functions her
def mc_trial(board, player):
    """
    This function takes a current board and the next player to move
    """
    while board.check_win() == None:
        empty_squares = board.get_empty_squares()
        square = random.choice(empty_squares)
        board.move(square[0], square[1], player)
        player = provided.switch_player(player)
        board.check_win()
    return board
def mc_update_scores(scores, board, player): 
    """
    This function update scores
    """
    winner = board.check_win()
    dim = board.get_dim()
    if winner == 4:
        pass
    else:
        for row in range(dim):
            for col in range(dim):
                if board.square(row,col) == 1:
                    pass
                else:
                    if board.square(row,col) == winner:
                        scores[row][col] += MCMATCH
                    else:
                        scores[row][col] -= MCMATCH
def get_best_move(board, scores):
    """
    This function get best move
    """
    squares = board.get_empty_squares()
    print squares
    max_score = float("-inf")
    for (row, col) in squares:
        if scores[row][col] >= max_score:
            max_score = scores[row][col]
    max_squares =[(row, col) for (row, col) in squares if max_score == scores[row][col]]
    return random.choice(max_squares)
def mc_move(board, player, trials): 
    """
    This function get machine move
    """
    scores = [[0 for dummy_row in range(board.get_dim())]for dummy_col in range(board.get_dim())]
    for dummy_i in range(trials):
        newboard = board.clone()
        mc_trial(newboard, player)
        mc_update_scores(scores, newboard, player)
    return get_best_move(board, scores)
        
# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
