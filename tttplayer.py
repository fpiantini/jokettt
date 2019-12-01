# --------------------------------------------------------------------
# jokettt project, v. 0.1
# by F. Piantini <francesco.piantini@gmail.com>
# ---
# Tic Tac Toe Player base class definition
# --------------------------------------------------------------------

# pylint: disable=too-few-public-methods

"""Implementation of the TttPlayer base abstract class:
    a generic player that has a piece and it is able to perform a move.
    This class shall not be used directly: it shall be used as a base
    class for real players
"""
from abc import ABC, abstractmethod

class TttPlayer(ABC):
    """A Tic Tac Toe player base class."""
    def __init__(self, piece):
        """TttPlayer class constructor. Just save the given piece."""
        self.piece = piece
        ABC.__init__(self)

    @abstractmethod
    def move(self, board):
        """Method to make a move. This is the base player,
            so this method is abstract."""