#!/usr/bin/env python3
# https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-2-evaluation-function/
#
# Minimax algo applied to TicTacToe game
from random import seed
from random import randint
from random import shuffle

# --------------------------------------------------

# - - - - - - - - - - - - - - - - - - - - - - - - -
# returns a value based on who is winning
# board[3][3] is the TicTacToe board
#
# the function returns:
#    10 if "x" is winning,
#   -10 is "o" is winning,
#     0 if draw
#    -1 if no one win and other moves are possible
def ttt_evaluate(board):
    score = ttt_evaluate_rows(board)
    if score != 0:
        return score
    score = ttt_evaluate_cols(board)
    if score != 0:
        return score
    return ttt_evaluate_diags(board)

# - - - - - - - - - - - - - - - - - - - - - - - - -
def board_is_not_full(board):
    for x in range(0, 3):
        for y in range(0, 3):
            if board[x][y] == "_":
                return True
    return False

# - - - - - - - - - - - - - - - - - - - - - - - - -
def board_is_full(board):
    return not board_is_not_full(board)

# - - - - - - - - - - - - - - - - - - - - - - - - -
def ttt_evaluate_rows(board):

    for row in range(0, 3):
        if board[row][0] == board[row][1] and board[row][1] == board[row][2]:
            if board[row][0] == 'x':
                return 10
            elif board[row][0] == 'o':
                return -10

    return 0

# - - - - - - - - - - - - - - - - - - - - - - - - -
def ttt_evaluate_cols(board):

    for col in range(0, 3):
        if board[0][col] == board[1][col] and board[1][col] == board[2][col]:
            if board[0][col] == 'x':
                return 10
            elif board[0][col] == 'o':
                return -10

    return 0

# - - - - - - - - - - - - - - - - - - - - - - - - -
def ttt_evaluate_diags(board):

    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        if board[1][1] == 'x':
            return 10
        elif board[1][1] == 'o':
            return -10

    if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        if board[1][1] == 'x':
            return 10
        elif board[1][1] == 'o':
            return -10

    return 0

# - - - - - - - - - - - - - - - - - - - - - - - - -
def clone_board(board):
    new_board = []
    new_board.append(board[0].copy())
    new_board.append(board[1].copy())
    new_board.append(board[2].copy())
    return new_board

# - - - - - - - - - - - - - - - - - - - - - - - - -
def print_board(board):
    print("     1    2    3")
    print("A ", board[0])
    print("B ", board[1])
    print("C ", board[2])

# - - - - - - - - - - - - - - - - - - - - - - - - -
def player_move(board):
    while True:
        move = input("Move? ")
        if is_valid_move(board, move):
            return convert_move_to_indexes(move)
        print("Invalid move. Try again.")

# - - - - - - - - - - - - - - - - - - - - - - - - -
def is_valid_move(board, move):
    if len(move) != 2:
        return False

    x, y = convert_move_to_indexes(move)
    if x == -1 or y == -1:
        return False

    if board[x][y] != "_":
        return False

    return True

def build_move_list(board):
    move_list = []
    for x in range(0, 3):
        for y in range(0, 3):
            if board[x][y] == "_":
                move_list.append([x, y])
    return move_list

# - - - - - - - - - - - - - - - - - - - - - - - - -
def convert_move_to_indexes(move):
    row = move[0].upper()
    col = move[1]
    return convert_move_coords_to_indexes(row, col)

# - - - - - - - - - - - - - - - - - - - - - - - - -
def convert_move_coords_to_indexes(row, col):
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

# - - - - - - - - - - - - - - - - - - - - - - - - -
def computer_move(board):
    print("")
    print("my move:")

    # to make a really dumb player uncomment next line and comment the following one
    #x, y = generate_random_move(board)
    score, x, y = find_move_minimax(board, 0, True)

    return x, y

# - - - - - - - - - - - - - - - - - - - - - - - - -
def generate_random_move(board):
    while True:
        x = randint(0, 2)
        y = randint(0, 2)
        if board[x][y] == "_":
            return x, y

# - - - - - - - - - - - - - - - - - - - - - - - - -
def evaluate_move(board, x, y, player_turn):
    if player_turn:
        board[x][y] = "o"
    else:
        board[x][y] = "x"

    return ttt_evaluate(board)

# - - - - - - - - - - - - - - - - - - - - - - - - -
def find_move_minimax(mm_board, depth, is_maximizer):

    best_x = None
    best_y = None
    val = ttt_evaluate(mm_board)
    if val != 0 or board_is_full(mm_board):
        # evaluate function returns a positive value
        # if maximizer win, a negative value otherwise
        if val > 0:
            return val - depth, best_x, best_y
        else:
            return val + depth, best_x, best_y


    move_list = build_move_list(mm_board)
    shuffle(move_list)  # to add some variability to the play (...maybe)

    if is_maximizer:
        best_score = -1000
        for move in move_list:
            simul_board = clone_board(mm_board)
            simul_board[move[0]][move[1]] = "x"
            score, x, y = find_move_minimax(simul_board, depth+1, False)
            if score > best_score:
                best_score = score
                best_x = move[0]
                best_y = move[1]
    else:
        best_score = 1000
        for move in move_list:
            simul_board = clone_board(mm_board)
            simul_board[move[0]][move[1]] = "o"
            score, x, y = find_move_minimax(simul_board, depth+1, True)
            if score < best_score:
                best_score = score
                best_x = move[0]
                best_y = move[1]

    return best_score, best_x, best_y

# --------------------------------------------------------------------------
# main

# --------------------------------------------------
board = [['_', '_', '_'],
         ['_', '_', '_'],
         ['_', '_', '_']]
result = 0
first_turn_to_engine = True

# seed random number generator
seed()

first_move = input("Do you want to do first move? [y/N] ")
if first_move.upper() == "Y":
    first_turn_to_engine = False

if first_turn_to_engine:
    # first turn for computer... generates random move
    print("I move first... my move:")
    x, y = generate_random_move(board)
    result = evaluate_move(board, x, y, False)

player_turn = True
while result == 0 and board_is_not_full(board):

    print_board(board)
    if player_turn:
        x, y = player_move(board)
    else:
        x, y = computer_move(board)

    result = evaluate_move(board, x, y, player_turn)
    player_turn = not player_turn


print_board(board)
if (result == 10):
    print("You lose! :-D")
elif (result == -10):
    print("You win!! :-(")
else:
    print("Draw! ;-)")

