"""
The state is a list of 2 items: the board, the path
The target is :
012
345
678
"""
import math
from numpy import sqrt


def get_next(x):
    ns = []
    for i in "<>v^":
        s = x[0][:]
        if_legal(s, i)
        if s.index(0) != x[0].index(0) and \
                (x[1] == "" or x[1][-1] != "><^v"["<>v^".index(i)]):
            ns.append([s, x[1] + i])
    return ns


# returns a random board nXn
def create(start):
    s = start
    return [s, ""]


def path_len(x):
    return len(x[1])


def is_target(x):
    n = len(x[0])
    return x[0] == list(range(n))


def hdistance(s):
    n = sqrt(len(s[0]))
    c = 0
    for i in range(0, len(s[0])):  # manheten distance for each tile
        index = s[0].index(i)
        disX = abs(i % n - index % n)
        disY = abs(i // n - index // n)
        c += disX + disY
    return c


#############################
def if_legal(x, m):
    n = int(math.sqrt(len(x)))
    z = x.index(0)
    if z % n > 0 and m == "<":
        x[z] = x[z - 1]
        x[z - 1] = 0
    elif z % n < n - 1 and m == ">":
        x[z] = x[z + 1]
        x[z + 1] = 0
    elif z >= n and m == "^":
        x[z] = x[z - n]
        x[z - n] = 0
    elif z < n * n - n and m == "v":
        x[z] = x[z + n]
        x[z + n] = 0


