"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # initalize players be ints
    player_X = 0
    player_O = 0

    for row in board:
        if X in row:
            player_X += row.count(X)

        if O in row:
            player_O += row.count(O)

    # intial game, X gets first move.
    return X if player_X <= player_O else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    all_possible_actions = set()

    # Consider indexes at the rows using enumerate function ()
    for i, row in enumerate(board):
        # if we have an empty cell
        if EMPTY in row:
            # now within the row, consider indexes to find the empty cell
            for j, space in enumerate(row):
                if space == EMPTY:
                    all_possible_actions.add((i, j))

    return all_possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    current_player = player(board)
    # (i,j) tuple represents an action where i=row, j=cell in row
    (i, j) = action

    # Invalid action if we have no moves left or
    if new_board[i][j] != EMPTY:
        raise Exception("Invalid action")
    else:
        new_board[i][j] = current_player

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    current_player = player(board)

    # 3 in a row
    for row in board:
        o_count = row.count(O)
        x_count = row.count(X)
        if o_count == 3:
            return O
        if x_count == 3:
            return X

    # diagonals win
    if board[0][0] == X and board[1][1] == X and board[2][2] == X:
        return X
    if board[0][2] == X and board[1][1] == X and board[2][0] == X:
        return X
    if board[0][0] == O and board[1][1] == O and board[2][2] == O:
        return O
    if board[0][2] == O and board[1][1] == O and board[2][0] == O:
        return O

    # 3 in a column win
    columns = []
    for j in range(len(board)):
        col = [row[j] for row in board]
        columns.append(col)

    for j in columns:
        o_count = j.count(O)
        x_count = j.count(X)
        if o_count == 3:
            return O
        if x_count == 3:
            return X

    # tie
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If we do not have a winner i.e. no draws/wins then the game is still ongoing
    if winner(board) != EMPTY:
        return True
    # else we have a win or loss thus the game is over
    else:
        for row in board:
            # if we still have an empty cell, the game is not over!
            if EMPTY in row:
                return False
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    current_player = player(board)

    # maximizing player
    if current_player == X:
        v = -math.inf
        for action in actions(board):
            # what is the best the maximizing player can do?
            b = min_value(result(board, action))
            if b > v:
                v = b
                optimal_move = action

    # minimizing player
    else:
        v = math.inf
        for action in actions(board):
            # what is the best the minimizing player can do?
            a = max_value(result(board, action))
            if a < v:
                v = a
                optimal_move = action

    return optimal_move


def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v
