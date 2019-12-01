# https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-2-evaluation-function/
#
# Minimax algo applied to TicTacToe game

# --------------------------------------------------
# evaluation function

# returns a value based on who is winning
# board[3][3] is the TicTacToe board
#
# the function returns:
#   10 if "x" is winning,
#   -10 is "o" is winning,
#   0 if no one is winning
def ttt_evaluate(board):

    score = ttt_evaluate_rows(board)
    if score != 0:
        return score
    score = ttt_evaluate_cols(board)
    if score != 0:
        return score
    score = ttt_evaluate_diags(board)
    return score

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

# --------------------------------------------------------------------------
# main

draw_board1 = [['', '', ''],
               ['', '', ''],
               ['', '', '']]
draw_board2 = [['x', 'o', 'x'],
               ['x', 'o', 'o'],
               ['o', 'x', 'x']]

win_board1  = [['x', 'x', 'x'],
               [ '', 'o', 'o'],
               [ '', 'o',  '']]
win_board2  = [['x', '', ''],
               ['x', 'o', 'o'],
               ['x', '', 'o']]
win_board3  = [['x',  '',  ''],
               [ '', 'x', 'o'],
               ['o', 'o', 'x']]
lose_board1 = [['x', 'o',  ''],
               ['x', 'o',  ''],
               [ '', 'o', 'x']]

print(ttt_evaluate(draw_board1))
print(ttt_evaluate(draw_board2))

print(ttt_evaluate(win_board1))
print(ttt_evaluate(win_board2))
print(ttt_evaluate(win_board3))

print(ttt_evaluate(lose_board1))

