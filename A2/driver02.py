"""
Created on Feb 23, 2020

@author1: leyu_lin(Jack)
@author2: Parth_Thummar

driver for graph search problem
"""
import re
import time
from statistics import (mean, stdev)  # Only available in Python 3.4 and newer

import pandas as pd
from tabulate import tabulate

from basicsearch_lib02.tileboard import TileBoard
from npuzzle import NPuzzle
from problemsearch import graph_search
from searchstrategies import (BreadthFirst, DepthFirst, Manhattan)

num_puzzle = 31
board_size = 8
search_method = [BreadthFirst, DepthFirst, Manhattan]

# output configuration
debug = False
verbose = False


class Timer:
    """Timer class
    Usage:
      t = Timer()
      # figure out how long it takes to do stuff...
      elapsed_s = t.elapsed_s() OR elapsed_min = t.elapsed_min()
    """

    def __init__(self):
        "Timer - Start a timer"
        self.s_per_min = 60.0  # Number seconds per minute
        self.start = time.time()

    def elapsed_s(self):
        "elapsed_s - Seconds elapsed since start (wall clock time)"
        return time.time() - self.start

    def elapsed_min(self):
        "elapsed_min - Minutes elapsed since start (wall clock time)"

        # Get elapsed seconds and convert to minutes
        return self.elapsed_s() / self.s_per_min


def driver():
    print("-------------------------- TileBoard searching...-----------------------------------")
    # declarations
    path_length = dict()
    num_nodes = dict()
    elapsed_sec = dict()
    elapsed_min = dict()

    for method in search_method:
        path_length[method] = list()
        num_nodes[method] = list()
        elapsed_sec[method] = list()
        elapsed_min[method] = list()

    for i in range(num_puzzle):
        print('\n###Puzzle %d###' % (i + 1))

        for method in search_method:
            if method.__name__ is 'Manhattan':
                name = 'A*'
            else:
                name = method.__name__
            print('Solving puzzle using %s' % name)


            # set the puzzle
            npuzzle = NPuzzle(board_size, g=method.g, h=method.h,
                              force_state=TileBoard(board_size).state_tuple())
            t = Timer()
            # (1,2,3,None,4,6,7,5,8) solve in 3 moves

            """--------------------One Path Demo using A---------------------------*  
            temp = False
            if method.__name__ is 'Manhattan':
                temp = True
            path, nodes_explored = graph_search(npuzzle, debug=False, verbose=temp)
            ----------------------------------------------------------------------"""
            path, nodes_explored = graph_search(npuzzle, debug=False, verbose=False)

            if method.__name__ is 'Manhattan':
                name = "A*"
            else:
                name = method.__name__
            print('Puzzle Solved in %d sec or  %d min' % (t.elapsed_s(), t.elapsed_min()))

            assert path is not None
            path_length[method].append(len(path))
            num_nodes[method].append(nodes_explored)
            elapsed_sec[method].append(t.elapsed_s())
            elapsed_min[method].append(t.elapsed_min())

    # use pandas tabulate and print table pretty
    data = list()

    # round 2digit and formatting
    for method in search_method:
        if method.__name__ is 'Manhattan':
            name = 'A*'
        else:
            name = method.__name__
        # create list according to column names
        data.append([' '.join(re.sub('(?!^)([A-Z][a-z]+)', r' \1', name).split()),
                     '{:.2f} / {:.2f}'.format(mean(path_length[method]), stdev(path_length[method])),
                     '{:.2f} / {:.2f}'.format(mean(num_nodes[method]), stdev(num_nodes[method])),
                     '{:.2f} / {:.2f}'.format(mean(elapsed_sec[method]), stdev(elapsed_sec[method])),
                     '{:.2f} / {:.2f}'.format(mean(elapsed_min[method]), stdev(elapsed_min[method]))])

    df_data = pd.DataFrame(data)
    df_data.columns = ['Search Type',
                       'Path_Length (Mean/Stdev)',
                       'Node_Explored (Mean/Stdev)',
                       'Time in Sec(Mean/Stdev)',
                       'Time in Min(Mean/Stdev)']

    pd_tabulate = lambda df_data: tabulate(df_data, headers='keys', tablefmt='psql')
    print(pd_tabulate(df_data))


if __name__ == '__main__':
    driver()
