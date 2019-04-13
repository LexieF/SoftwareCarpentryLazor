#!/bin/python
"""
Created on Tue Apr 9 2019

@author: Wenhao Gao, Joan Golding

This file defines three class:
    LazorSolver(Root_Node): Class that provide the solution
    Node
    and some help functions
"""
from lazor_input import *
from lazor_board import *
from check import check
import numpy as np
import random


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
        """
        bs = self.board_status
        path = lazor_path(bs)
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
                # node.print_node()
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
        solve = False
        for node in candidates:
            node.print_node()
            if check_func(node.board_status):
                return node

        if not solve:
            return None

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


if __name__ == '__main__':
    f = "mad_4"
    filename = "../Lazor_board/{}.bff".format(f)
    grid, lasers, blocks, points = read_lazor_board(filename)
    bs = BoardStatus(grid, lasers, blocks, points)

    root = Node(bs)

    solver = LazorSolver(root=root)
    solver.build_tree()

    solution = solver.solution()
    if solution is None:
        print 'No Solution found!'
    else:
        solution.print_node(only=True)
