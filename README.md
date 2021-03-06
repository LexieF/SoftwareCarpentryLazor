# Group Project - Lazor

A code that will automatically find solutions to the "Lazor" game on Android and iPhone..

## Author

Joan Golding, Wenhao Gao, Wenye Deng, Yuchun Wang

## Hierarchy of Directory

This repository contains 3 directory, a PDF handout for Lazor project and a README file.

1. Lazor_board
    - This directory contains all the given .biff files
2. Programs
    - This directory has 5 .py files: lazor_input.py, lazor_board.py, check.py, lazor_solver.py, and lazor_output.py
    - And details about this file will be explained below
3. Outputs
    - This directory contains 8 outputs file with solution corresponding to the 8 given data file

## Getting Started

The input is a Lazor board with several types of blocks. To solve a level of the game, the lazor must pass through certain points and you can do this with reflective/refractive blocks. 
To solve we use Depth First Search and the Monte Carlo Method (MCM).

### Prerequisites

The code should be tested in Python 2.7

### PROGRAMS

1. lazor_input.py

  | **Function** | **Discription** | **Input** | **Outputs** |
  | ------------ | --------------- | --------- | ----------- |
  | read_lazor_board | read the bff file | filename | grid, lasers, blocks, points |
  | test_read_lazor_board | check the result of read_lazor_board | None | None |

2. lazor_board.py
    
  - Classes:
   
    BoardStatus - describes the status of the game board
    
  | **Method** | **Discription** | **Input** | **Outputs** |
  | ---------- | --------------- | --------- | ----------- |
  | laser_pathway | finds the points the laser passes through | self | path points |
  | put_block | puts a block on a specific position on the board | self, block_pos, block_type | self.grid, self.blocks |
  | delete_block | deletes a block at a specific position on the board | self, block_pos, block_type | self.grid, self.blocks |
  | copy | adds a copy of the board state | self | instance of BoardStatus class |
  | print_status | print the current board status | self | None |

   - Functions:
    
  | **Function** | **Discription** | **Input** | **Outputs** |
  | ------------ | --------------- | --------- | ----------- |
  | test_bs | test for BoardStatus class | None | None |

    
3. check.py 

  | **Function** | **Discription** | **Input** | **Outputs** |
  | ------------ | --------------- | --------- | ----------- |
  | check | check the beam of the lazor | instance of BoardStatus class | boolean data type |
    
4. lazor_solver.py 

  - Classes:
    
   (i) Node - represents each node in the game tree
   
  | **Method** | **Discription** | **Input** | **Outputs** |
  | ---------- | --------------- | --------- | ----------- |
  | add_child | add a child to the current node | self, board_status, verbose=True | None |
  | unvisited_children | finds children we haven't visited | self | a list of unvisited children |
  | visit | changes the "visit" status | self | None |
  | expansion | finds all the possible children of a node | self | None |
  | non_laser_path_expansion | construct all possible node of this node | self | None |
  | print_node | prints the node | self, only=False, verbose=False | None |

   (ii) LazorSolver - class that gives the solution, root is the start of the board
   
  | **Method** | **Discription** | **Input** | **Outputs** |
  | ---------- | --------------- | --------- | ----------- |
  | build_tree | builds the game tree from the start node | self | None |
  | solution | finds solution with Depth First Search | self, check_func=check | solved instance of BoardStatus class |
  | print_tree | help function to visualize tree structure | self | None |
    
   - Functions:
   
  | **Function** | **Discription** | **Input** | **Outputs** |
  | ------------ | --------------- | --------- | ----------- |
  | square | check if two lasor point is in one square | two points: a, b | board position that may put a block or False |
  | lazor_path | find all positions in lazor path | instance of BoardStatus class | list of position one can place a block |
  | non_lazor_path | find all positions not in lazor path | instance of BoardStatus class | list of position one can place a block |
    
5. lazor_output.py

  | **Function** | **Discription** | **Input** | **Outputs** |
  | ------------ | --------------- | --------- | ----------- |
  | lazor_board_solution_output | write output files | f_name | None |

    
## HOW TO RUN
  
 1. You can got the solutions directly by running the lazor_solver.py file
 
    - For all given files (on command line)
 
    ```
    python lazor_solver.py
    ```
 
    - For other new files, on any python console (please put the date file on the Laser_board directory before running the code)
  
    ```python
    import lazor_solver
    lazor_solver.lazor_run("mad_1")
    ```
    
 2. Or write out the solution into a text file
 
    - For all given files together (on command line)
  
    ```
    python lazor_output.py
    ```
    
    - For other new files, on any python console (please put the date file on the Laser_board directory before running the code)
  
    ```python
    import lazor_output
    lazor_output.lazor_board_solution_output("mad_1")
    ```
