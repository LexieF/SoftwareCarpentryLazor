#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This file defines the class BoardStatus(grid, lasers, blocks, points)
which describes a certain status of the game.

Created on Thu Mar 28 23:41:11 2019

@author: Wenye Deng, Yuchun Wang, Wenhao Gao

"""
import numpy as np
from copy import deepcopy
from lazor_input import *


class BoardStatus():
    """
    A class describe the status of the game board.
    
    **Method**
    
        laser_pathway(self)
        put_block(self, block_pos, block_type)
        delete_block(self, block_pos, block_type)
        print_status(self)
        print_status(self)
    """
    def __init__(self, grid, lasers, blocks, points):
        self.grid = deepcopy(grid)
        self.lasers = deepcopy(lasers)
        self.blocks = deepcopy(blocks)
        self.points = deepcopy(points)

    def laser_pathway(self):
        """
        Function that provide the laser pathway

        **Return**
            
            path: *list, list, int*
                List comprising all coordinates that laser would pass
        
        Add by WG
        """
        def board2laser(position):
            """
            Help function that transform the coordinates in board grid to laser grid
            
            **Parameters**
            
                position: *list, int*
                    Position in board grid
            
            **return**
                
                position: *list, int*
                    Position in laser grid
            """
            result = [0, 0]
            result[0] = position[0] * 2 + 1
            result[1] = position[1] * 2 + 1
            return result

        def laser2board(position):
            """
            Help function that transform the coordinates in laser grid to board grid
            
            **Parameters**
                
                position: *list, int*
                    Position in laser grid
            **Return**
                position: *list, int*
                    Position in board grid
            """
            result = [0, 0]
            result[0] = (position[0] - 1) / 2
            result[1] = (position[1] - 1) / 2
            return result

        def square(a, b):
            """
            Function that check if two lasor point is in one square
            Help generate legal path

            **Parameters**
                
                a: *list, int*
                Lazor point 1
                b: *list, int*
                Lazor point 2

            **Return**
                Board position that may put a block or None
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
            
            **Parameters**
            
                start_point: *list, int*
                start_direction: *list, int*
                board: *list, list, str*
                path: *list, list, int, optional*
                
            **Returns**
            
                path: *list, list, path*
            """
            point = start_point
            direction = start_direction

            x_dim = len(board[0]) * 2
            y_dim = len(board) * 2

            # Add the first point
            if start_point.tolist() not in path:
                path.append(start_point.tolist())

            trace_len_path = [i for i in range(8)]

            # Propagate the laser beam step by step
            while True:
                # Check for if the path is converged
                trace_len_path.append(len(path))
                del trace_len_path[0]
                if all([x == trace_len_path[-1] for x in trace_len_path]):
                    break

                # Check next laser point
                next = point + direction
                if next[0] == -1 or next[0] == x_dim + 1 or next[1] == -1 or next[1] == y_dim + 1:
                    break

                block_position_in_laser = square(point, next)
                block_position_in_board = laser2board(block_position_in_laser)

                # 'o' -- encounter nothing, propagate normally
                if content(board, block_position_in_board) == 'o':
                    point = next
                    if point.tolist() not in path:
                        path.append(point.tolist())
                elif content(board, block_position_in_board) == 'x':
                    point = next
                    if point.tolist() not in path:
                        path.append(point.tolist())
                # 'A' -- reflect block
                elif content(board, block_position_in_board) == 'A':
                    # Need to consider the former block
                    former = point - direction

                    # Case: block is placed at the corner or edge
                    if former[0] == -1 or former[0] == x_dim + 1 or former[1] == -1 or former[1] == y_dim + 1:
                        if point.tolist() not in path:
                            path.append(point.tolist())
                        break
                    # Case: block is placed at medium
                    else:
                        former_block_position_in_laser = square(point, former)
                        former_block_position_in_board = laser2board(former_block_position_in_laser)

                        if content(board, former_block_position_in_board) == 'o':
                            direction = direction + 2 * (point - block_position_in_laser)

                        elif content(board, former_block_position_in_board) == 'x':
                            direction = direction + 2 * (point - block_position_in_laser)

                        elif content(board, former_block_position_in_board) == 'A':
                            if point.tolist() not in path:
                                path.append(point.tolist())
                            break

                        elif content(board, former_block_position_in_board) == 'B':
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

                    if former[0] == -1 or former[0] == x_dim + 1 or former[1] == -1 or former[1] == y_dim + 1:
                        if point.tolist() not in path:
                            path.append(point.tolist())
                        laser_propagate(next, direction, board, path=path)
                    else:
                        former_block_position_in_laser = square(point, former)
                        former_block_position_in_board = laser2board(former_block_position_in_laser)

                        if content(board, former_block_position_in_board) == 'o':
                            # Normal refraction and transmission case
                            laser_propagate(
                                point, direction + 2 * (point - block_position_in_laser), board, path=path
                            )
                            laser_propagate(next, direction, board, path=path)

                        elif content(board, former_block_position_in_board) == 'x':
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

                        elif content(board, former_block_position_in_board) == 'B':
                            # Normal refraction and transmission case
                            laser_propagate(
                                point, direction + 2 * (point - block_position_in_laser), board, path=path
                            )
                            laser_propagate(next, direction, board, path=path)

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

def test_bs():
    filename = "../Lazor_board/showstopper_4.bff"
    grid, lasers, blocks, points = read_lazor_board(filename)
    bs = BoardStatus(grid, lasers, blocks, points)    
    assert bs.laser_pathway() == [[3, 6], [2, 5], [1, 4], [0, 3]], "Method laser_pathway() is incorrect"

    bs.put_block([2, 2], "A")
    assert bs.grid == [['B', 'o', 'o'], ['o', 'o', 'o'], ['o', 'o', 'A']], "Blocks didn't put in the right place"
    assert bs.blocks == {'A': 2, 'B': 3}, "Blocks set should be recounted"
    
    bs.delete_block([2, 2], "A")
    assert bs.grid == [['B', 'o', 'o'], ['o', 'o', 'o'], ['o', 'o', 'o']], "Blocks didn't delete right"
    assert bs.blocks == {'A': 3, 'B': 3}, "Blocks set should be recounted"

        
if __name__ == '__main__':
    test_bs()
    print "Everything passed"
    
    # Test code for BoardStatus class
    filename_list = ["dark_1", "mad_1", "mad_4", "mad_7", "numbered_6", "showstopper_4", "tiny_5", "yarn_5"]
    for f in filename_list:
        filename = "../Lazor_board/{}.bff".format(f)
        grid, lasers, blocks, points = read_lazor_board(filename)
        bs = BoardStatus(grid, lasers, blocks, points)
        print "The laser pathway of {} is: ".format(f)
        print bs.laser_pathway()
        print "\n"
