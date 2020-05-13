"""
Created on Apr 11, 2020

@author1: leyu_lin(Jack)
@author2: Parth_Thummar

"""
from backtrack import backtracking_search
from constraint_prop import AC3
from csp_lib.backtrack_util import mrv
from csp_lib.sudoku import (Sudoku)


def play():
    #  get from sudoku.py
    easy1 = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    harder1 = '4173698.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'

    for puzzle in [easy1, harder1]:
        # for puzzle in [easy1]:
        s = Sudoku(puzzle)
        # Initial sudoku state
        print("\nInitial problem:")
        s.display(s.infer_assignment())

        # The state of the puzzle after running AC3.
        AC3(s)
        if s.goal_test(s.curr_domains):
            print("\nAfter AC3 constraint propagation\n")
            s.display(s.infer_assignment())

        # if goal test fail try to find solution
        elif not s.goal_test(s.curr_domains):
            # run back track search
            solution = backtracking_search(s, select_unassigned_variable=mrv)
            if solution:
                print("\nSolved using backtracking:")
                s.display(s.infer_assignment())
            else:
                print("\nCould not be solved using backtrack\n")
                s.display(s.infer_assignment())


if __name__ == "__main__":
    play()
