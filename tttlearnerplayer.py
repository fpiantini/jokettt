# --------------------------------------------------------------------
# jokettt project, v. 0.1
# by F. Piantini <francesco.piantini@gmail.com>
# ---
# Tic Tac Toe "Learner" Player class definition
# --------------------------------------------------------------------
from random import shuffle

from tttplayer import TttPlayer

class TttLearnerPlayer(TttPlayer):
    def __init__(self, piece, board, alpha = 0.1):
        TttPlayer.__init__(self, piece)
        self.__alpha = alpha
        self.__values = {}
        zhash = board.get_zhash()
        score = board.evaluate()
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
        return

    def move(self, board):
        self.__x = None
        self.__y = None
        # apply reinforcement learning
        score, self.__x, self.__y = self.__find_rl_move(board)
        return self.__x, self.__y


    def __find_rl_move(self, board):

        current_zhash = board.get_zhash()
        if not current_zhash in self.__values:
            # this means that opponent has moved
            self.__values[current_zhash] = 0.5

        move_list = board.valid_moves()
        shuffle(move_list)  # to add some variability to the play (...maybe)
        best_value = -1000
        best_score = -1000
        for move in move_list:
            zhash, score = board.place_pawn(move[0], move[1], self.piece)
            board.remove_pawn(move[0], move[1])
            if score > 0:
                # we win! choose this move
                self.__values[zhash] = 1.0
                best_zhash = zhash
                best_value = self.__values[zhash]
                best_x, best_y = move
                best_score = score
                break
            elif score < 0:
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
                best_score = score

        # move selected... updates current zhash
        self.__values[current_zhash] += \
            self.__alpha * (self.__values[best_zhash] - \
                            self.__values[current_zhash])

        self.__last_zhash = best_zhash
        print(self.__values)
        return best_score, best_x, best_y

    def learn_from_defeat(self, board):
        current_zhash = board.get_zhash()
        score = board.evaluate() # this should be negative...
        if score < 0:            # so this check is useless...
            # defeat...
            self.__values[current_zhash] = 0.0
            self.__values[self.__last_zhash] += \
            self.__alpha * (self.__values[current_zhash] - \
                            self.__values[self.__last_zhash])
            print(self.__values)




