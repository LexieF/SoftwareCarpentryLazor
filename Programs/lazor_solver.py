#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This file defines three class:
    LazorSolver(Root_Node): Class that provide the solution
    Node and some help functions

Created on Tue Apr 9 2019

@author: Wenhao Gao, Joan Golding, Wenye Deng

"""
from lazor_input import *
from lazor_board import *
from check import check
import numpy as np
import time

class Node:
    """
    class that represent a node in a tree
    Each node represent a game step
    Its father node is last step
    Its children nodes are possible nest steps
    The board status represent the board content in this step
    """
    def __init__(self, board_status, father=None, depth=None):
        """
        Initialization of a node according to a board status
        Unless root node, we should specify father node

        :param board_status: *class BoardStatus*
            the board status in this node

        :param father: *class Node*
            father node

        :param depth: *int*
            depth, maximum is the number of blocks can be placed
        """
        self.board_status = board_status
        if depth is None:
            self.depth = 0
        else:
            self.depth = depth
        self.visit = False # initial status is unvisited
        self.children = [] # initial status is no child
        self.father = father

    def add_child(self, board_status, verbose=True):
        """
        Add a child node whose father node is this to this node

        :param board_status: *class BoardStatus*
            the board_status of child node

        :return: None
        """
        children_board = [x.board_status.grid for x in self.children]
        if board_status.grid not in children_board:
            node = Node(board_status, self, depth=(self.depth + 1))
            self.children.append(node)
        else:
            if verbose:
                print 'This child is already added.'
        return None

    def unvisited_children(self):
        """
        Return a list of unvisited children
        """
        unvisited_children = []
        for x in self.children:
            if not x.visit:
                unvisited_children.append(x)
        return unvisited_children

    def visit(self):
        """
        Function to change the visit status when visit.
        """
        self.visit = True
        return None

    def expansion(self):
        """
        Construct all possible children node of this node
        On laser path
        """
        bs = self.board_status
        path = lazor_path(bs)
        for block in bs.blocks.keys():
            for position in path:
                bs_ = bs.copy()
                bs_.put_block(position, block)
                self.add_child(bs_, verbose=False)
        return None

    def non_laser_path_expansion(self):
        """
        Construct all possible node of this node
        """
        bs = self.board_status
        path = non_lazor_path(bs)
        for block in bs.blocks.keys():
            for position in path:
                bs_ = bs.copy()
                bs_.put_block(position, block)
                self.add_child(bs_, verbose=False)
        return None

    def print_node(self, only=False, verbose=False):
        """
        Print out the information of node to check.

        :param verbose: *Boolean*
            if True, print out all children node

        :param only: *Boolean*
            if True, only print out current game board

        :return: None
        """
        print 'Node content:'
        self.board_status.print_status()
        print ''

        if not only:
            print 'Node Status:'
            if self.visit:
                print 'Visited'
            else:
                print 'Unvisited'

            print ''

            if self.father is None:
                print 'No father Node for Root Node'
            else:
                print 'Father node content:'
                self.father.board_status.print_status()
            print ''
            print 'Children number:'
            print len(self.children)
            print ''
            print 'Unvisited Children number:'
            uvc = self.unvisited_children()
            print len(uvc)

        if verbose:
            print 'Children content:'
            for x in self.children:
                x.board_status.print_status()
                print ''

        return None


class LazorSolver:
    """
    class that give the solution of a lazor
    Its root node is the start board
    """
    def __init__(self, root):
        """
        Initialization of search tree

        :param root: *class Node*
            the starting board node
        """
        self.root = root

        # calculate the maximum depth of the tree
        self.max_depth = sum(self.root.board_status.blocks.values())

        # The tree list that store the nodes in their corresponding depth
        self.tree = [[] for i in range(self.max_depth + 1)]
        self.tree[0].append(root)

    def build_tree(self):
        """
        Function that build a tree from a root node
        For each layer, apply expansion function to every nodes
        """
        for i in range(self.max_depth + 1):
            layer = self.tree[i]
            for node in layer:
                # for q in node.board_status.grid:
                #     print q
                # print node.board_status.laser_pathway()
                node.expansion()
                # print 'complete expansion'
                children = node.children
                for child in children:
                    self.tree[i + 1].append(child)
            #         print 'Add a child node'
            #
            #     print 'Complete one node'
            #     print ''
            print 'complete layer %i' % i
            if i < self.max_depth:
                print 'The number of nodes in last layer is %i' % len(self.tree[i + 1])
                print '----------------------------------------------------------------------------------------------'
                print ''

        print 'Finish building the tree!'
        print '----------------------------------------------------------------------------------------------'

        return None

    def solution(self, check_func=check):
        """
        Function that find the solution to this lazor problem
        Depth first search algorithm is applied

        :param check_func: *function*
            Function that judge if we can win

        :return: *class BoardStatus*
            The solution to this problem
        """
        candidates = self.tree[-1]
        solutions = []
        for node in candidates:
            #node.print_node()
            if check_func(node.board_status):
                solution_grids = [node_.board_status.grid for node_ in solutions]
                if node.board_status.grid not in solution_grids:
                    solutions.append(node)

        # If no solution found, there is blocks that block the laser beam, which is redundant
        # Back propagate from bottom and found a subset that can win the game
        # Then use non_laser_beam_expansion to the node
        marker = 1
        while True:
            if len(solutions) != 0:
                break

            marker += 1
            for node in self.tree[-marker]:
                node.non_laser_path_expansion()
                for child in node.children:
                    if check_func(child.board_status):
                        solution_grids = [node_.board_status.grid for node_ in solutions]
                        if child.board_status.grid not in solution_grids:
                            solutions.append(child)

        # expansion from pre-solution
        temp = []
        for i in range(marker - 2):
            for node in solutions:
                node.non_laser_path_expansion()
                for child in node.children:
                    if check_func(child.board_status):
                        temp_grids = [node_.board_status.grid for node_ in temp]
                        if child.board_status.grid not in temp_grids:
                            temp.append(child)
            solutions = temp

        return solutions

    def print_tree(self):
        """
        Help function, to visualize the tree structure
        """
        for i in range(self.max_depth + 1):
            layer = self.tree[i]
            for j in range(len(layer)):
                print '-'
                print '*'
        return None

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
    L = [a, b]
    position = []
    for i in range(2):
        if L[i][0] % 2 != 0:
            position.append((L[i][0] - 1)/2)

    for i in range(2):
        if L[i][1] % 2 != 0:
            position.append((L[i][1] - 1)/2)

    diff_original = [(a[i] - b[i]) for i in range(len(a))]
    diff = [np.abs(x) == 1 for x in diff_original]
    if all(diff):
        return position
    else:
        return False

def lazor_path(board_status):
    """
    Return all positions that on the lazor pathway
    Help function to generate children

    :param board_state: *class BoardStatus*
        the board status that want to analyse

    :return: *list* with content *position list*
        list of position one can place a block
    """
    check = []
    path = board_status.laser_pathway()
    for i, a in enumerate(path):
        for j in range(i, len(path)):
            b = path[j]
            if square(a, b):
                position = square(a, b)
                if board_status.grid[position[1]][position[0]] == 'o':
                    check.append(position)
    return check

def non_lazor_path(board_status):
    """
    Return all positions that not on the lazor pathway
    Help function to generate children

    :param board_state: *class BoardStatus*
        the board status that want to analyse

    :return: *list* with content *position list*
        list of position one can place a block
    """
    check = []
    x_dim = len(board_status.grid[0])
    y_dim = len(board_status.grid)

    for i in range(x_dim):
        for j in range(y_dim):
            position = [i, j]
            if board_status.grid[position[1]][position[0]] == 'o':
                check.append(position)
    return check

def lazor_run(f_name):
    filename = "../Lazor_board/{}.bff".format(f_name)
    grid, lasers, blocks, points = read_lazor_board(filename)
    bs = BoardStatus(grid, lasers, blocks, points)

    print "{}:".format(f_name)
    
    root = Node(bs)
    root.print_node()

    solver = LazorSolver(root=root)
    solver.build_tree()    
    solution = solver.solution()

    if len(solution) == 0:
        print 'No Solution found!'
    else:
        for node in solution:
            node.print_node(only=True)
            print '----------------------------------------------------------------------------------------------'


if __name__ == '__main__':
    filename_list = ["dark_1", "mad_1", "mad_4", "mad_7", "numbered_6", "showstopper_4", "tiny_5", "yarn_5"]
    for f in filename_list:
        
        time1 = time.time()
        
        lazor_run(f)
    
        time2 = time.time()
        dt = time2 - time1
    
        print 'Total time consumed: %.1f\n' % dt
