#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 23:41:11 2019

@author: Wenye Deng, Yuchun Wang

This file defines three class:
    BoardStatus(grid, lasers, blocks, points): describe the status of the game
    TreeNode
    GameTree
"""
import numpy as np
from copy import deepcopy
from lazor_input import *


class BoardStatus():
    """
    A class describe the status of the game board.
    
    **Method**
    
        laser_pathway(self)
        put_block(block_pos, block_type)
        delete_block(block_pos, block_type)
    """
    def __init__(self, grid, lasers, blocks, points):
        self.grid = deepcopy(grid)
        self.lasers = deepcopy(lasers)
        self.blocks = deepcopy(blocks)
        self.points = deepcopy(points)

    def laser_pathway(self):
        """
        Function that provide the laser pathway
        @Author: Wenhao Gao

        :return: *list*
            list comprising all coordinates that laser would pass
        """
        def board2laser(position):
            """
            Help function that transform the coordinates in board grid to laser grid
            :param position: *list*
                position in board grid
            :return: *list*
                position in laser grid
            """
            result = [0, 0]
            result[0] = position[0] * 2 + 1
            result[1] = position[1] * 2 + 1
            return result

        def laser2board(position):
            """
            Help function that transform the coordinates in laser grid to board grid
            :param position: *list*
                position in laser grid
            :return: *list*
                position in board grid
            """
            result = [0, 0]
            result[0] = (position[0] - 1) / 2
            result[1] = (position[1] - 1) / 2
            return result

        def square(a, b):
            """
            Function that check if two lasor point is in one square
            Help generate legal path

            :param a: *list* with content *int*
                lazor point 1

            :param b: *list* with content *int*
                lazor point 2

            :return: board position that may put a block or None
            """
            l = [a, b]
            position = []

            for i in range(2):
                if l[i][0] % 2 != 0:
                    position.append(l[i][0])

            for i in range(2):
                if l[i][1] % 2 != 0:
                    position.append(l[i][1])

            return np.array(position)

        def content(board, position):
            """
            Help function that return the content of input position
            """
            return board[position[1]][position[0]]

        def laser_propagate(start_point, start_direction, board, path=[]):
            """
            Function that propagate a laser beam
            """
            point = start_point
            direction = start_direction
            b_dim = len(board) * 2
            if start_point.tolist() not in path:
                path.append(start_point.tolist())

            while True:
                next = point + direction
                if next[0] == -1 or next[0] == b_dim + 1 or next[1] == -1 or next[1] == b_dim + 1:
                    break

                block_position_in_laser = square(point, next)
                block_position_in_board = laser2board(block_position_in_laser)

                if content(board, block_position_in_board) == 'o':
                    point = next
                    if point.tolist() not in path:
                        path.append(point.tolist())
                # 'A' -- reflect block
                elif content(board, block_position_in_board) == 'A':
                    # Need to consider the former block
                    former = point - direction

                    former_block_position_in_laser = square(point, former)
                    former_block_position_in_board = laser2board(former_block_position_in_laser)

                    if content(board, former_block_position_in_board) == 'o':
                        direction = direction + 2 * (point - block_position_in_laser)

                    elif content(board, former_block_position_in_board) == 'A':
                        if point.tolist() not in path:
                            path.append(point.tolist())
                        break

                    elif content(board, former_block_position_in_board) == 'C':
                        direction = direction + 2 * (point - block_position_in_laser)

                # 'B' -- opaque block
                elif content(board, block_position_in_board) == 'B':
                    break
                # 'C' -- refract block
                elif content(board, block_position_in_board) == 'C':
                    # Need to consider the former block
                    former = point - direction

                    former_block_position_in_laser = square(point, former)
                    former_block_position_in_board = laser2board(former_block_position_in_laser)

                    if content(board, former_block_position_in_board) == 'o':
                        # Normal refraction and transmission case
                        laser_propagate(
                            point, direction + 2 * (point - block_position_in_laser), board, path=path
                        )
                        laser_propagate(next, direction, board, path=path)

                    elif content(board, former_block_position_in_board) == 'A':
                        # The incident light is from refraction of 'A' block
                        # Only transmission should be considered
                        laser_propagate(next, direction, board, path=path)
                        if point.tolist() not in path:
                            path.append(point.tolist())

                    elif content(board, former_block_position_in_board) == 'C':
                        # Imaginary case (No instance to verify)
                        # The incident light is from refraction of 'A' block
                        # Only transmission should be considered
                        laser_propagate(next, direction, board, path=path)
                        if point.tolist() not in path:
                            path.append(point.tolist())

                    break

                elif content(board, block_position_in_board) == 'x':
                    break

            return path

        num_laser = len(self.lasers)
        board = self.grid
        path = []

        for i in range(num_laser):
            laser_start = np.array([self.lasers[i][0], self.lasers[i][1]])
            laser_start_direction = np.array([self.lasers[i][2], self.lasers[i][3]])
            laser_propagate(laser_start, laser_start_direction, board, path=path)

        return path

    def put_block(self, block_pos, block_type):
        '''
        A function that put block on a specific position of the board.
        
        **Parameters**
        
            block_pos: *list, int*
                The position on the board want to put block.
            block_type: *str*
                One of three different types of block.
                Possible value are 'A', 'B' or 'C'.
                'A' -- reflect block
                'B' -- opaque block
                'C' -- refract block
                
        **Returns**
        
            self.grid: *list*
                A matrix describe the board.
            self.blocks: *dict*
                The updated blocks set after putting block on board.
        '''
        
        self.blocks[block_type] -= 1
        if self.blocks[block_type] == 0:
           del self.blocks[block_type] 
        self.grid[block_pos[1]][block_pos[0]] = block_type # adjust by WG
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
                'A' -- reflect block
                'B' -- opaque block
                'C' -- refract block
                
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

    def copy(self):
        """
        Make a copy of the board state
        Add by WG
        """
        bs = BoardStatus(
            self.grid,
            self.lasers,
            self.blocks,
            self.points
        )
        return bs

    def print_status(self):
        """
        Print the current board status
        :return:
        Add by WG
        """
        print 'Board Condition:'
        for x in self.grid:
            print x

        print ''
        print 'Laser Start Coordinate, Dirction:'
        print self.lasers
        print ''
        print 'Blocks Remain:'
        print self.blocks
        print ''
        print 'Destination Coordinates'
        print self.points
        return None

        
if __name__ == '__main__':
    
    # Test code for BoardStatus class
    f = "test"
    filename = "../Lazor_board/{}.bff".format(f)
    grid, lasers, blocks, points = read_lazor_board(filename)
    bs = BoardStatus(grid, lasers, blocks, points)

    print bs.laser_pathway()
