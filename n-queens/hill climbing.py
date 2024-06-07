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
    returns a board x*x with queens in random cols
    :param x: size of the board
    :return: a board x*x with queens in random cols
    """
    board = []
    for i in range(x):
        board.append(random.randrange(x))
    return board


def printboard(board):
    """
    Prints the board: #= empty cell Q=a queen
    :param board: a board x*x with queens in random cols
    :return: None
    """
    print()
    for r in range(len(board)):
        for c in range(len(board)):
            if board[c] == r:
                print('Q', end=' ')
            else:
                print('#', end=' ')
        print()
    return


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
    while n > 0:
        x = improve(b)
        if x == n:
            b = rndboard(size)
            n = threats(b)
        else:
            n = x
    printboard(b)


hill_climbing(8)
