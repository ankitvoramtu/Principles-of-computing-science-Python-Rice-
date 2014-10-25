# -*- coding: utf-8 -*-
"""
Created on Sat Jul 12 14:18:28 2014

@author: zhihuixie
"""

"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len (self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zom in self._zombie_list:
            yield zom   # replace with an actual generator
        #return

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append ((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len (self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for hum in self._human_list:
            yield hum # replace with an actual generator
        #return
        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        height = self.get_grid_height ()
        width = self.get_grid_width ()
        visited = poc_grid.Grid(height, width)
        visited.clear()
        distance_field = [[height * width for dummy_col in range (width)]for dummy_row in range (height)]
        boundary = poc_queue.Queue()
        if entity_type == HUMAN:
            for hum_cell in self._human_list:
                boundary.enqueue (hum_cell)
                visited.set_full(hum_cell[0], hum_cell[1])
                distance_field[hum_cell[0]][hum_cell[1]] = 0
        if entity_type == ZOMBIE:
            for zom_cell in self._zombie_list:
                boundary.enqueue (zom_cell)
                visited.set_full(zom_cell[0], zom_cell[1])
                distance_field[zom_cell[0]][zom_cell[1]] = 0
        while boundary:
              current_cell = boundary.dequeue()
              distance = distance_field[current_cell[0]][current_cell[1]] + 1
              neighbors = self.four_neighbors(current_cell[0], current_cell[1])
              for neighbor in neighbors:
                  if visited.is_empty(neighbor[0], neighbor[1]) and self.is_empty(neighbor[0], neighbor[1]):
                     visited.set_full(neighbor[0], neighbor[1])
                     distance_field[neighbor[0]][neighbor[1]] = distance
                     boundary.enqueue(neighbor)
                     
        return distance_field
    
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        move_list = []
        if self._human_list != []:
            for hum_cell in self._human_list:
                neighbors = self.eight_neighbors(hum_cell[0], hum_cell[1])
                neighbors.append (hum_cell)
                max_distance = max ([zombie_distance[dummy_n[0]][dummy_n[1]] for dummy_n in neighbors])
                human_move = [dummy_ne for dummy_ne in neighbors if zombie_distance[dummy_ne[0]][dummy_ne[1]] == max_distance]
                move_list.append(random.choice(human_move)) 
        #print human_move, random.choice (human_move)
        self._human_list = move_list
    
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        #print self._zombie_list
        move_list = []
        if self._zombie_list != []:
            for zom_cell in self._zombie_list:
                neighbors = self.four_neighbors(zom_cell[0], zom_cell[1])
                neighbors.append (zom_cell)
                min_distance = min ([human_distance[dummy_n[0]][dummy_n[1]] for dummy_n in neighbors])
                zom_move = [dummy_ne for dummy_ne in neighbors if human_distance[dummy_ne[0]][dummy_ne[1]] == min_distance]
                move_list.append(random.choice(zom_move)) 
        self._zombie_list = move_list
# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Zombie(30, 40))

#import user35_EPZOWWGoUeaEemm as test
#test.phase1_test(Zombie)
#test.phase2_test(Zombie)
#test.phase3_test(Zombie)
