import random
from board import rndboard, threats


def improve(board):
    """
    improves board if possible
    :param board: a board x*x with queens in random cols
    :return: number of threats in the board
    """
    minimum = threats(board)
    improved = [0, board[0]]  # improved holds the best move
    for r in range(len(board)):
        tmp = board[r]
        for c in range(len(board)):
            board[r] = c
            x = threats(board)
            if x < minimum:
                minimum = x
                improved = [r, c]
        board[r] = tmp
    board[improved[0]] = improved[1]
    return minimum


def hill_climbing(size):
    """
    solves the (size) quenns problem
    :param size: size of the board
    :return: None
    """
    b = rndboard(size)
    n = threats(b)
    i = 1
    while n > 0:
        x = improve(b)
        if x == n:
            b = rndboard(size)
            n = threats(b)
        else:
            n = x
        yield b
        i += 1
    print(i)
