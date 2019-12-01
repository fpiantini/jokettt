#!/usr/bin/env python3

from copy import deepcopy, copy

from random import seed
from random import randint
from random import shuffle

# --------------------------------------------------------------------
# --------------------------------------------------------------------
# --------------------------------------------------------------------
class TttBoard:
    def __init__(self, init_board = [['_', '_', '_'],
                                     ['_', '_', '_'],
                                     ['_', '_', '_']]):
        self.__board = init_board
        seed()

    def get_board(self):
        return self.__board

    def is_not_full(self):
        for x in range(0, 3):
            for y in range(0, 3):
                if self.__board[x][y] == "_":
                    return True
        return False

    def is_full(self):
        return not self.is_not_full()

    def pos_is_empty(self, x, y):
        if self.__board[x][y] == "_":
            return True
        else:
            return False

    def pos_is_busy(self, x, y):
        return not self.pos_is_empty(x, y)

    def valid_moves(self):
        move_list = []
        for x in range(0, 3):
            for y in range(0, 3):
                if self.__board[x][y] == "_":
                    move_list.append([x, y])
        return move_list

    def place_pawn(self, x, y, type):
        if self.pos_is_empty(x, y):
            self.__board[x][y] = type
        return self.evaluate()

    def evaluate(self):
        score = self.__evaluate_rows()
        if score != 0:
            return score
        score = self.__evaluate_cols()
        if score != 0:
            return score
        return self.__evaluate_diags()

    def convert_move_to_indexes(self, move):
        row = move[0].upper()
        col = move[1]
        return self.__convert_move_coords_to_indexes(row, col)

    def pretty_print(self):
        print("     1    2    3")
        print("A ", self.__board[0])
        print("B ", self.__board[1])
        print("C ", self.__board[2])

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

    def __evaluate_rows(self):
        for row in range(0, 3):
            if self.__board[row][0] == self.__board[row][1] and self.__board[row][1] == self.__board[row][2]:
                if self.__board[row][0] == 'x':
                    return 10
                elif self.__board[row][0] == 'o':
                    return -10
        return 0

    def __evaluate_cols(self):
        for col in range(0, 3):
            if self.__board[0][col] == self.__board[1][col] and self.__board[1][col] == self.__board[2][col]:
                if self.__board[0][col] == 'x':
                    return 10
                elif self.__board[0][col] == 'o':
                    return -10
        return 0

    def __evaluate_diags(self):
        if self.__board[0][0] == self.__board[1][1] and self.__board[1][1] == self.__board[2][2]:
            if self.__board[1][1] == 'x':
                return 10
            elif self.__board[1][1] == 'o':
                return -10

        if self.__board[0][2] == self.__board[1][1] and self.__board[1][1] == self.__board[2][0]:
            if self.__board[1][1] == 'x':
                return 10
            elif self.__board[1][1] == 'o':
                return -10
        return 0

# --------------------------------------------------------------------
# --------------------------------------------------------------------
# --------------------------------------------------------------------
class TttAutoPlayer:
    def __init__(self, dumb_mode):
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
        score, best_x, best_y = self.__find_move_minimax(board, 0, True)
        self.__x = best_x
        self.__y = best_y
        return

    def __find_move_minimax(self, board, depth, is_maximizer):
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
                #simul_board = TttBoard(board.get_board())
                simul_board.place_pawn(move[0], move[1], "x")
                score, x, y = self.__find_move_minimax(simul_board, depth+1, False)
                if score > best_score:
                    best_score = score
                    best_x = move[0]
                    best_y = move[1]
        else:
            best_score = 1000
            for move in move_list:
                simul_board = deepcopy(board)
                #simul_board = TttBoard(board.get_board())
                simul_board.place_pawn(move[0], move[1], "o")
                score, x, y = self.__find_move_minimax(simul_board, depth+1, True)
                if score < best_score:
                    best_score = score
                    best_x = move[0]
                    best_y = move[1]
        return best_score, best_x, best_y


# --------------------------------------------------------------------
# --------------------------------------------------------------------
# --------------------------------------------------------------------
class TttTtyPlayer:
    def __init__(self):
        return

    def move(self, board):
        while True:
            move = input("Move? ")
            if self.__is_valid_move(move, board):
                return board.convert_move_to_indexes(move)
            print("Invalid move. Try again.")

    def __is_valid_move(self, move, board):
        if len(move) != 2:
            return False
        x, y = board.convert_move_to_indexes(move)
        if x == -1 or y == -1:
            return False
        if board.pos_is_busy(x, y):
            return False
        return True


# --------------------------------------------------------------------
# --------------------------------------------------------------------
#   ***  MAIN ***
# --------------------------------------------------------------------
# --------------------------------------------------------------------
board = TttBoard()
autoPlayer = TttAutoPlayer(True)
ttyPlayer = TttTtyPlayer()
result = 0
first_turn_to_engine = True

first_move = input("Do you want to do first move? [y/N] ")
if first_move.upper() == "Y":
    first_turn_to_engine = False

if first_turn_to_engine:
    # first turn for computer... generates random move
    print("I move first... my move:")
    x, y = autoPlayer.move(board)
    result = board.place_pawn(x, y, "x")

autoPlayer.set_dumb_mode(False)
player_turn = True

while result == 0 and board.is_not_full():

    board.pretty_print()
    if player_turn:
        x, y = ttyPlayer.move(board)
        result = board.place_pawn(x, y, 'o')
    else:
        x, y = autoPlayer.move(board)
        result = board.place_pawn(x, y, 'x')

    player_turn = not player_turn

board.pretty_print()
if (result > 0):
    print("You lose! :-D")
elif (result < 0):
    print("You win!! :-(")
else:
    print("Draw! ;-)")
# --------------------------------------------------------------------
# --------------------------------------------------------------------


