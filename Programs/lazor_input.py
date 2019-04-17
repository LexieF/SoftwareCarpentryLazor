#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This file contains two functions: read_lazor_board(filename) 
and its related unit test function test_read_lazor_board()

Created on Tue Mar 26 22:14:27 2019

@author: Wenye Deng
"""



def read_lazor_board(filename):
    """
    This is a input function to read the bff file
    which contains the information of grid, lasers, blocks and points
    """
    f = open(filename)
    l = f.readlines()
    f.close()
    
    l_ind = 0
    
    grid = []
    lasers = []
    blocks = {}
    points = []
    
    while l_ind < len(l):        
        # Read grid
        if l[l_ind][0] == "G":    
            s = True # s means Grid Start or Stop
            i = 1
            while s:
                temp_str = l[l_ind+i].split('\n')[0]
                while "  " in temp_str:
                    temp_str = temp_str.replace("  ", " ")
                grid.append(temp_str.split(' '))
                i += 1
                if l[l_ind+i][0] == "G":
                    l_ind += i+1
                    s = False
                    break

        # Read blocks
        elif l[l_ind][0] == "A" or l[l_ind][0] == "B" or l[l_ind][0] == "C":
            temp_str = l[l_ind].split('\n')[0]
            blocks[temp_str.split(' ')[0]] = int(temp_str.split(' ')[1])
            l_ind += 1
        
        # Read lasers
        elif l[l_ind][0] == "L":
            temp_str = l[l_ind].split('\n')[0]
            lasers.append(map(int, temp_str.split(' ')[1:5]))
            l_ind += 1
        
        # Read points
        elif l[l_ind][0] == "P":
            temp_str = l[l_ind].split('\n')[0]
            points.append(map(int, temp_str.split(' ')[1:3]))
            l_ind += 1
        
        else:
            l_ind += 1
            
    return grid, lasers, blocks, points

def test_read_lazor_board():
    """
    This is a unit test function to check the result of read_lazor_board(filename)
    """
    assert read_lazor_board("../Lazor_board/mad_1.bff")[0] == [['o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o']], "Grid read is incorrect"
    assert read_lazor_board("../Lazor_board/mad_1.bff")[1] == [[2, 7, 1, -1]], "Lasers reading is incorrect"
    assert read_lazor_board("../Lazor_board/mad_1.bff")[2] == {'A': 2, 'C': 1}, "Blocks reading is incorrect"
    assert read_lazor_board("../Lazor_board/mad_1.bff")[3] == [[3, 0], [4, 3], [2, 5], [4, 7]], "Points reading is incorrect"

# Test the read_lazor_board() function
if __name__ == "__main__":
    # Unit test
    test_read_lazor_board()
    print "Everything passed"
    
    # Print all info of the given files
    filename_list = ["dark_1", "mad_1", "mad_4", "mad_7", "numbered_6", "showstopper_4", "tiny_5", "yarn_5"]
    for f in filename_list:
        filename = "../Lazor_board/{}.bff".format(f)
        print "{}:".format(f)
        print "Grid: {}".format(read_lazor_board(filename)[0])
        print "Lasers: {}".format(read_lazor_board(filename)[1])
        print "Blocks: {}".format(read_lazor_board(filename)[2])
        print "Points: {}\n".format(read_lazor_board(filename)[3])