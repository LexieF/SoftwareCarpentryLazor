# Lazor Solver
A code that will automatically solve the "Lazor" game.
Author: Joan Golding, Wenhao Gao, Wenye Deng, Yuchun Wang

The input is a Lazor board with several types of blocks. To solve a level of the game, the lazor must pass through certain points and you can do this with reflective/refractive blocks. 

The Lazor Boards can be used to test the code in Python 2.7. 

To solve we use:

(1) lazor_input - reads the input of the lazor board, separates them into each component: blocks, points (that the lazor must pass through), and the initial lazor path. 
(2) lazor_solver - solves the board using Depth First Search and the Monte Carlo Method (MCM). 

There are several classes:

(1) Nodes - these are the nodes for the game tree and identifies both the father node and children nodes. The root node is the start of the board.  
(2) LazorSolver - gives the solution of the board 



