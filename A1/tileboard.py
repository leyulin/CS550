"""
Created on Feb 9, 2020

@author1: leyu_lin(Jack)
@author2: Parth_Thummar

Description: Create a tile board for an n puzzle. The board initialized by init_board() check odd/even rows columns
set flag next use shuffle() to make sure is solvable Then use populate() place shuffled list to board
also track blank location pass to tuple blank_ix. Player can use get_actions() find possible moves,
call move() to move and get new_board if single solution lower right is the goal state or solved
else None can be anywhere is the goal state or solved if slide is even or middle is blank only lower right
is the solution. self.goals() will set solution tuple and compare if puzzle is solved()

goal_state: multiple to False only  lower right
            multiple to true none can be any where
"""

import copy
import math
import random

from basicsearch_lib.board import Board


class TileBoard(Board):
    blank_ix = (0, 0)  # the tuple store blank location

    def __init__(self, n, multiple_solutions=False, force_state=None,
                 verbose=False):
        """"
        Create a tile board for an n puzzle.
        """
        self.multiple_solutions = multiple_solutions
        self.verbose = verbose  # not debug state, up to you to use it
        self.size = n + 1
        self.board_size = int(math.sqrt(self.size))
        if math.sqrt(self.size) != self.board_size:
            raise ValueError("Bad board size\n" + "Must be one less than an odd perfect square 8, 24, ...")
        # initialize parent
        super().__init__(self.board_size, self.board_size)

        if force_state is None:
            # create random board that is solvable
            self.init_board()
            # check if the number of rows and columns are even
            # Set goal state
            self.goals()
        else:
            # if there is force_state place to board
            self.board = self.populate(force_state)

    def populate(self, item):
        """
        place item from list to the board one by one
        return: the updated board with item placed
        """
        for cnt, item in enumerate(item):
            rows = cnt // super().get_rows()
            cols = cnt % super().get_cols()
            self.place(rows, cols, item)
            if self.board[rows][cols] is None:
                self.blank_ix = (rows, cols)
        return self.board

    def solvable(self, tiles, verbose=False):
        """solvable - Determines if a puzzle is solvable"""
        inversion_order = 0
        # Make life easy, remove None
        reduced = [t for t in tiles if t is not None]
        # Loop over all but last (no tile after it)
        for idx in range(len(reduced) - 1):
            value = reduced[idx]
            after = reduced[idx + 1:]  # Remaining tiles
            smaller = [x for x in after if x < value]
            num_tiles = len(smaller)
            inversion_order = inversion_order + num_tiles
            if verbose:
                print("idx {} value {} tail {} #smaller {} sum: {}".format(
                    idx, value, after, num_tiles, inversion_order))

        # Even number of rows must take the blank position into account
        if self.get_rows() % 2 == 0:
            if verbose:
                print("Even # rows, adding for position of blank")
            inversion_order = inversion_order + \
                              math.floor(tiles.index(None) / self.board_size) + 1

        solvable = inversion_order % 2 == 0  # Solvable if even
        return solvable

    def __hash__(self):
        "__hash__ - Hash the board state"
        # Convert state to a tuple and hash
        return hash(self.state_tuple())

    def __eq__(self, other):
        "__eq__ - Check if objects equal:  a == b"
        # check if different board size
        if self.board_size != other.boardsize:
            return False
        # same size
        else:
            return self.board == other.board

    def state_tuple(self):
        "state_tuple - Return board state as a single tuple"
        board_list = []
        for i in range(self.get_rows()):
            for j in range(self.get_cols()):
                board_list.append(self.get(i, j))
        return tuple(board_list)

    def get_actions(self):
        """
        find all possible location blank can go add to the list
        if there is no wall or sides in all four directions just move respectively
        return: row column offsets of where the empty tile can be moved"
        """
        wall = self.board_size - 1
        self.board = self.populate(list(self.state_tuple()))
        current_cols = self.blank_ix[1]
        current_rows = self.blank_ix[0]
        list_valid_actions = []

        # go left if left is not reach sides
        if current_cols is not 0:
            list_valid_actions.append([0, -1])
        # go right if left is not reach sides
        if current_cols is not wall:
            list_valid_actions.append([0, 1])
        # go up if up is not reach sides
        if current_rows is not 0:
            list_valid_actions.append([-1, 0])
        # go Down if Down is not reach sides
        if current_rows is not wall:
            list_valid_actions.append([1, 0])
        return list_valid_actions

    def init_board(self):
        """
        Set the middle to be empty always
        but if is not solvable shuffle it
        """
        temp_list = list(range(1, self.size))
        temp_list.append(None)
        # shuffle initial state
        random.shuffle(temp_list)
        self.board = self.populate(temp_list)
        # shuffle the board till can be solvable
        while not self.solvable(self.state_tuple()) and not self.solved():
            self.shuffle()
        # populate to get new board
        self.board = self.populate(temp_list)

    def shuffle(self):
        """
        random change value create a new list, in order to change inversion order value
        to be solvable and pop from the new list to setup newboard
        """
        list_board = list(self.state_tuple())
        random.shuffle(list_board)
        self.board = self.populate(list_board)

    def move(self, offset):
        "move - Move the empty space by [delta_row, delta_col] and return new board"
        # check valid offset
        if offset not in self.get_actions() or offset is None:
            return self
        # deep copy the instance
        new_board = copy.deepcopy(self)

        # get index need to move add to current location tuple
        cols = self.blank_ix[1] + offset[1]  # move cols
        rows = self.blank_ix[0] + offset[0]  # move rows
        # put the new blank location
        new_board.board[rows][cols] = None
        # get old value from old board to the  blank location
        new_board.board[self.blank_ix[0]][self.blank_ix[1]] = self.board[rows][cols]
        return new_board

    def solved(self):
        """
        # solved depend single/multiple goal_state compare with self.gaols
        :return: boolean Checks to see if the tile board is solved or not.
        """
        goal_state = self.goals()
        if self.multiple_solutions is False:
            current_list = list(self.state_tuple())
        elif self.multiple_solutions is True:
            current_list = [i for i in self.state_tuple() if i is not None]
            return current_list == list(goal_state)

    def goals(self):
        """
         "Multiple solution None can be any where"
        # so we compare two lists
        # first one we just made from 1 to size which is n+1
        # first list is the goal state
        # second list we get each elements from current state tuple to list
         "Single Solution Only check the lower right one which is board_size -1"
        :return:  set goal_state tuple
        """
        temp_list = list(range(1, self.size))
        if not self.multiple_solutions:
            temp_list.append(None)
        goal_state = tuple(temp_list)
        return goal_state
