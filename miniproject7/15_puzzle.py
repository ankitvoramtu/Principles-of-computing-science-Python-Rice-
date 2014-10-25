# -*- coding: utf-8 -*-
"""
Created on Sat Aug  2 22:21:07 2014

@author: zhihuixie
"""

"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        if self._grid[target_row][target_col] != 0:
            return False
        elif target_row == self._height -1:
            if target_col == self._width -1:
                return True
            else:
                for col in range (target_col + 1, self._width):
                    sloved_position = self.current_position (target_row, col)
                    if sloved_position != (target_row, col):
                        return False
        else:
            for col in range (self._width):
                for row in range (target_row + 1, self._height):
                    sloved_position = self.current_position (row, col)
                    if sloved_position != (row, col):
                        return False
            for col in range (target_col + 1, self._width):
                sloved_position = self.current_position (target_row, col)
                if sloved_position != (target_row, col):
                    return False
        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        move_string = ""
        target_value = target_col + self._width * target_row
        
        for dummy_row in range (self._height):
                for dummy_col in range (self._width):
                    if self.get_number (dummy_row, dummy_col) == target_value:
                        (target_tile_row, target_tile_col) = (dummy_row, dummy_col)
        if target_col == target_tile_col: #case 1
                move_string += "u"*(target_row - target_tile_row) 
                move_string += "lddru"*(target_row - target_tile_row - 1) 
                move_string += "ld"
        elif target_row == target_tile_row: #case 2
                move_string += "l"*(target_col - target_tile_col) 
                move_string += "urrdl"*(target_col - target_tile_col - 1) 
        else:  #case 3
                if target_tile_col < target_col:
                    move_string += "u"*(target_row - target_tile_row)
                    move_string += "l"*(target_col - target_tile_col) 
                    move_string += "drrul"*(target_col - target_tile_col - 1) 
                    move_string += "dr"
                    move_string += "ulddr"*(target_col - target_tile_col - 1)
                    move_string += "uld"
                else:
                    move_string += "u"*(target_row - target_tile_row)
                    move_string += "r"*(target_tile_col - target_col) 
                    move_string += "dllur"*(target_tile_col - target_col - 1) 
                    move_string += "dl"
                    move_string += "ulddr"*(target_tile_col - target_col - 1)
                    move_string += "uld"
        self.update_puzzle(move_string)        
        return move_string
        

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # replace with your code
        move_string = ""
        target_col = 0
        target_value = target_col + self._width * target_row
        
        for dummy_row in range (self._height):
                for dummy_col in range (self._width):
                    if self.get_number (dummy_row, dummy_col) == target_value:
                        (target_tile_row, target_tile_col) = (dummy_row, dummy_col)
        if target_row - target_tile_row == 1:
            move_string += "ur"   
            
        else:
            if target_col == target_tile_col:
                move_string += "u"*(target_row - target_tile_row)
                move_string +="rddlu"*(target_row - target_tile_row - 2)
                move_string += "rdl"
                move_string += "ruldrdlurdluurddlur"
            else:
                move_string += "u"*(target_row - target_tile_row)
                move_string += "r"*(target_tile_col - target_col) 
                move_string += "dllur"*(target_tile_col - target_col - 1) 
                move_string += "dlu"
                move_string +="rddlu"*(target_row - target_tile_row - 2)
                move_string += "rdl"
                move_string += "ruldrdlurdluurddlur"
        move_string += "r"*(self._width - 2)
        self.update_puzzle(move_string)        
        return move_string

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self.get_number (0, target_col) == 0:
            new_board = self.clone()
            if new_board.get_number (1, target_col) == target_col + self._width * 1:
                new_board.set_number(1, target_col, 0)
                return new_board.row1_invariant(target_col)
            else:
                return False
        else:
            return False

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        if self.lower_row_invariant(1, target_col):
            cells = [(0, dummy_col) for dummy_col in range (target_col + 1, self._width)]
            for cell in cells:
                cell_value = cell[1] + self._width * cell[0]
                if cell_value != self.get_number (cell[0], cell[1]):
                    return False
        return self.lower_row_invariant(1, target_col)

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        
        move_string = ""
        target_row = 0
        target_value = target_col + self._width * target_row
        
        for dummy_row in range (self._height):
                for dummy_col in range (self._width):
                    if self.get_number (dummy_row, dummy_col) == target_value:
                        (target_tile_row, target_tile_col) = (dummy_row, dummy_col)
        if target_col - target_tile_col == 1:
            move_string += "ld"
            
            
        else:
            if target_row == target_tile_row:
                move_string += "l"*(target_col - target_tile_col)
                move_string +="drrul"*(target_col - target_tile_col - 2)
                move_string += "dru"
                move_string += "dlurdruldrulldrruld"
            else:
                move_string += "l"*(target_col - target_tile_col)
                move_string += "d"*(target_tile_row - target_row) 
                move_string += "ruuld"*(target_tile_row - target_row - 1) 
                move_string += "rul"
                move_string +="drrul"*(target_col - target_tile_col - 2)
                move_string += "dru"
                move_string += "dlurdruldrulldrruld"
        #move_string += "r"*(self._width - 2)
        self.update_puzzle(move_string)        
        return move_string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        move_string = ""
        target_row = 1
        target_value = target_col + self._width * target_row
        
        for dummy_row in range (self._height):
                for dummy_col in range (self._width):
                    if self.get_number (dummy_row, dummy_col) == target_value:
                        (target_tile_row, target_tile_col) = (dummy_row, dummy_col)
        if target_col == target_tile_col: #case 1
                move_string += "u"*(target_row - target_tile_row) 
                move_string += "lddru"*(target_row - target_tile_row - 1) 
                move_string += "ld"
        elif target_row == target_tile_row: #case 2
                move_string += "l"*(target_col - target_tile_col) 
                move_string += "urrdl"*(target_col - target_tile_col - 1) 
        else:  #case 3
                if target_tile_col < target_col:
                    move_string += "u"*(target_row - target_tile_row)
                    move_string += "l"*(target_col - target_tile_col) 
                    move_string += "drrul"*(target_col - target_tile_col - 1) 
                    move_string += "dr"
                    #move_string += "ulddr"*(target_col - target_tile_col - 1)
                    move_string += "uld"
                else:
                    move_string += "u"*(target_row - target_tile_row)
                    move_string += "r"*(target_tile_col - target_col) 
                    move_string += "dllur"*(target_tile_col - target_col - 1) 
                    move_string += "dl"
                    move_string += "ulddr"*(target_tile_col - target_col - 1)
                    move_string += "uld"
        move_string += "ur"
        self.update_puzzle(move_string)        
        return move_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        move_string = "lu"
        while not self.row0_invariant(0):
            move_string += "rdlu"
            self.update_puzzle(move_string)  
        # replace with your code
        return move_string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        move_string = ""
        for dummy_row in range (self._height):
            for dummy_col in range (self._width):
                if self.get_number (dummy_row, dummy_col) == 0:
                    (target_zero_row, target_zero_col) = (dummy_row, dummy_col)
        while not self.row0_invariant(0):
            if self.lower_row_invariant(target_zero_row, target_zero_col):
                if target_zero_row > 1 and target_zero_col > 0:
                    move_string += self.solve_interior_tile(target_zero_row, target_zero_col)
                elif target_zero_row > 1 and target_zero_col == 0:
                    move_string += self.solve_col0_tile(target_zero_row)
            elif self.row0_invariant(target_zero_col):
                move_string += self.solve_row0_tile(target_zero_col)
            elif self.row1_invariant(target_zero_col):
                move_string += self.solve_row1_tile(target_zero_col)
            else:
                if target_zero_row < self._height - 1:
                    move_string += "d"
                else:
                    if target_zero_col < self._width - 1:
                        move_string += "r"
            self.update_puzzle(move_string)

        #case 1 target_zero_row > 1 and target_zero_col > 0: solve_interior_tile(target_zero_row, target_zero_col)
        #case 2 target_zero_row > 1 and target_zero_col == 0: solve_col0_tile(target_zero_row)
        #case 3 target_zero_row == 1: solve_row1_tile(target_zero_col)
        #case 4 target_zero_row == 0: solve_row0_tile(target_zero_col)
        # replace with your code
        return move_string

# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))


