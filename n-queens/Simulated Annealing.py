import random
import math


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


def get_neighbor(board):
    """Generate a neighbor state by randomly moving a queen."""
    size = len(board)
    neighbor = board[:]
    col = random.randint(0, size - 1)
    new_row = random.randint(0, size - 1)
    neighbor[col] = new_row
    return neighbor


def simulated_annealing(n):
    """Solve the n-queens problem using simulated annealing."""
    # Initial state (randomly placing n queens)
    current_board = rndboard(n)
    current_cost = threats(current_board)

    # Initial temperature and cooling rate
    temperature = 1.0
    cooling_rate = 0.99
    min_temperature = 1e-10

    while temperature > min_temperature and current_cost > 0:
        # Generate a neighbor state
        neighbor_board = get_neighbor(current_board)
        neighbor_cost = threats(neighbor_board)

        # Calculate the acceptance probability
        delta_cost = neighbor_cost - current_cost
        acceptance_probability = math.exp(-delta_cost / temperature) if delta_cost > 0 else 1.0

        # Decide whether to accept the neighbor state
        if acceptance_probability > random.random():
            current_board = neighbor_board
            current_cost = neighbor_cost

        # Cool down the temperature
        temperature *= cooling_rate

    printboard(current_board)


simulated_annealing(8)
