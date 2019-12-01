# --------------------------------------------------------------------
# jokettt project, v. 0.1
# by F. Piantini <francesco.piantini@gmail.com>
# ---
# Tic Tac Toe Board class definition
# --------------------------------------------------------------------
import sys
import numpy as np

from random import seed
from random import randint

class TttBoard:

    # ------------------------------------------------------
    def __init__(self, positive_piece, negative_piece,
                 init_board = [['_', '_', '_'],
                               ['_', '_', '_'],
                               ['_', '_', '_']]):
        self.__posPiece = positive_piece
        self.__negPiece = negative_piece
        self.__board = init_board
        seed()
        self.__init_zhash()

    # ------------------------------------------------------
    def reset(self,
              init_board = [['_', '_', '_'],
                            ['_', '_', '_'],
                            ['_', '_', '_']]):
        for x in range(0, 3):
            for y in range(0, 3):
                self.__board[x][y] = init_board[x][y]
        # initialize Zobrist hash value
        self.__evaluate_zhash()

    # ------------------------------------------------------
    def get_zhash(self):
        return self.__zobrist_hash

    # ------------------------------------------------------
    def is_not_full(self):
        for x in range(0, 3):
            for y in range(0, 3):
                if self.__board[x][y] == "_":
                    return True
        return False

    # ------------------------------------------------------
    def is_full(self):
        return not self.is_not_full()

    # ------------------------------------------------------
    def pos_is_empty(self, x, y):
        if self.__board[x][y] == "_":
            return True
        else:
            return False

    # ------------------------------------------------------
    def pos_is_busy(self, x, y):
        return not self.pos_is_empty(x, y)

    # ------------------------------------------------------
    def valid_moves(self):
        move_list = []
        for x in range(0, 3):
            for y in range(0, 3):
                if self.__board[x][y] == "_":
                    move_list.append([x, y])
        return move_list

    # ------------------------------------------------------
    def is_valid_move(self, move):
        # check the format of the move
        if len(move) != 2:
            return False
        x, y = self.convert_move_to_indexes(move)
        if x == -1 or y == -1:
            return False
        # check if the position if free in the board
        if self.pos_is_busy(x, y):
            return False
        return True

    # ------------------------------------------------------
    def place_pawn(self, x, y, piece):
        if self.pos_is_empty(x, y):
            self.__board[x][y] = piece
            self.__update_zhash(x, y, piece)
        return self.get_zhash(), self.evaluate()

    # ------------------------------------------------------
    def remove_pawn(self, x, y):
        piece = self.__board[x][y]
        if piece != "_":
            self.__update_zhash(x, y, piece)
            self.__board[x][y] = "_"

    # ------------------------------------------------------
    def evaluate(self):
        score = self.__evaluate_rows()
        if score != 0:
            return score
        score = self.__evaluate_cols()
        if score != 0:
            return score
        return self.__evaluate_diags()

    # ------------------------------------------------------
    def convert_move_to_indexes(self, move):
        row = move[0].upper()
        col = move[1]
        return self.__convert_move_coords_to_indexes(row, col)

    # ------------------------------------------------------
    def __convert_move_coords_to_indexes(self, row, col):
        row_to_x = {
            "A": 0,
            "B": 1,
            "C": 2
        }
        col_to_y = {
            "1": 0,
            "2": 1,
            "3": 2
        }
        return row_to_x.get(row, -1), col_to_y.get(col, -1)

    # ------------------------------------------------------
    def __evaluate_rows(self):
        for row in range(0, 3):
            if self.__board[row][0] == self.__board[row][1] and self.__board[row][1] == self.__board[row][2]:
                if self.__board[row][0] == self.__posPiece:
                    return 10
                elif self.__board[row][0] == self.__negPiece:
                    return -10
        return 0

    # ------------------------------------------------------
    def __evaluate_cols(self):
        for col in range(0, 3):
            if self.__board[0][col] == self.__board[1][col] and self.__board[1][col] == self.__board[2][col]:
                if self.__board[0][col] == self.__posPiece:
                    return 10
                elif self.__board[0][col] == self.__negPiece:
                    return -10
        return 0

    # ------------------------------------------------------
    def __evaluate_diags(self):
        if self.__board[0][0] == self.__board[1][1] and self.__board[1][1] == self.__board[2][2]:
            if self.__board[1][1] == self.__posPiece:
                return 10
            elif self.__board[1][1] == self.__negPiece:
                return -10

        if self.__board[0][2] == self.__board[1][1] and self.__board[1][1] == self.__board[2][0]:
            if self.__board[1][1] == self.__posPiece:
                return 10
            elif self.__board[1][1] == self.__negPiece:
                return -10
        return 0

    # ------------------------------------------------------
    def __init_zhash(self):
        # initialize Zobrist hash table
        self.__zhash_table = np.empty([3,3,2], dtype=int)
        for x in range(0, 3):
            for y in range (0, 3):
                for e in range (0, 2):
                    self.__zhash_table[x][y][e] = randint(0, sys.maxsize)
        # initialize Zobrist hash value
        self.__evaluate_zhash()

    # ------------------------------------------------------
    def __evaluate_zhash(self):
        # initialize Zobrist hash value
        self.__zobrist_hash = 0
        for x in range(0, 3):
            for y in range(0, 3):
                piece = self.__board[x][y]
                if piece != "_":
                    piece_ndx = self.__convert_piece_in_index(piece)
                    self.__zobrist_hash ^= self.__zhash_table[x][y][piece_ndx]

    # ------------------------------------------------------
    def __update_zhash(self, x, y, piece):
        piece_ndx = self.__convert_piece_in_index(piece)
        self.__zobrist_hash ^= self.__zhash_table[x][y][piece_ndx]

    # ------------------------------------------------------
    def __convert_piece_in_index(self, piece):
        if piece == self.__posPiece:
            return 0
        return 1

    # ------------------------------------------------------
    def __str__(self):
        return '     1    2    3\nA %r\nB %r\nC %r\n--- hash = %r' % \
            (self.__board[0], self.__board[1], self.__board[2], self.get_zhash())

    # ------------------------------------------------------
    def __repr__(self):
        return 'TttBoard(%s)' % self.__board



