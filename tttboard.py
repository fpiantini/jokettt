#!/usr/bin/env python3
# --------------------------------------------------------------------
# jokettt project, v. 0.1
# by F. Piantini <francesco.piantini@gmail.com>
# ---
# Tic Tac Toe Board class definition
# --------------------------------------------------------------------
"""Implementation of the TttBoard class: a board to play Tic Tac Toe game."""
import sys

from random import seed
from random import randint

import numpy as np

class TttBoard:
    """A board to play Tic Tac Toe game."""
    # ------------------------------------------------------
    def __init__(self, positive_piece, negative_piece, init_board=None):

        """TttBoard class constructor"""
        if init_board is not None:
            self.__board = init_board
        else:
            self.__board = [['_', '_', '_'],
                            ['_', '_', '_'],
                            ['_', '_', '_']]

        self.__pos_piece = positive_piece
        self.__neg_piece = negative_piece
        seed()
        self.__zobrist_hash = 0
        self.__init_zhash()

    # ------------------------------------------------------
    def reset(self, init_board=None):

        """Reset the board to the given schema (default = empty)."""
        if init_board is not None:
            for _x in range(0, 3):
                for _y in range(0, 3):
                    self.__board[_x][_y] = init_board[_x][_y]
        else:
            self.__board = [['_', '_', '_'],
                            ['_', '_', '_'],
                            ['_', '_', '_']]

        # initialize Zobrist hash value
        self.__evaluate_zhash()

    # ------------------------------------------------------
    def get_zhash(self):
        """Return the current Zobrist hash of the board."""
        return self.__zobrist_hash

    # ------------------------------------------------------
    def is_not_full(self):
        """Returns true if the board is not full."""
        for _x in range(0, 3):
            for _y in range(0, 3):
                if self.__board[_x][_y] == "_":
                    return True
        return False

    # ------------------------------------------------------
    def is_full(self):
        """Returns true if the board is full."""
        return not self.is_not_full()

    # ------------------------------------------------------
    def pos_is_empty(self, _x, _y):
        """Returns true if the given board position does not contains a pawn."""
        return bool(self.__board[_x][_y] == "_")

    # ------------------------------------------------------
    def pos_is_busy(self, _x, _y):
        """Returns true if the given board position contains a pawn."""
        return not self.pos_is_empty(_x, _y)

    # ------------------------------------------------------
    def valid_moves(self):
        """Returns the list of the valid moves in the current board state."""
        move_list = []
        for _x in range(0, 3):
            for _y in range(0, 3):
                if self.__board[_x][_y] == "_":
                    move_list.append([_x, _y])
        return move_list

    # ------------------------------------------------------
    def is_valid_move(self, move):
        """Returns true if the move is valid in the current board state."""
        # check the format of the move
        if len(move) != 2:
            return False
        _x, _y = self.convert_move_to_indexes(move)
        if _x == -1 or _y == -1:
            return False
        # check if the position if free in the board
        if self.pos_is_busy(_x, _y):
            return False
        return True

    # ------------------------------------------------------
    def place_pawn(self, _x, _y, piece):
        """Places a pawn in the given board position."""
        if self.pos_is_empty(_x, _y):
            self.__board[_x][_y] = piece
            self.__update_zhash(_x, _y, piece)
        return self.get_zhash(), self.evaluate()

    # ------------------------------------------------------
    def remove_pawn(self, _x, _y):
        """Removes a pawn from the given board position."""
        piece = self.__board[_x][_y]
        if piece != "_":
            self.__update_zhash(_x, _y, piece)
            self.__board[_x][_y] = "_"

    # ------------------------------------------------------
    def evaluate(self):
        """Evaluates the board value."""
        score = self.__evaluate_rows()
        if score != 0:
            return score
        score = self.__evaluate_cols()
        if score != 0:
            return score
        return self.__evaluate_diags()

    # ------------------------------------------------------
    def convert_move_to_indexes(self, move):
        """Convert the move from the <row><col> (e.g. "A1") format to the board x,y indexes."""
        row = move[0].upper()
        col = move[1]
        return self.__convert_move_coords_to_indexes(row, col)

    # ------------------------------------------------------
    @staticmethod
    def __convert_move_coords_to_indexes(row, col):
        """Convert move coordinates (e.g. "A","1") to board x,y indexes."""
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
        """Evaluates the board value checking only rows."""
        val = 0
        row = 0
        while val == 0 and row < 3:
            if self.__board[row][0] == self.__board[row][1] and \
                    self.__board[row][1] == self.__board[row][2]:
                if self.__board[row][0] == self.__pos_piece:
                    val = 10
                elif self.__board[row][0] == self.__neg_piece:
                    val = -10
            row += 1

        return val

    # ------------------------------------------------------
    def __evaluate_cols(self):
        """Evaluates the board value checking only columns."""
        val = 0
        col = 0
        while val == 0 and col < 3:
            if self.__board[0][col] == self.__board[1][col] and \
               self.__board[1][col] == self.__board[2][col]:
                if self.__board[0][col] == self.__pos_piece:
                    val = 10
                elif self.__board[0][col] == self.__neg_piece:
                    val = -10
            col += 1

        return val

    # ------------------------------------------------------
    def __evaluate_diags(self):
        """Evaluates the board value checking only diagonals."""
        val = 0
        if self.__board[0][0] == self.__board[1][1] and \
           self.__board[1][1] == self.__board[2][2]:
            if self.__board[1][1] == self.__pos_piece:
                val = 10
            elif self.__board[1][1] == self.__neg_piece:
                val = -10

        if val != 0:
            return val

        if self.__board[0][2] == self.__board[1][1] and \
           self.__board[1][1] == self.__board[2][0]:
            if self.__board[1][1] == self.__pos_piece:
                val = 10
            elif self.__board[1][1] == self.__neg_piece:
                val = -10

        return val

    # ------------------------------------------------------
    def __init_zhash(self):
        """Initialize Zobrist hash table."""
        # initialize Zobrist hash table
        self.__zhash_table = np.empty([3, 3, 2], dtype=int)
        for _x in range(0, 3):
            for _y in range(0, 3):
                for _e in range(0, 2):
                    self.__zhash_table[_x][_y][_e] = randint(0, sys.maxsize)
        # initialize Zobrist hash value
        self.__evaluate_zhash()

    # ------------------------------------------------------
    def __evaluate_zhash(self):
        """Initialize Zobrist hash value."""
        self.__zobrist_hash = 0
        for _x in range(0, 3):
            for _y in range(0, 3):
                piece = self.__board[_x][_y]
                if piece != "_":
                    piece_ndx = self.__convert_piece_in_index(piece)
                    self.__zobrist_hash ^= self.__zhash_table[_x][_y][piece_ndx]

    # ------------------------------------------------------
    def __update_zhash(self, _x, _y, piece):
        """Update Zobrist hash value after a board status change
        due to a single place or remove of a pawn.
        """
        piece_ndx = self.__convert_piece_in_index(piece)
        self.__zobrist_hash ^= self.__zhash_table[_x][_y][piece_ndx]

    # ------------------------------------------------------
    def __convert_piece_in_index(self, piece):
        """Convert a piece in internal index."""
        if piece == self.__pos_piece:
            return 0
        return 1

    # ------------------------------------------------------
    def __str__(self):
        """__str__ display of the board."""
        ###return '     1    2    3\nA %r\nB %r\nC %r\n--- hash = %r' % \
        ###    (self.__board[0], self.__board[1], self.__board[2], self.get_zhash())
        return '     1    2    3\nA %r\nB %r\nC %r\n' % \
            (self.__board[0], self.__board[1], self.__board[2])

    # ------------------------------------------------------
    def __repr__(self):
        """__repr__ representation of the board."""
        return 'TttBoard(%s)' % self.__board
