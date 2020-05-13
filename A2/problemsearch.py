"""
Created on Feb 23, 2020

@author1: leyu_lin(Jack)
@author2: Parth_Thummar

problemsearch - Functions for searching.
"""
from collections import deque

from basicsearch_lib02.queues import PriorityQueue
from basicsearch_lib02.searchrep import (Node)
from explored import Explored


def graph_search(problem, verbose=False, debug=False):
    """graph_search(problem, verbose, debug) - Given a problem representation
    attempt to solve the problem.

    Returns a tuple (path, nodes_explored) where:
    path - list of actions to solve the problem or None if no solution was found
    nodes_explored - Number of nodes explored (dequeued from frontier)
    """

    frontier = PriorityQueue()
    root = Node(problem, problem.initial)
    frontier.append(root)
    node = frontier.pop()
    pop = True # for right pop left pop for BFS

    if node.expand(node.problem)[0].g < 0:
        # DFS which has the negative depth
        # since start from the deepest node
        frontier = deque()
        frontier.append(root)
    elif node.expand(node.problem)[0].h == 2:
        # BFS
        pop = False
        frontier = deque()
        frontier.append(root)
    else:
        # Manhattan
        frontier.append(node)

    DONE = False
    nodes_explored = 0
    explored_set = Explored()
    while not DONE:
        if pop:
            node = frontier.pop() # DFS A*
        else:
            node = frontier.popleft()  # BFS
        if debug:
            print("Next decision is:", str(node))

        explored_set.add(node.state.state_tuple())
        nodes_explored += 1

        if problem.goal_test(node.state):
            solved_path = node.path()
            if debug:
                print("Puzzle solved")
                #  print("path:", str(node.path()))
            DONE = True
            # if Verbose True display the info stats in requirement
            if verbose:
                print("Solution in %d moves" % (len(solved_path) - 1))
                print("Initial State")
                print(solved_path[0])

                for i in range(1, len(solved_path)):
                    print("Move %d - %s" % (i, solved_path[i].action))
                    print(solved_path[i].state)

            return solved_path, nodes_explored
        # Not solved yet
        else:
            for child in node.expand(node.problem):
                # add new child to frontier set
                if not explored_set.exists(child.state.state_tuple()):
                    frontier.append(child)
                    explored_set.add(child)
            # finish when there is no node in the queue
            # if debug:
            #    print("Num node in quenue:", str(len(frontier)))
            DONE = len(frontier) == 0

    if verbose:
        print("No solution found")
    return None, nodes_explored
