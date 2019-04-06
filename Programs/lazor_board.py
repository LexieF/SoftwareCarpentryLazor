#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 23:41:11 2019

@author: Wenye Deng and Yuchun Wang
"""

import numpy as np

class BoardStatus():
    """
    A class describe the status of the game board.
    """
    def __init__(self, grid, lasers, blocks, points):
        self.grid = grid
        self.laser = lasers
        self.block = blocks
        self.point = points

    # def cood_trans(self):
    #     '''
    #     
    #     '''
    #     pass

    def reflect(self):
        pass

        
    def laser_pathway(self):
        """
        A function calculate the points that laser will pass through.
        """
        x_bound = 2 * len(self.grid[0])
        y_bound = 2 * len(self.grid)
        
        all_laser_path = []
        for l in self.laser:
            
            laser_point = np.array([int(l[0]), int(l[1])]) + np.array([int(l[2]), int(l[3])])
            laser_path = [laser_point]
            
            while True:
                laser_point = laser_point + np.array([int(l[2]), int(l[3])])
                if laser_point[0] <= x_bound and laser_point[0] >= 0 and laser_point[1] <= y_bound and laser_point[1] >= 0:
                    laser_path.append(laser_point)
                else:
                    break
            all_laser_path.append(laser_path)
        
        return all_laser_path
    
    # def possible_positions(self):
    #     pass
    
    def replace(self, grid, m, n, c):
    	# Replace the item in specific position [m,n] of grid with new item c
    	new = []
    	string = self.grid[m]
    	for s in string:
    		new.append(s)
    	new[n] = c
    	self.grid[m] = ''.join(new)
    	return self.grid

    def put_block(self, block_position, block_type):
        # Put a specific block into  sepecific position []
        self.grid = replace(self.grid, block_position[0] - 1, (block_position[1] - 1) * 4, block_type)
        block_number = int(self.block[block_type]) - 1
        self.block[block_type] = str(block_number)
        if block_number == 0:
        	del self.block[block_type]
        return self.grid, self.block
    
    def delete_block(self, block_position):
        # Delete a block in sepecific position []
        m = block_position[0] - 1
        n = (block_position[1] - 1) * 4
        block_type = self.grid[m][n]
        self.grid = replace(self.grid, m, n, 'o')
        if block_type in self.block:
        	block_number = int(self.block[block_type]) + 1
        	self.block[block_type] = str(block_number)
        else:
        	self.block[block_type] = str(1)
        return self.grid, self.block

    
class TreeNode():
    def __init__(self, board_status):
        self.board_status = board_status
        self.parent = bs
        self.children = []
        
        for (i, elem) in enumerate(possible_step):
            locals()['children' + str(i)] = elem

    
class GameTree():
    def __init__(self, init_status):
        self.init_status = init_status
        self.root = TreeNode(self.init_status)