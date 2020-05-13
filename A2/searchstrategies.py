"""
Created on Feb 23, 2020

@author1: leyu_lin(Jack)
@author2: Parth_Thummar

searchstrategies

Module to provide implementations of g and h for various search strategies.
In each case, the functions are class methods as we don't need an instance
of the class.

Contains g and h functions for:
BreadFirst - breadth first search
DepthFirst - depth first search
Manhattan - city block heuristic search.  To restrict the complexity of
    this, you only need handle heuristics for puzzles with a single solution
    When multiple solutions are allowed, the heuristic becomes a little more
    complex as the city block distance must be estimated to each possible solution
    state.
"""
from basicsearch_lib02.searchrep import Node
from basicsearch_lib02.tileboard import TileBoard


class BreadthFirst:
    @classmethod
    def g(cls, parent_node, action, child_node):
        return len(child_node.path())

    @classmethod
    def h(cls, state):
        return 0


# ∀𝑛 𝑔(n) = k and h = -depth(n)
# reverse role of g and h
class DepthFirst:
    @classmethod
    def g(cls, parent_node, action, child_node):
        return (parent_node.depth + 1) * -1

    @classmethod
    def h(cls, state: TileBoard):
        return 0


class Manhattan:
    @classmethod
    def g(cls, parent_node, action, child_node):
        return parent_node.depth + 1

    @classmethod
    def h(cls, state: TileBoard):
        manhattan_distance = 0
        goal_state = list(state.goals[0])
        size = state.boardsize
        # calculate misplacement tiles
        # h = |x1 − x2| + |y1 − y2|
        # for index above board mod board_size will get cols
        # for index above board divide board_size will get rows
        for row in range(size):
            for col in range(size):
                # not count the blank for misplacement
                if state.get(row, col) is not None:
                    val_rc = state.get(row, col)
                    idx = goal_state.index(val_rc)
                    if idx > size - 1:
                        manhattan_distance += abs(idx // size - row) + abs(idx % size - col)
                    else:
                        manhattan_distance += row + abs(idx - col)
        return manhattan_distance
