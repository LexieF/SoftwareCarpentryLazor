#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This file is used to write the output files
which contains the solution of the corresponding data files

Created on Wed Apr 17 12:28:29 2019

@author: Wenye Deng
"""
from lazor_input import *
from lazor_board import *
from lazor_solver import *


def lazor_board_solution_output(f_name):
    """
    The function write the related soulution of a certain data file
    into a text file
    
    **Parameters**
    
        f_name: *str*
            The filename of the data file that want to get a solution
            This filename should not include the path infomation
    
    **Returns**
    
        None
    """
    filename = "../Lazor_board/{}.bff".format(f_name)
    grid, lasers, blocks, points = read_lazor_board(filename)
    bs = BoardStatus(grid, lasers, blocks, points)

    root = Node(bs)
    root.print_node()

    solver = LazorSolver(root=root)
    solver.build_tree()
    solution = solver.solution()
    
    f = open("../Outputs/{}_solution.txt".format(f_name), "w")
    
    f.write("The {} file has {} solution(s)\n\n".format(f_name, len(solution)))
    for i, sol in enumerate(solution):
        f.write("Solution {}\n".format(i+1))
        for l in sol.board_status.grid:
            f.write(" ".join(item for item in l))
            f.write("\n")
        f.write("\n")

if __name__ == "__main__":
    # write the solution text file of the corresponding given files
    filename_list = ["dark_1", "mad_1", "mad_4", "mad_7", "numbered_6", "showstopper_4", "tiny_5", "yarn_5"]
    for f_name in filename_list:
        lazor_board_solution_output(f_name)



