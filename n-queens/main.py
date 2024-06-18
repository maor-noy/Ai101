import pygame
from genetic_algorithm import genetic_algorithm
from hill_climbing import hill_climbing
from simulated_annealing import simulated_annealing


def main_menu():
    """
    Display the main menu and allow the user to select an algorithm and board size.
    """
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("N-Queens Visualization - Main Menu")

    # Load background image
    # background_image = pygame.image.load("background.jpg")
    background_color = (173, 216, 230)

    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    options = ["Hill Climbing", "Simulated Annealing", "Genetic Algorithm"]
    algorithms = {
        "Hill Climbing": "hill_climbing",
        "Simulated Annealing": "simulated_annealing",
        "Genetic Algorithm": "genetic_algorithm"
    }

    selected_option = 0
    board_size = 8

    while True:
        screen.fill(background_color)  # Use background color or image
        # screen.blit(background_image, (0, 0))

        title_text = font.render("Select Algorithm", True, (0, 0, 128))
        screen.blit(title_text, (100, 50))

        # Instructions
        how_to1 = small_font.render("Use UP/DOWN to choose algorithm,", True, (255, 0, 0))
        how_to2 = small_font.render("Use LEFT/RIGHT to choose size", True, (255, 0, 0))
        how_to3 = small_font.render("Press ENTER to start", True, (255, 0, 0))
        screen.blit(how_to1, (100, 130))
        screen.blit(how_to2, (100, 160))
        screen.blit(how_to3, (100, 190))

        for i, option in enumerate(options):
            text_color = (255, 69, 0) if i == selected_option else (0, 0, 0)
            text = small_font.render(option, True, text_color)
            screen.blit(text, (100, 250 + i * 50))

        size_text = small_font.render(f"Board Size: {board_size}", True, (0, 0, 128))
        screen.blit(size_text, (100, 450))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    algorithm_name = algorithms[options[selected_option]]
                    run_algorithm(board_size, algorithm_name)
                    return
                elif event.key == pygame.K_RIGHT:
                    board_size = min(board_size + 1, 20)
                elif event.key == pygame.K_LEFT:
                    board_size = max(board_size - 1, 4)

        pygame.display.flip()
        clock.tick(30)


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


main_menu()
