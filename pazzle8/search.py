# search
import state
import frontier


def search(start):
    """
    function to search for the target state
    :param n: the size of the board
    :param start: the start state
    :return: the path to the target state
    """
    s = state.create(start)
    f = frontier.create(s)
    while not frontier.is_empty(f):
        s = frontier.remove(f)
        if state.is_target(s):
            return s[-1]
        ns = state.get_next(s)
        for i in ns:
            frontier.insert(f, i)
    return 0
