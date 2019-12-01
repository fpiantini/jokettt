#!/usr/bin/env python3
#
import tttboard
from tttboard import TttBoard
from tttconsoleplayer import TttConsolePlayer
from tttlearnerplayer import TttLearnerPlayer

# --------------------------------------------------------------------
# --------------------------------------------------------------------
def play_a_game(p1, p2, board):
    result = 0
    print("----------------------------------------------------")
    print("  --- NEW GAME ---")
    p1_turn = True
    while result == 0 and board.is_not_full():

        print('%s' % board)
        if p1_turn:
            x, y = p1.move(board)
            zhash, result = board.place_pawn(x, y, p1.piece)
        else:
            x, y = p2.move(board)
            zhash, result = board.place_pawn(x, y, p2.piece)

        p1_turn = not p1_turn

    print('%s' % board)
    if (result > 0):
        print("You lose! :-D")
    elif (result < 0):
        p2.learn_from_defeat(board)
        print("You win!! :-(")
    else:
        print("Draw! ;-)")

# --------------------------------------------------------------------
# --------------------------------------------------------------------
#   ***  MAIN ***
# --------------------------------------------------------------------
# --------------------------------------------------------------------
board = TttBoard('x', 'o')
lPlayer = TttLearnerPlayer('x', board)
cPlayer = TttConsolePlayer('o')
while True:
    board.reset()
    play_a_game(cPlayer, lPlayer, board)

# --------------------------------------------------------------------
# --------------------------------------------------------------------


