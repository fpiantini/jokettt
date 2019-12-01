#!/usr/bin/env python3
#
"""Play a tic-tac-toe games between two AI players"""

from argparse import ArgumentParser

from tttboard import TttBoard
from tttlearnerplayer import TttLearnerPlayer
from tttminimaxplayer import TttMinimaxPlayer

# --------------------------------------------------------------------
# --------------------------------------------------------------------
def play_ai_vs_ai_game(first_player, second_player, board, verbosity_level):
    """Play a tic-tac-toe game between an human and an AI player"""
    result = 0
    if verbosity_level > 0:
        print("----------------------------------------------------")
        print("  --- NEW GAME ---")
    first_player_turn = True

    while result == 0 and board.is_not_full():

        if first_player_turn:
            _x, _y = first_player.move(board)
            _, result = board.place_pawn(_x, _y, first_player.piece)
        else:
            _x, _y = second_player.move(board)
            _, result = board.place_pawn(_x, _y, second_player.piece)
            result = -result

        if verbosity_level > 1:
            print('%s' % board)
        first_player_turn = not first_player_turn

    if verbosity_level > 1:
        print('%s' % board)

    if result > 0:
        # first player wins
        if isinstance(second_player, TttLearnerPlayer):
            second_player.learn_from_defeat(board)
        return 1
    if result < 0:
        # Second player wins
        if isinstance(first_player, TttLearnerPlayer):
            first_player.learn_from_defeat(board)
        return -1
    # draw
    return 0

# --------------------------------------------------------------------
def update_results_and_print_statistics(res, total_games, results):
    """Update results and print games statistics"""
    if res > 0:
        results['first_win'] += 1
        print("First Player wins!  --- ", results, " - { ",
              results['first_win'] / total_games, ", ",
              results['second_win'] / total_games, ", ",
              results['draw'] / total_games, " }")
    elif res < 0:
        results['second_win'] += 1
        print("Second Player wins! --- ", results, " - { ",
              results['first_win'] / total_games, ", ",
              results['second_win'] / total_games, ", ",
              results['draw'] / total_games, " }")
    else:
        results['draw'] += 1
        print("Draw!               --- ", results, " - { ",
              results['first_win'] / total_games, ", ",
              results['second_win'] / total_games, ", ",
              results['draw'] / total_games, " }")

# --------------------------------------------------------------------
# --------------------------------------------------------------------
#   ***  MAIN ***
# --------------------------------------------------------------------
# --------------------------------------------------------------------
def main():
    """Main program: parses options, declare board and players, and
        plays a series of games"""

    parser = ArgumentParser()
    parser.add_argument("-f", "--first",
                        help="the mode of the first player", default="minimax")
    parser.add_argument("-s", "--second",
                        help="the mode of the second player", default="learner")
    parser.add_argument("-m", "--multiple-games",
                        help="play multiple games", action="store_true")
    parser.add_argument("-v", "--verbosity", action="count",
                        help="increase output verbosity")
    args = parser.parse_args()

    board = TttBoard('x', 'o')
    if args.first == "minimax":
        first_player = TttMinimaxPlayer('x')
    else:
        first_player = TttLearnerPlayer('x', board, 0.5)
    if args.second == "minimax":
        second_player = TttMinimaxPlayer('o')
    else:
        second_player = TttLearnerPlayer('o', board, 0.5)
    print("FIRST PLAYER  = ", args.first)
    print("SECOND PLAYER = ", args.second)
    if args.verbosity:
        verbosity = args.verbosity
    else:
        verbosity = 0

    results = {}
    results['first_win'] = 0
    results['second_win'] = 0
    results['draw'] = 0
    total_games = 0

    res = play_ai_vs_ai_game(first_player, second_player, board, verbosity)
    total_games += 1
    update_results_and_print_statistics(res, total_games, results)

    while args.multiple_games:
        board.reset()
        res = play_ai_vs_ai_game(first_player, second_player, board, verbosity)
        total_games += 1
        update_results_and_print_statistics(res, total_games, results)



# --------------------------------------------------------------------
if __name__ == "__main__":
    main()
