# Lazor Solver
A code that will automatically solve the "Lazor" game.
Author: Joan Golding, Wenhao Gao, Wenye Deng, Yuchun Wang

The input is a Lazor board with several types of blocks. To solve a level of the game, the lazor must pass through certain points and you can do this with reflective/refractive blocks. 

The Lazor Boards can be used to test the code in Python 2.7. 
The lazor boards are under the folder lazor_board as .biff files. 

Each type of block is represented by a different character. 
x = no block allowed
o = blocks allowed
A = fixed reflect block
B = fixed opaque block
C = fixed refract block

To solve we use Depth First Search and the Monte Carlo Method (MCM). 

----PROGRAMS----

(1) lazor_input.py
    Functions:
    (i) read_lazor_board - takes a file and returns the grid, laser, blocks, and points as a list 

(2) lazor_board.py
    Classes:
    (i) BoardStatus - describes the status of the game board
    Functions:
    (i) laser_pathway - finds the points the laser passes through
    (ii) board2laser - transforms coordinates from the board grid to the laser grid
    (iii) laser2board - transforms coordinates from the laser grid to the board grid
    (iv) square - checks if there are two laser points on one block
    (v) content - returns the content of the input position
    (vi) laser_propogate - propogates the laser beam
    (vii) put_block - puts a block on a specific position on the board
    (viii) delete_block - deletes a block at a specific position on the board
    (ix) copy - adds a copy of the board state 
    
(3) check.py 
    Functions:
    (i) check - check the beam of the laser, if the required point is at the end of the laser
    
(4) lazor_solver.py 
    Classes:
    (i) LazorSolver - class that gives the solution, root is the start of the board
    (ii) Node - represents each node in the game tree 
    Function:
    (i) square - checks if there are two laser points on one block
    (ii) lazor_path - all positions in lazor path
    (iii) add_child - add a child to the current node (who becomes the father node) 
    (iv) unvisited_children - finds children we haven't visited
    (v) visit - changes the "visit" status 
    (vi) expansion - finds all the possible children of a node 
    (vii) print_node - prints the node so it can be checked 
    (viii) build_tree - builds the game tree from the start node 
    (ix) solution - finds solution with Depth First Search 
    (x) print_tree - help function to visualize tree structure 
    
  ---HOW TO RUN---
  
  You can run the program either by running the lazor_solver.py file or with this code:
  
  
  if __name__ == '__main__':
  
    f = "mad_1"
    filename = "../Lazor_board/{}.bff".format(f)
    grid, lasers, blocks, points = read_lazor_board(filename)
    bs = BoardStatus(grid, lasers, blocks, points)

    root = Node(bs)

    solver = LazorSolver(root=root)
    solver.build_tree()

    solution = solver.solution()

    if len(solution) == 0:
        print 'No Solution found!'
    else:
        for node in solution:
            node.print_node(only=True)









