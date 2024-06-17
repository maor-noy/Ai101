import random
from board import threats, rndboard

def generate_population(board_size, population_size):
    """
    Generates a population of random boards.
    :param board_size: size of the board
    :param population_size: size of the population
    :return: a population of random boards
    """
    population = [rndboard(board_size) for _ in range(population_size)]
    return population

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

def select_parents(population, fitnesses):
    """
    Select parents based on their fitness.
    :param fitnesses: list of fitness values
    :param population: list of boards
    :return: two selected parent boards
    """
    total_fitness = sum(fitnesses)
    probabilities = [(total_fitness - f) / total_fitness for f in fitnesses]
    parents = random.choices(population, weights=probabilities, k=2)
    return parents

def genetic_algorithm(size, population_size=100, mutation_rate=0.3):
    """
    Solve the n-queens problem using genetic algorithm.
    :param size: size of the board
    :param population_size: size of the population
    :param mutation_rate: mutation rate
    :return: best board and the generation it was found
    """
    population = generate_population(size, population_size)
    best_board = min(population, key=threats)
    best_fitness = threats(best_board)
    generation = 0

    while best_fitness != 0:
        fitness = [threats(board) for board in population]
        current_best_fitness = min(fitness)

        if current_best_fitness < best_fitness:
            best_fitness = current_best_fitness
            best_board = population[fitness.index(best_fitness)]

        new_population = []
        for _ in range(population_size // 2):
            parent1, parent2 = select_parents(population, fitness)
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)
            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)
            new_population.extend([child1, child2])

        population = new_population  # Ensure population size remains constant
        generation += 1
        yield min(population, key=threats)

    print(generation)
    return best_board
