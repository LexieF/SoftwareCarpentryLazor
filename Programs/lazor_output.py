#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 12:28:29 2019

@author: Wenye Deng
"""
from lazor_input import *
from lazor_board import *
from lazor_solver import *


def lazor_board_solution_output(f_name):    
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
    filename_list = ["dark_1", "mad_1", "mad_4", "mad_7", "numbered_6", "showstopper_4", "tiny_5", "yarn_5"]
    for f_name in filename_list:
        lazor_board_solution_output(f_name)



