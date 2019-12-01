# --------------------------------------------------------------------
# jokettt project, v. 0.1
# by F. Piantini <francesco.piantini@gmail.com>
# ---
# Tic Tac Toe Player base class definition
# --------------------------------------------------------------------
from tttboard import TttBoard

class TttPlayer:
    def __init__(self, piece):
        self.piece = piece

    def move(self, board):
        # this is the player base class definition,
        # refuses to play...
        return None, None

