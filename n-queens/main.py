import pygame
from genetic_algorithm import genetic_algorithm
from hill_climbing import hill_climbing
from simulated_annealing import simulated_annealing


def draw_board(screen, board, n):
    screen.fill((255, 255, 255))
    block_size = 600 // n
    colors = [(255, 206, 158), (209, 139, 71)]  # Chessboard colors

    for col in range(n):
        for row in range(n):
            color = colors[(col + row) % 2]
            rect = pygame.Rect(col * block_size, row * block_size, block_size, block_size)
            pygame.draw.rect(screen, color, rect)

    for col in range(n):
        row = board[col]
        queen_rect = pygame.Rect(col * block_size, row * block_size, block_size, block_size)
        # Draw the queen (circle) in the center of the block with the text Q in the center
        pygame.draw.circle(screen, (0, 0, 0), queen_rect.center, block_size // 2 - 5)
        font = pygame.font.Font(None, block_size//2)
        text = font.render("Q", True, (255, 255, 255))
        text_rect = text.get_rect(center=queen_rect.center)
        screen.blit(text, text_rect)

    pygame.display.flip()


def run_algorithm(n, algorithm_name):
    """
    Run the selected algorithm and display the results using pygame.
    The algorithm returns by yielding the board at each iteration.
    Display the board at each iteration.
    :param n: Size of the board (number of queens).
    :param algorithm_name: The name of the algorithm to run.
    :return:
    """
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("N-Queens Visualization")
    clock = pygame.time.Clock()

    algorithms = {
        "genetic_algorithm": genetic_algorithm,
        "hill_climbing": hill_climbing,
        "simulated_annealing": simulated_annealing
    }

    algorithm = algorithms[algorithm_name]

    for board in algorithm(n):
        draw_board(screen, board, n)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

    # Keep the window open at the end
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()

    pygame.quit()


run_algorithm(20, "simulated_annealing")
