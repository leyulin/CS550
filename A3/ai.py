"""
Created on March 13, 2020

@author1: leyu_lin(Jack)
@author2: Parth_Thummar

ai module
implement a concrete Strategy class and AlphaBetaSearch
"""
import math

import abstractstrategy


class Strategy(abstractstrategy.Strategy):
    weights = [5, 100, 1]
    # kings,distance to king or at some spots in board,pieces

    def __init__(self, maxplayer, game, maxplies):
        super(Strategy, self).__init__(maxplayer, game, maxplies)
        self.ABSearch = AlphaBetaSearch(self, maxplayer, self.minplayer, self.maxplies)

    def utility(self, board):
        player_set, otherplayer_set = self.get_evalset(board)
        # evaluate score for both players
        player_pts = sum(i * j for (i, j) in zip(player_set, self.weights))
        otherplayer_pts = sum(i * j for (i, j) in zip(otherplayer_set, self.weights))
        return player_pts - otherplayer_pts

    def eval_d2king(self, board, player, row, col):
        # evaluate distance to king
        edge_size = board.edgesize - 1
        d2king = board.disttoking(player, col)
        if row == 0 or row == edge_size or col == 0 or col == edge_size:
            return self.maxplies + d2king
        return d2king

    def get_evalset(self, board):
        d2king, pieces, kings = 0, 0, 0
        D2king, Pieces, Kings = 0, 0, 0
        # check type and counts
        for (row, col, piece) in board:
            (player, King) = board.identifypiece(piece)
            if player == board.playeridx(self.maxplayer):
                d2king += 1
                if King:
                    kings += 1
                pieces += self.eval_d2king(board, self.maxplayer, row, col)
            else:
                # other player
                D2king += 1
                if King:
                    Kings += 1
                Pieces += self.eval_d2king(board, self.minplayer, row, col)
        otherplaer_set = [Kings, D2king, Pieces]
        player_set = [kings, d2king, pieces]

        return player_set, otherplaer_set

    def play(self, board):
        # for each player find best choices
        print('%s thinking using *AI* strategy...' % self.maxplayer)
        # Returns updated board as well as resetting depth of search
        action = self.ABSearch.alphabeta(board)
        if action is None:
            return board, None
        return board.move(action), action


class AlphaBetaSearch(object):
    """
    AlphaBetaSearch ----- Example
    # Given an instance of a class derived from AbstractStrategy
    # max the red player
    # minimize black player. Search 10 plies.
    search = AlphaBetaSearch(strategy, 'r', 'b', 10)
    """
    inf = math.inf

    def __init__(self, strategy, maxplayer, minplayer, maxplies=10, verbose=False):
        """
        AlphaBetaSearch - Initialize a class capable of AlphaBetaSearch
        """
        self.strategy = strategy
        self.max_player = maxplayer
        self.min_player = minplayer
        self.max_plies = maxplies
        self.verbose = verbose

    def alphabeta(self, state):
        """  run alpha-beta from current state """
        return self.max_value(state, -self.inf, self.inf, 0)[1]  # value 0, action 1

    def max_value(self, state, alpha, beta, depth):
        val = -self.inf
        max_move = None
        terminal = state.is_terminal()
        if terminal[0] or depth > self.max_plies:
            # if is terminal state
            val = self.strategy.utility(state)
        else:
            # return value if reach max plies
            for action in state.get_actions(self.max_player):
                # check if is there a better optimal move
                min_val = self.min_value(state.move(action), alpha, beta, depth + 1)[0]
                if min_val > val:
                    val = min_val
                    max_move = action
                if val >= beta:
                    break
                else:
                    alpha = max(alpha, val)
        return val, max_move

    def min_value(self, state, alpha, beta, depth):
        min_move = None
        val = self.inf
        terminal = state.is_terminal()
        # if is terminal state
        if terminal[0]  or depth > self.max_plies:
            val = self.strategy.utility(state)
        else:
            for action in state.get_actions(self.min_player):
                # check if is there a better optimal move
                max_val = self.max_value(state.move(action), alpha, beta, depth + 1)[0]
                if max_val < val:
                    val = max_val
                    min_move = action
                if val <= alpha:
                    break
                else:
                    beta = min(beta, val)
        return val, min_move
