import pygame
import search  # Ensure your `search` module is correctly implemented and available.
from state import if_legal
import random


def shuffle_puzzle(puzzle):
    """
    Shuffles the puzzle by executing 100 random moves.

    Args:
        puzzle (list): The current state of the puzzle.
        zero_pos (int): The current position of the zero tile.

    Returns:
        int: The new position of the zero tile.
    """
    zero_pos = puzzle.index(0)
    for _ in range(100):
        valid_moves = []
        if zero_pos % 3 != 0:
            valid_moves.append('<')
        if zero_pos % 3 != 2:
            valid_moves.append('>')
        if zero_pos >= 3:
            valid_moves.append('^')
        if zero_pos < 6:
            valid_moves.append('v')
        move = random.choice(valid_moves)
        if_legal(puzzle, move)


def main():
    """
    Main function to run the 8-puzzle game using Pygame.
    """
    # Initial state setup
    puzzle = list(range(9))
    zero_pos = puzzle.index(0)
    tile_colors = ["white", "green", "blue", "yellow", "purple", "orange", "pink", "brown", "gray"]
    solution_moves = ""
    solving = False
    move_count = 0  # Counter to keep track of the moves in the solution

    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((300, 400))
    pygame.display.set_caption("8 Puzzle")
    screen.fill("white")

    font = pygame.font.Font(None, 36)
    solve_text = font.render("Solve", True, "black")
    solve_rect = solve_text.get_rect(center=(150, 370))

    shuffle_text = font.render("Shuffle", True, "black")
    shuffle_rect = shuffle_text.get_rect(center=(150, 320))

    # Create rectangles for the 3x3 grid
    tile_rects = [pygame.Rect(j * 100, i * 100, 100, 100) for i in range(3) for j in range(3)]
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            # Check if the user has clicked the close button
            if event.type == pygame.QUIT:
                running = False

            # Check if the user has clicked the solve button
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if solve_rect.collidepoint(x, y):
                    solving = True
                    solution_moves = search.search(puzzle)
                elif shuffle_rect.collidepoint(x, y):
                    shuffle_puzzle(puzzle)

            # Check if the user has pressed any key to move the tiles
            elif event.type == pygame.KEYDOWN and not solving:
                if event.key == pygame.K_LEFT:
                    if_legal(puzzle, "<")
                elif event.key == pygame.K_RIGHT:
                    if_legal(puzzle, ">")
                elif event.key == pygame.K_UP:
                    if_legal(puzzle, "^")
                elif event.key == pygame.K_DOWN:
                    if_legal(puzzle, "v")

        screen.blit(solve_text, solve_rect)
        screen.blit(shuffle_text, shuffle_rect)

        # Render the puzzle grid with current state
        for i, rect in enumerate(tile_rects):
            pygame.draw.rect(screen, tile_colors[puzzle[i]], rect)
            if puzzle[i] != 0:
                text = font.render(str(puzzle[i]), True, "white")
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

        if solving:
            if move_count < len(solution_moves):
                if_legal(puzzle, solution_moves[move_count])
                move_count += 1
            else:
                solving = False
                move_count = 0

        pygame.display.flip()
        clock.tick(5) if solving else clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
