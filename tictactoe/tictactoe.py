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
    # print("player")
    counterX = 0

    counterO = 0

    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                counterX += 1
            elif board[i][j] == O:
                counterO += 1

    if counterX > counterO:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # raise NotImplementedError
    # print("actions")
    possible_moves = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_moves.add((i, j))
    return possible_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # print("result")
    new_state = copy.deepcopy(board)

    new_state[action[0]][action[1]] = player(board)

    return new_state


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # print("winner")
    for row in range(0, 3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not EMPTY:
            if board[row][0] == X:
                return X
            else:
                return O

    for col in range(0, 3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not EMPTY:
            if board[0][col] == X:
                return X
            else:
                return O

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        if board[0][0] == X:
            return X
        else:
            return O
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        if board[0][2] == X:
            return X
        else:
            return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # print("terminal")
    if winner(board) is not None:
        return True
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
    return True
    # raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # print("utility")
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        score = -math.inf
        future_action = None

        for action in actions(board):
            min_val = minvalue(result(board, action))
            if min_val > score:
                score = min_val
                future_action = action
        return future_action

    elif player(board) == O:
        score = math.inf
        future_action = None

        for action in actions(board):
            max_val = maxvalue(result(board, action))
            if max_val < score:
                score = max_val
                future_action = action
        return future_action


def minvalue(board):

    if terminal(board):
        return utility(board)

    max_value = math.inf
    for action in actions(board):
        max_value = min(max_value, maxvalue(result(board, action)))
    return max_value


def maxvalue(board):

    if terminal(board):
        return utility(board)

    min_val = -math.inf
    for action in actions(board):
        min_val = max(min_val, minvalue(result(board, action)))
    return min_val
