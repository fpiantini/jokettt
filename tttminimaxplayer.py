# --------------------------------------------------------------------
# jokettt project, v. 0.1
# by F. Piantini <francesco.piantini@gmail.com>
# ---
# Tic Tac Toe perfect minimax Player class definition
#
# --- Credits:
# https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-2-evaluation-function/
#
# ---
# Minimax algo applied to TicTacToe game
#  - with alpha-beta-pruning
#  - with (Zobrist) hash evaluation function
# --------------------------------------------------------------------
from copy import deepcopy

from random import randint
from random import shuffle

from tttplayer import TttPlayer

class TttMinimaxPlayer(TttPlayer):
    def __init__(self, piece, dumb_mode = False):
        TttPlayer.__init__(self, piece)
        self.set_dumb_mode(dumb_mode)

    def set_dumb_mode(self, dumb_mode):
        self.__dumb_mode = dumb_mode

    def move(self, board):
        self.__x = None
        self.__y = None
        if self.__dumb_mode:
            self.__move_dumb(board)
        else:
            self.__move_smart(board)
        return self.__x, self.__y

    def __move_dumb(self, board):
        if board.is_full():
            return
        while True:
            x = randint(0, 2)
            y = randint(0, 2)
            if board.pos_is_empty(x, y):
                self.__x = x
                self.__y = y
                return

    def __move_smart(self, board):
        # apply minimax...
        #print(".....called __move_smart()")
        score, best_x, best_y = self.__find_move_minimax(board, 0, True, -1000, 1000)
        self.__x = best_x
        self.__y = best_y
        return

    def __find_move_minimax(self, board, depth, is_maximizer, alpha, beta):
        best_x = None
        best_y = None
        val = board.evaluate()
        if val != 0 or board.is_full():
            # evaluate function returns a positive value
            # if maximizer win, a negative value otherwise
            if val > 0:
                return val - depth, best_x, best_y
            else:
                return val + depth, best_x, best_y

        move_list = board.valid_moves()
        shuffle(move_list)  # to add some variability to the play (...maybe)
        if is_maximizer:
            best_score = -1000
            for move in move_list:
                simul_board = deepcopy(board)
                simul_board.place_pawn(move[0], move[1], 'x')
                score, x, y = self.__find_move_minimax(simul_board, depth+1, False, alpha, beta)
                if score > best_score:
                    best_score = score
                    best_x = move[0]
                    best_y = move[1]
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
        else:
            best_score = 1000
            for move in move_list:
                simul_board = deepcopy(board)
                simul_board.place_pawn(move[0], move[1], 'o')
                score, x, y = self.__find_move_minimax(simul_board, depth+1, True, alpha, beta)
                if score < best_score:
                    best_score = score
                    best_x = move[0]
                    best_y = move[1]
                beta = min(beta, best_score)
                if beta <= alpha:
                    break

        return best_score, best_x, best_y



