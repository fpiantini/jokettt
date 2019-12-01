# --------------------------------------------------------------------
# jokettt project, v. 0.1
# by F. Piantini <francesco.piantini@gmail.com>
# ---
# Tic Tac Toe "Learner" Player class definition
# --------------------------------------------------------------------
"""Implementation of a "learner" tic-tac-toe player, that improves
    his gameplay learning during games.
    The player made use of a value function that assign a value to
    every board state. Initially the value is 0 for any losing position,
    1 for every winning position and 0.5 for all the other positions.
    During games the values of the intermediates position are calibrated
    using the standard reinforcement learning formula:
        V(s) = V(s) + alpha * [ V(s') - V(s) ]
    This class is derived from the TttPlayer base class
"""
from random import shuffle

from tttplayer import TttPlayer

class TttLearnerPlayer(TttPlayer):
    """A Tic Tac Toe learner automatic player."""
    def __init__(self, piece, board, alpha=0.1):
        """TttPlayer class constructor. Save the given piece,
            the alpha value and initializes Value vector."""
        TttPlayer.__init__(self, piece)
        self.__alpha = alpha
        self.__values = {}
        zhash = board.get_zhash()
        score = board.evaluate(self.piece)
        if score > 0:
            # winning board...
            self.__values[zhash] = 1.0
        elif score < 0:
            #losing board
            self.__values[zhash] = 0.0
        else:
            # playable board
            self.__values[zhash] = 0.5
        self.__last_zhash = zhash

    def move(self, board):
        """Do a move using reinforcement learning algo"""
        return self.__find_rl_move(board)


    def __find_rl_move(self, board):
        """Find a move that is considered the best depending on current knowledge"""
        current_zhash = board.get_zhash()
        if not current_zhash in self.__values:
            # this means that opponent has moved
            self.__values[current_zhash] = 0.5

        move_list = board.valid_moves()
        shuffle(move_list)  # to add some variability to the play (...maybe)
        best_value = -1000
        for move in move_list:
            zhash, score = board.place_pawn(move[0], move[1], self.piece)
            board.remove_pawn(move[0], move[1])
            if score > 0:
                # we win! choose this move
                self.__values[zhash] = 1.0
                best_zhash = zhash
                best_value = self.__values[zhash]
                best_x, best_y = move
                break
            if score < 0:
                # we lose... try do not select this move
                # updates values table in any case
                self.__values[zhash] = 0.0
            else:
                # neutral move... if the hash is not in dictionary
                # this is the first time we encounter this move:
                # initialize value
                if not zhash in self.__values:
                    self.__values[zhash] = 0.5

            # if here the move is not winning...
            # checks if it is good and continue
            if best_value < self.__values[zhash]:
                best_zhash = zhash
                best_value = self.__values[zhash]
                best_x, best_y = move

        # move selected... updates current zhash
        self.__values[current_zhash] += \
            self.__alpha * (self.__values[best_zhash] - \
                            self.__values[current_zhash])

        self.__last_zhash = best_zhash
        ###print(self.__values)
        return best_x, best_y

    def learn_from_defeat(self, board):
        """Updates the value vector given a final lost position"""
        current_zhash = board.get_zhash()
        score = board.evaluate(self.piece) # this should be negative...
        if score < 0:            # so this check is useless...
            # defeat...
            self.__values[current_zhash] = 0.0
            self.__values[self.__last_zhash] += \
            self.__alpha * (self.__values[current_zhash] - \
                            self.__values[self.__last_zhash])
            ###print(self.__values)
