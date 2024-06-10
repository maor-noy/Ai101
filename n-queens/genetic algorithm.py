import random


def get_fitness(board):
    """
    Calculate the fitness of a board.
    Fitness is defined as the number of pairs of queens that are attacking each other.
    :param board: a board x*x with queens in random columns
    :return: number of attacking pairs of queens
    """
    count = 0
    for i in range(len(board) - 1):
        for j in range(i + 1, len(board)):
            if board[i] == board[j] or abs(i - j) == abs(board[i] - board[j]):
                count += 1
    return count


def generate_population(board_size, population_size):
    """
    Generates a population of random boards.
    :param board_size: size of the board
    :param population_size: size of the population
    :return: a population of random boards
    """
    population = []
    for _ in range(population_size):
        population.append(rndboard(board_size))
    return population


def rndboard(x):
    """
    Returns a board x*x with queens in random columns.
    :param x: size of the board
    :return: a board x*x with queens in random columns
    """
    return [random.randrange(x) for _ in range(x)]


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


def mutate(board, mutation_rate=0.1):
    """
    Mutate a board with a given mutation rate.
    :param board: a board x*x with queens in random cols
    :param mutation_rate: probability of mutation
    :return: mutated board
    """
    if random.random() < mutation_rate:
        size = len(board)
        col = random.randint(0, size - 1)
        new_row = random.randint(0, size - 1)
        board[col] = new_row
    return board


def crossover(parent1, parent2):
    """
    Perform crossover between two parents.
    :param parent1: first parent board
    :param parent2: second parent board
    :return: child board
    """
    size = len(parent1)
    crossover_point = random.randint(0, size - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child


def genetic_algorithm(size, population_size=100, mutation_rate=0.3):
    """
    Solve the n-queens problem using genetic algorithm.
    :param size: size of the board
    :param population_size: size of the population
    :param mutation_rate: mutation rate
    :return: best board and the generation it was found
    """
    population = generate_population(size, population_size)
    best_board = None
    best_fitness = float('inf')

    while best_fitness != 0:
        fitnesses = [get_fitness(board) for board in population]
        current_best_fitness = min(fitnesses)

        if current_best_fitness < best_fitness:
            best_fitness = current_best_fitness
            best_board = population[fitnesses.index(best_fitness)]

        new_population = []
        for _ in range(population_size // 2):
            parent1, parent2 = select_parents(population, fitnesses)
            child1 = crossover(parent1, parent2)
            mutate(child1, mutation_rate)
            child2 = crossover(parent2, parent1)
            mutate(child2, mutation_rate)
            new_population.extend([child1, child2])

        population = new_population  # Ensure population size remains constant

    printboard(best_board)
    return best_board, best_fitness


def select_parents(population, fitnesses):
    """
    Select parents based on their fitness.
    :param population: list of boards
    :param fitnesses: list of fitness values corresponding to the boards
    :return: two selected parent boards
    """
    total_fitness = sum(fitnesses)
    probabilities = [(total_fitness - f) / total_fitness for f in fitnesses]
    parents = random.choices(population, weights=probabilities, k=2)
    return parents


# Example usage
genetic_algorithm(15)
