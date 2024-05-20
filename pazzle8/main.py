import pygame
import search  # Ensure your `search` module is correctly implemented and available.


def do_move(start, zero_index, move):
    """
    Executes a move by swapping the zero tile with an adjacent tile.

    Args:
        start (list): The current state of the puzzle.
        zero_index (int): The current position of the zero tile.
        move (str): The move to be executed ('<', '>', '^', 'v').

    Returns:
        int: The new position of the zero tile.
    """
    if move == "<":
        start[zero_index], start[zero_index - 1] = start[zero_index - 1], start[zero_index]
        zero_index -= 1
    elif move == ">":
        start[zero_index], start[zero_index + 1] = start[zero_index + 1], start[zero_index]
        zero_index += 1
    elif move == "^":
        start[zero_index], start[zero_index - 3] = start[zero_index - 3], start[zero_index]
        zero_index -= 3
    elif move == "v":
        start[zero_index], start[zero_index + 3] = start[zero_index + 3], start[zero_index]
        zero_index += 3
    return zero_index

def swap(start, zero_index, move):
    """
    Swaps the zero tile with an adjacent tile based on the input move.

    Args:
        start (list): The current state of the puzzle.
        zero_index (int): The current position of the zero tile.
        move (str): The move to be executed ('left', 'right', 'up', 'down').

    Returns:
        int: The new position of the zero tile.
    """
    if move == "left" and zero_index % 3 != 0:
        start[zero_index], start[zero_index - 1] = start[zero_index - 1], start[zero_index]
        zero_index -= 1
    elif move == "right" and zero_index % 3 != 2:
        start[zero_index], start[zero_index + 1] = start[zero_index + 1], start[zero_index]
        zero_index += 1
    elif move == "up" and zero_index >= 3:
        start[zero_index], start[zero_index - 3] = start[zero_index - 3], start[zero_index]
        zero_index -= 3
    elif move == "down" and zero_index < 6:
        start[zero_index], start[zero_index + 3] = start[zero_index + 3], start[zero_index]
        zero_index += 3
    return zero_index

def main():
    """
    Main function to run the 8-puzzle game using Pygame.
    """
    # Initial state setup
    start = [0, 1, 2, 3, 4, 5, 6, 7, 8]  # Example starting state
    zero_index = start.index(0)
    colors = ["white", "green", "blue", "yellow", "purple", "orange", "pink", "brown", "gray"]
    solution = ""
    solve = False
    count = 0

    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((300, 400))
    pygame.display.set_caption("8 Puzzle")
    screen.fill("white")

    font = pygame.font.Font(None, 36)
    solve_text = font.render("Solve", True, "black")
    solve_rect = solve_text.get_rect(center=(150, 350))

    # Create rectangles for the 3x3 grid
    rects = [pygame.Rect(j * 100, i * 100, 100, 100) for i in range(3) for j in range(3)]
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if solve_rect.collidepoint(x, y):
                    solve = True
                    solution = search.search(3, start)  # Assumes search.search returns a solution path
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    zero_index = swap(start, zero_index, "left")
                elif event.key == pygame.K_RIGHT:
                    zero_index = swap(start, zero_index, "right")
                elif event.key == pygame.K_UP:
                    zero_index = swap(start, zero_index, "up")
                elif event.key == pygame.K_DOWN:
                    zero_index = swap(start, zero_index, "down")

        screen.fill("white")
        screen.blit(solve_text, solve_rect)

        # Render the puzzle grid with current state
        for i, r in enumerate(rects):
            pygame.draw.rect(screen, colors[start[i]], r)
            if start[i] != 0:
                text = font.render(str(start[i]), True, "white")
                text_rect = text.get_rect(center=r.center)
                screen.blit(text, text_rect)

        if solve:
            if count < len(solution):
                zero_index = do_move(start, zero_index, solution[count])
                count += 1
            else:
                solve = False
                count = 0

        pygame.display.flip()
        clock.tick(5) if solve else clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
