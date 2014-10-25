# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 22:54:41 2014

@author: zhihuixie
"""

"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(200)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    winner = board.check_win()
    if winner != None:
        return SCORES[winner], (-1,-1)
    else:
        score_list = []
        squares = board.get_empty_squares()
        for square in squares:
            new_board = board.clone()
            next_player = provided.switch_player(player)
            new_board.move(square[0], square[1], player)
            score, dummy_move = mm_move(new_board, next_player)
            score_list.append(score)
        if player == 2:
              max_score = max(score_list)
              return max_score, squares[score_list.index(max_score)]
        elif player == 3:
              min_score = min(score_list)
              return min_score, squares[score_list.index(min_score)]
            
                    
    
def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

provided.play_game(move_wrapper, 1, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
