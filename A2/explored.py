'''
"""
Created on Feb 23, 2020

@author1: leyu_lin(Jack)
@author2: Parth_Thummar
'''


# hash the state
class Explored(object):
    "Maintain an explored set.  Assumes that states are hashable"

    def __init__(self):
        "__init__() - Create an empty explored set"
        self.set = {}

    def exists(self, state):
        """exists(state) - Has this state already been explored?
        Returns True or False, state must be hashable
        """
        try:
            return state in self.set[hash(state)]
        except KeyError:
            return False

    def add(self, state):
        """add(state) - add given state to the explored set.
        state must be hashable and we asssume that it is not already in set
        """
        # if not same key modify set add the new key
        if hash(state) not in self.set:
            self.set[hash(state)] = set()
        # add state in same key in dictionary avoid collisions
        self.set[hash(state)].add(state)
