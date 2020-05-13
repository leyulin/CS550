"""
Created on Feb 23, 2020

@author1: leyu_lin(Jack)
@author2: Parth_Thummar
"""

from basicsearch_lib02.searchrep import Problem
from basicsearch_lib02.tileboard import TileBoard


class NPuzzle(Problem):
    """
    NPuzzle - Problem representation for an N-tile puzzle
    Provides implementations for Problem actions specific to N tile puzzles.
    """

    def __init__(self, n, force_state=None, **kwargs):
        """"__init__(n, force_state, **kwargs)

        NPuzzle constructor.  Creates an initial TileBoard of size n.
        If force_state is not None, the puzzle is initialized to the
        specified state instead of being generated randomly.

        The parent's class constructor is then called with the TileBoard
        instance any any remaining arguments captured in **kwargs.
        """
        super().__init__(TileBoard(n, force_state=force_state),
                         g=kwargs['g'], h=kwargs['h'])

    def actions(self, state):
        "actions(state) - find a set of actions applicable to specified state"
        return state.get_actions()

    def result(self, state, action):
        "result(state, action)- apply action to state and return new state"
        return state.move(action)

    def goal_test(self, state):
        "goal_test(state) - Is state a goal?"
        return state.solved()
