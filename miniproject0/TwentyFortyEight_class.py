# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 21:29:19 2014

@author: zhihuixie
"""
import random
# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0), 
           DOWN: (-1, 0), 
           LEFT: (0, 1), 
           RIGHT: (0, -1)} 

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.grids = [ [0 for dummy_col in range(self.grid_width)] for dummy_row in range(self.grid_height)]
        self.init_dict = {1:[(0, num_of_width) for num_of_width in range(self.grid_width)], 
                          2:[(self.grid_height - 1, num_of_width) for num_of_width in range(self.grid_width)],
                          3:[(num_of_height, 0) for num_of_height in range(self.grid_height)],
                          4:[(num_of_height, self.grid_width - 1) for num_of_height in range(self.grid_height)]}
    
    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        # replace with your code
        self.grids = [ [0 for dummy_col in range(self.grid_width)] for dummy_row in range(self.grid_height)]
    
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        print "The grid height is: " + self.grid_height
        print "The grid width is: " + self.grid_width

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self.grid_height
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self.grid_width
                            
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # replace with your code
        for indices in self.init_dict[direction]:
            (dir1, dir2) = OFFSETS[direction]
            temp_tiles = [indices]
            temp_list = []
            if dir2 == 0:
                for dummy_i in range (self.grid_height - 1):
                    (num1, num2) = temp_tiles[-1]
                    temp_tiles.append((dir1 + num1, dir2 + num2))
            if dir1 == 0:
                for dummy_j in range (self.grid_width - 1):
                    (num1, num2) = temp_tiles[-1]
                    temp_tiles.append((dir1 + num1, dir2 + num2))
            for (indx1, indx2) in temp_tiles:
                temp_list.append(self.grids[indx1][indx2])
            new_list = merge(temp_list)
            count = 0
            for (indx1, indx2) in temp_tiles:
                self.grids[indx1][indx2] = new_list[count]
                count += 1
        self.new_tile()        
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # replace with your code
        num_of_row = random.randrange(self.grid_height)
        num_of_col = random.randrange(self.grid_width)
        num_of_rate = random.randrange(10)
        is_empty = False
        for col in self.grids:
            if 0 in col: 
                is_empty = True
        if is_empty:
            while self.grids[num_of_row][num_of_col] != 0:
                   num_of_row = random.randrange(self.grid_height)
                   num_of_col = random.randrange(self.grid_width)
            if num_of_rate == 9:                  
                self.grids[num_of_row][num_of_col] = 4
            else:
                self.grids[num_of_row][num_of_col] = 2
                  
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """        
        # replace with your code
        
        self.grids[row][col] = value
        

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """        
        # replace with your code
        return self.grids[row][col]


