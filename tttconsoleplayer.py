# --------------------------------------------------------------------
# jokettt project, v. 0.1
# by F. Piantini <francesco.piantini@gmail.com>
# ---
# Tic Tac Toe Console Player class definition
# --------------------------------------------------------------------
from tttplayer import TttPlayer

class TttConsolePlayer(TttPlayer):
    # no need to redefine the __init__ from TttPlayer
    #def __init__(self, piece):
    #    pass

    def move(self, board):
        # read move from Console
        while True:
            move = input("Move? ")
            if board.is_valid_move(move):
                return board.convert_move_to_indexes(move)
            print("Invalid move. Try again.")


