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
###from random import shuffle

from tttplayer import TttPlayer

class TttLearnerPlayer(TttPlayer):
    """A Tic Tac Toe learner automatic player."""

    # --------------------------------------------------------------
    def __init__(self, piece, board, alpha=0.1, verbosity=0):
        """TttPlayer class constructor. Save the given piece,
            the alpha value and initializes Value vector."""
        print("verbosity level = ", verbosity)
        TttPlayer.__init__(self, piece, verbosity)
        self.__alpha = alpha
        self.__values = {}
        self.__best_value = -1000
        self.__best_x = None
        self.__best_y = None
        self.__best_zhash = -1
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

    # --------------------------------------------------------------
    def move(self, board):
        """Do a move using reinforcement learning algo"""
        return self.__find_rl_move(board)

    # --------------------------------------------------------------
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

    # --------------------------------------------------------------
    def __find_rl_move(self, board):
        """Find a move that is considered the best depending on current knowledge"""
        current_zhash = board.get_zhash()
        if not current_zhash in self.__values:
            # the board status is not in values array:
            # this is the first time we encounter this position
            if self.verbosity > 0:
                print("new board status encounted: init to 0.5")
            self.__values[current_zhash] = 0.5

        move_list = board.valid_moves()
        #shuffle(move_list)  # to add some variability to the play (...maybe)
        self.__best_value = -1000
        self.__best_x = None
        self.__best_y = None
        for move in move_list:
            if self.__analyze_move(move, board):
                # winning move found
                break

        # move selected... updates current zhash
        self.__values[current_zhash] += \
            self.__alpha * (self.__values[self.__best_zhash] - \
                            self.__values[current_zhash])

        self.__last_zhash = self.__best_zhash
        ###print(self.__values)
        return self.__best_x, self.__best_y

    # --------------------------------------------------------------
    def __analyze_move(self, move, board):
        winning_move_found = False
        zhash, score = board.place_pawn(move[0], move[1], self.piece)
        if self.verbosity > 0:
            print("evaluating move: ", board.convert_move_to_movestring(move),
                  ", score = ", score)
        board.remove_pawn(move[0], move[1])
        if score > 0:
            # we win! choose this move
            if self.verbosity > 0:
                print("WINNING MOVE! Choose it")
            self.__values[zhash] = 1.0
            self.__best_zhash = zhash
            self.__best_value = self.__values[zhash]
            self.__best_x, self.__best_y = move
            winning_move_found = True
        if score < 0:
            # we lose... try do not select this move
            # updates values table in any case
            if self.verbosity > 0:
                print("LOSING MOVE(?!) Avoid it")
            self.__values[zhash] = 0.0
        else:
            # neutral move... if the hash is not in dictionary
            # this is the first time we encounter this move:
            # initialize value
            if self.verbosity > 0:
                print("NEUTRAL MOVE... analyzing it")
            if not zhash in self.__values:
                if self.verbosity > 0:
                    print("   - new board status encounted: init to 0.5")
                self.__values[zhash] = 0.5

        # if here the move is not winning...
        # checks if it is good and continue
        if self.__best_value < self.__values[zhash]:
            self.__best_zhash = zhash
            self.__best_value = self.__values[zhash]
            self.__best_x, self.__best_y = move
            if self.verbosity > 0:
                print("   - move is selected as the new best choice - value = ", self.__best_value)

        return winning_move_found
