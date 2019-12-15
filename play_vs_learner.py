#!/usr/bin/env python3
#
"""Play a series of tic-tac-toe games between an human and an AI learner player"""
from argparse import ArgumentParser, ArgumentTypeError

import os
import sys
import random

import numpy as np

from jokettt.board import Board
from jokettt.consoleplayer import ConsolePlayer
from jokettt.learnerplayer import LearnerPlayer

# --------------------------------------------------------------------
# --------------------------------------------------------------------
def file_to_load(_x):
    """Definition of argument type for learner init data,
       a string with a pathname of a file. The file shall exist"""

    if not os.path.exists(_x):
        raise ArgumentTypeError("%s does not exist" % (_x,))
    if not os.path.isfile(_x):
        raise ArgumentTypeError("%s is not a file" % (_x,))
    return _x

# --------------------------------------------------------------------
# --------------------------------------------------------------------
def build_random_ztable_initdata():
    ztable_init = np.empty([3, 3, 2], dtype=int)
    random.seed()
    for _x in range(0, 3):
        for _y in range(0, 3):
            for _e in range(0, 2):
                ztable_init[_x][_y][_e] = random.randint(0, sys.maxsize)
    np.save('data/test', ztable_init)
    return ztable_init

# --------------------------------------------------------------------
# --------------------------------------------------------------------
def play_human_vs_ai_game(human_player, ai_player, first_ai, board):
    """Play a tic-tac-toe game between an human and an AI learner player"""
    result = 0
    print("----------------------------------------------------")
    if first_ai:
        print("  --- NEW GAME --- My turn to begin ---")
    else:
        print("  --- NEW GAME --- Your turn to begin ---")

    console_player_turn = not first_ai

    if console_player_turn:
        print('%s' % board)

    while result == 0 and board.is_not_full():

        if console_player_turn:
            _x, _y = human_player.move(board)
            _, result = board.place_pawn(_x, _y, human_player.piece)
        else:
            _x, _y = ai_player.move(board)
            _, result = board.place_pawn(_x, _y, ai_player.piece)
            result = -result

        print('%s' % board)
        console_player_turn = not console_player_turn

    print('%s' % board)

    if result < 0:
        # AI player wins
        return -1
    if result > 0:
        # Human wins
        ai_player.learn_from_defeat(board)
        return 1
    # draw
    return 0

# --------------------------------------------------------------------
# --------------------------------------------------------------------
#   ***  MAIN ***
# --------------------------------------------------------------------
# --------------------------------------------------------------------
AI_PIECE = 'x'
HUMAN_PIECE = 'o'
ALPHA_VALUE = 0.1
def main():
    """Main program: parses options, declare board and players, and
        plays a series of games"""

    # --------------------------------------------------
    # 1. PARSE COMMAND LINE ARGUMENTS
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbosity", action="count",
                        help="increase output verbosity")
    parser.add_argument("-l", "--loaddata", type=file_to_load,
                        help="load learned data from file")
    args = parser.parse_args()
    if args.verbosity:
        verbosity = args.verbosity
    else:
        verbosity = 0

    # --------------------------------------------------
    # 2. if requested, load learned data
    print("...loading data from %s" % args.loaddata)
    if args.loaddata:
        try:
            ztable_init = np.load(args.loaddata)
        except:
            print("error reading learned data from %s" % args.loaddata)
            ztable_init = build_random_ztable_initdata()
    else:
        ztable_init = build_random_ztable_initdata()

    # --------------------------------------------------
    # 3. DECLARES BOARD AND PLAYERS
    board = Board(AI_PIECE, HUMAN_PIECE, ztable_init)
    auto_player = LearnerPlayer(AI_PIECE, board, ALPHA_VALUE, verbosity)
    console_player = ConsolePlayer(HUMAN_PIECE, verbosity)

    # --------------------------------------------------
    # 4. PLAYS!
    first_ai = False   # first move of first game is for human
    while True:
        board.reset()

        res = play_human_vs_ai_game(console_player, auto_player, first_ai, board)

        if res < 0:
            print("You lose! :-D")
        elif res > 0:
            print("You win!! :-(")
        else:
            print("Draw! ;-)")

        # change turn
        first_ai = not first_ai

if __name__ == "__main__":
    main()
