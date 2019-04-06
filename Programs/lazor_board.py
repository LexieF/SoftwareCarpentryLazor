#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 23:41:11 2019

@author: Wenye Deng, Yuchun Wang
"""

import numpy as np
from copy import deepcopy

import lazor_input

class BoardStatus():
    """
    A class describe the status of the game board.
    """
    def __init__(self, grid, lasers, blocks, points):
        self.grid = deepcopy(grid)
        self.lasers = deepcopy(lasers)
        self.blocks = deepcopy(blocks)
        self.points = deepcopy(points)


        
    def laser_pathway(self):
        """
        A function calculate all the points that laser will pass through on the current status.
        """
        def coord_trans(p1, p2):
            '''
            Transfer point coordinates into row and column of grid
            
            **Parameteres**
            
                p1: *array, int*
                    Coordinate of first point.
                p2: *array, int*
                    Coordinate of a neighbor point.
                    
            **Returns**
            
                pos: *list, int*
                    The position both p1 and p2 occupied.
            '''
            position = []
            
            if p1[0] % 2 == 0:
                position.append((p1[1]-1) / 2)
                position.append((p2[0]-1) / 2)
            else:
                position.append((p2[1]-1) / 2)
                position.append((p1[0]-1) / 2)
                
            return position

        x_bound = 2 * len(self.grid[0])
        y_bound = 2 * len(self.grid)
        
        laser_path = []
        laser_lines = deepcopy(self.lasers)
        for l in laser_lines:
            
            start_point = np.array([l[0], l[1]])
            laser_path.append(list(start_point))
            laser_point = start_point
            current_point = start_point
            previous_point = np.array([0, 0])
                        
            while not previous_point.all == current_point.all:
                previous_point = current_point                
                laser_point = current_point + np.array([l[2], l[3]])
                if laser_point[0] <= x_bound and laser_point[0] >= 0 and laser_point[1] <= y_bound and laser_point[1] >= 0:
                    # Check if there any block on next move
                    pos = coord_trans(current_point, laser_point)
                    if self.grid[pos[0]][pos[1]] == 'o':
                        laser_path.append(list(laser_point))
                        current_point = laser_point
                    # Change the direction of the laser
                    elif self.grid[pos[0]][pos[1]] == 'A':
                        if current_point[0] % 2 == 0:
                            laser_lines.append([current_point[0], current_point[1], -l[2], l[3]])
                        else: 
                            laser_lines.append([current_point[0], current_point[1], l[2], -l[3]])
                    elif self.grid[pos[0]][pos[1]] == 'C':
                        # Refracted lazer
                        laser_lines.append([laser_point[0], laser_point[1], l[2], l[3]])
                        # Reflected lazer
                        if current_point[0] % 2 == 0:
                            laser_lines.append([current_point[0], current_point[1], -l[2], l[3]])
                        else: 
                            laser_lines.append([current_point[0], current_point[1], l[2], -l[3]])
                    else:
                        break
                else:
                    break               
        laser_path = list(dict.fromkeys(laser_path))
        
        return laser_path
    
     
    def put_block(self, block_pos, block_type):
        '''
        A function that put block on a specific position of the board.
        
        **Parameters**
        
            block_pos: *list, int*
                The position on the board want to put block.
            block_type: *str*
                One of three different types of block.
                Possible value are 'A', 'B' or 'C'.
                
        **Returns**
        
            self.grid: *list*
                A matrix describe the board.
            self.blocks: *dict*
                The updated blocks set after puting block on board.
        '''
        
        self.blocks[block_type] -= 1
        if self.blocks[block_type] == 0:
           del self.blocks[block_type] 
        self.grid[block_pos[0]][block_pos[1]] = block_type
        return self.grid, self.blocks
            
    
    def delete_block(self, block_pos, block_type):
        '''
        A function that delete block on a specific position of the board.
        
        **Parameters**
        
            block_pos: *list, int*
                The position on the board want to delete block.
            block_type: *str*
                One of three different types of block.
                Possible value are 'A', 'B' or 'C'.
                
        **Returns**
        
            self.grid: *list*
                A matrix describe the board.
            self.blocks: *dict*
                The updated blocks set after deleting block on board.
        '''
        if block_type not in self.blocks:
            self.blocks[block_type] = 1
        else:
            self.blocks[block_type] += 1
        self.grid[block_pos[0]][block_pos[1]] = 'o'
        return self.grid, self.blocks

        
    
class TreeNode():
    def __init__(self, board_status):
        self.board_status = board_status

    
class GameTree():
    def __init__(self, init_status):
        self.init_status = init_status
        self.root = TreeNode(self.init_status)
        
if __name__ == '__main__':
    
    # Test code for BoardStatus class
    filename = '../Lazor_board/mad_1.bff'
    grid, lasers, blocks, points = lazor_input.read_lazor_board(filename)
    bs_test = BoardStatus(grid, lasers, blocks, points)
    print bs_test.grid
    print bs_test.lasers
    print bs_test.blocks
    print bs_test.points
    print grid
    print lasers
    print blocks
    print points    
    print bs_test.laser_pathway()
    
    bs_test.put_block([2, 2], 'C')
    print bs_test.laser_pathway()
    print bs_test.grid
    print bs_test.lasers
    print bs_test.blocks
    print bs_test.points
    print grid
    print lasers
    print blocks
    print points
    
    bs_test.delete_block([2, 2], 'C')
    print bs_test.laser_pathway()
    print bs_test.grid
    print bs_test.lasers
    print bs_test.blocks
    print bs_test.points
    print grid
    print lasers
    print blocks
    print points
    # Test end