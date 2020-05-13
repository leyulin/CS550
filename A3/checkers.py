"""
Created on March 13, 2020

@author1: leyu_lin(Jack)
@author2: Parth_Thummar
"""
# Python cand load compiled modules using the imp module (deprecated)
# We'll format the path to the tonto module based on the
# release of Python.  Note that we provided tonto compilations for Python 3.7
# and 3.8.  If you're not using one of these, it won't work.
import imp
import ai
import sys
from statistics import (mean)

# Game representation and mechanics
import checkerboard
# human - human player, prompts for input
import human
from timer import Timer
import boardlibrary
# tonto - Professor Roch's not too smart strategy
# You are not given source code to this, but compiled .pyc files
# are available for Python 3.7 and 3.8 (fails otherwise).
# This will let you test some of your game logic without having to worry
# about whether or not your AI is working and let you pit your player
# against another computer player.
#
# Decompilation is cheating, don't do it.  Big sister is watching you :-)

major = sys.version_info[0]
minor = sys.version_info[1]
modpath = "__pycache__/tonto.cpython-{}{}.pyc".format(major, minor)
tonto = imp.load_compiled("tonto", modpath)


def Game(red=human.Strategy, black=tonto.Strategy,
         maxplies=10, init=None, verbose=True, firstmove=0):
    """Game(red, black, maxplies, init, verbose, turn)
    Start a game of checkers
    red,black - Strategy classes (not instances)
    maxplies - # of turns to explore (default 10)
    init - Start with given board (default None uses a brand new game)
    verbose - Show messages (default True)
    firstmove - Player N starts 0 (red) or 1 (black).  Default 0.
    """

    # Don't forget to create instances of your strategy,
    # e.g. black('b', checkerboard.CheckerBoard, maxplies)

    print("How about a nice game of checkers?")
    if init is not None:
        board = init
    else:
        board = checkerboard.CheckerBoard()
    red_player = red('r', board, maxplies)
    black_player = black('b', board, maxplies)
    turn = firstmove
    moves = 0
    players = [red_player, black_player]
    game_time = Timer()
    winner = None
    rplayer_time = list()
    bplayer_time = list()
    while not board.is_terminal()[0]:
        if turn == 0:
            print("Player r turn\n", board)
            red_time = Timer()
            board, action = red_player.play(board)
            if action is None:
                winner = 'b'
                break
            if verbose:
                print("Move {} by r: {}  Result: ".format(moves, board.get_action_str(action)))
                moves += 1
                print(board)
                print("Pawn/King count: r {} R {} b {} B {} Time - move: {:.0f}s / game: {:.1f}min".format(
                    board.get_pawnsN()[0], board.get_kingsN()[0], board.get_pawnsN()[1],
                    board.get_kingsN()[1], red_time.elapsed_s(), game_time.elapsed_min()))
                print("Moves since last capture {} last pawn advance {}".format(
                    moves - board.lastcapture, moves - board.lastpawnadvance))
                if action is None:
                    print("Player r has Forfeited")
            rplayer_time.append(red_time.elapsed_s())
        else:
            print("Player b turn\n", board)
            black_time = Timer()
            board, action = black_player.play(board)
            if action is None:
                winner = 'r'
                break
            if verbose:
                print("Move {} by b: {}  Result: ".format(moves, board.get_action_str(action)))
                moves += 1
                print(board)
                print("Pawn/King count: b {} R {} b {} B {} Time - move: {:.0f}s / game: {:.1f}min".format(
                    board.get_pawnsN()[0], board.get_kingsN()[0], board.get_pawnsN()[1],
                    board.get_kingsN()[1], black_time.elapsed_s(), game_time.elapsed_min()))
                print("Moves since last capture {} last pawn advance {}".format(
                    moves- board.lastcapture, moves - board.lastpawnadvance))
            bplayer_time.append(black_time.elapsed_s())
        turn = (turn + 1) % 2
    # determine each state and print out output
    if board.is_terminal()[0]:
        print("Final Board")
        print(board)
        winner = board.is_terminal()[1]
        if winner is None:
            print("Game is a draw")
            print("r Average move time: {:.2f}s".format(mean(rplayer_time)))
            print("b Average move time: {:.2f}s".format(mean(bplayer_time)))
        else:
            print("Player {} WINS!!! ".format(winner))
    else:
        print("player Forfeit - {} wins!".format(winner))


if __name__ == "__main__":
    # ai against tonoto
    Game(red=ai.Strategy, black=tonto.Strategy, maxplies=3, firstmove=0)
    # Manual play
    #Game(init = boardlibrary.boards["EndGame1"])
    # ez game
    #Game(red=ai.Strategy, black=tonto.Strategy, init = boardlibrary.boards["EndGame1"],firstmove=0)