import random


def threats(board):
    """
    returns number of threats in board
    :param board: a board x*x with queens in random cols
    :return: number of threats in board
    """
    count = 0
    for i in range(0, len(board) - 1):
        for j in range(i + 1, len(board)):
            if board[i] == board[j] or abs(i - j) == abs(board[i] - board[j]):
                count = count + 1
    return count


def rndboard(x):
    """
    Returns a board x*x with queens in random columns.
    :param x: size of the board
    :return: a board x*x with queens in random columns
    """
    return [random.randrange(x) for _ in range(x)]
