#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: Joan Golding, Wenhao Gao

This file defines a check function that check if we can win the game
"""
from lazor_input import *
from lazor_board import *


def check(board_status):
	"""
	check the beam of the lazor
	check if the destination point is on the beam of the lazor
	if the beam meets all the required points, return True
	if not, return False and it goes back to the
	expansion function
	"""
	check = []
	path = board_status.laser_pathway()
	for points in board_status.points:
		marker = False
		for x in path:
			if all([x[i] == points[i] for i in range(len(x))]):
				marker = True
		check.append(marker)	

	if all(check):
		return True
	else:
		return False 


if __name__ == "__main__":
	f = "test"
	filename = "../Lazor_board/{}.bff".format(f)
	grid, lasers, blocks, points = read_lazor_board(filename) 
	board_status = BoardStatus(grid, lasers, blocks, points)
	print check(board_status)
	


