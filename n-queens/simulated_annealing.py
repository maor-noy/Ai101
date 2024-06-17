import math
import random
from board import rndboard, threats


def schedule(t):
    return 1000 * (0.995 ** t)


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
    current_board = rndboard(n)
    current_cost = threats(current_board)
    i = 0
    while True:
        T = schedule(i)
        if T == 0 or current_cost == 0:
            print(i)
            break

        neighbor = get_neighbor(current_board)
        neighbor_cost = threats(neighbor)
        delta = neighbor_cost - current_cost
        if delta < 0 or random.uniform(0, 1) < math.exp(-delta / T):
            current_board = neighbor
            current_cost = neighbor_cost
        i += 1
        yield current_board

