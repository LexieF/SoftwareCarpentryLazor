from lazor_input import *
from lazor_board import *
import numpy as np
import random 

def square(a, b):
	# a, b = lazor points
	L = [a, b]
	position = []
	for i in range(2):
		if L[i][0] % 2 != 0:
			position.append(L[i][0])

	for i in range(2):
		if L[i][1] % 2 != 0:
			position.append(L[i][1])
	
	diff_original = a - b
	diff = [np.abs(x) == 1 for x in diff_original]
	if all(diff):
		return position 
	else:
		return False 

def expansion(board_state):
	'''
	Gives us all the possible points
	to put a block
	'''
	check = []
	path = board_state.laser_pathway()
	for i, a in enumerate(path):
		for j in range(i, len(path)):
			b = path[j]
			if square(a,b):
				check.append(square(a,b))
	return check 


class LazorSolver:
	'''
	Class to solve lazor by constructing
	a Monte Carlo tree search
	'''
	__init__(self, root):
		self.root = root 

	def depth_search(self, check):
		current_status = self.root
		current_depth = 0 
		while True:
			if len(current_status.children) == 0:
				legal_position = expansion(current_status)
				current_status.add_children(legal_position)
				children = curent_status.children
			else: 
				children = []
				for x in current_status.children:
					if not x.visit:
						children.append(x)


			current_status = children[rand.randit(len(current_status.children))]
			depth += 1 
			current_status.check_double()
			if check(current_status.board_state):
				return current_status.board_state
			else:
				# back propogate 
				




class Node: 
	'''
	These are the nodes of the tree
	'''
	__init__(self, board_state, depth):
	self.board_state = board_state
	self.depth = depth 
	self.children = []
	self.visit = False 

	def add_children(self, node):
		for x in node:
			self.children.append(x) 

	def father_node(self, father):
		self.father = father

	def check_double(self):
		self.visit = True 




if __name__ == "__main__":
	f = "mad_1"
	filename = "../Lazor_board/{}.bff".format(f)
	grid, lasers, blocks, points = read_lazor_board(filename) 
	board_status = BoardStatus(grid, lasers, blocks, points)
	print expansion(board_status)




