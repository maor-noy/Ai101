import tkinter as tk
from tkinter import filedialog, messagebox
import search  # Ensure your `search` module is correctly implemented and available.
from state import if_legal  # Renamed for clarity
import random


N = 3  # Initial dimension of the puzzle (3x3)
puzzle = list(range(N * N))  # Initial puzzle state


def shuffle_puzzle():
    """Shuffles the puzzle by making random legal moves."""
    zero_pos = puzzle.index(0)
    for _ in range(100):
        valid_moves = get_valid_moves(zero_pos)
        move = random.choice(valid_moves)
        if_legal(puzzle, move)  # Update zero_pos after each move


def get_valid_moves(zero_pos):
    """Returns a list of valid moves based on the zero tile position."""
    valid_moves = []
    if zero_pos % N != 0:
        valid_moves.append('<')
    if (zero_pos + 1) % N != 0:
        valid_moves.append('>')
    if zero_pos >= N:
        valid_moves.append('^')
    if zero_pos < N * (N - 1):
        valid_moves.append('v')
    return valid_moves


def next_move(move_count, solution_moves):
    """Advances the solution by one move if available, otherwise stops solving."""
    if move_count < len(solution_moves):
        if_legal(puzzle, solution_moves[move_count])
        move_count += 1
    else:
        return False, 0  # Stop solving and reset move count
    return True, move_count


def hash_num_to_rgb(num):
    """Converts a number to RGB color values."""
    if num == 0:
        return 255, 255, 255
    return (num * 120) % 255, (num * 30) % 255, (num * 80) % 255


def press_key(event):
    """Handles keyboard input for moving the tile."""
    key = event.keysym
    moves = {'Left': '<', 'Right': '>', 'Up': '^', 'Down': 'v'}
    move = moves.get(key)
    if move:
        if_legal(puzzle, move)


def import_photo():
    """Opens a file dialog to select an image."""
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        messagebox.showinfo("Selected File", f"File selected: {file_path}")


def change_level(root, canvas, button_frame):
    """Changes the puzzle level by updating dimensions and UI elements."""
    global N, puzzle

    def set_level(new_level):
        global N, puzzle
        N = new_level
        puzzle = list(range(N * N))
        new_width, new_height = N * 100, N * 100 + 50
        canvas.config(width=new_width, height=new_height)
        button_frame.place(relx=0.5, rely=(new_width + 20) / new_height, anchor=tk.CENTER)
        root.geometry(f"{new_width}x{new_height + 20}")  # Adjust the main window size
        root.update()
        level_window.destroy()

    level_window = tk.Toplevel(root)
    level_window.title("Change Level")
    level_window.geometry("200x100")

    scale = tk.Scale(level_window, from_=3, to=5, orient=tk.HORIZONTAL, label="Select Level")
    scale.pack(pady=10)

    set_button = tk.Button(level_window, text="Set Level", command=lambda: set_level(scale.get()))
    set_button.pack(pady=5)


def main():
    solution_moves = []
    solving = False
    move_count = 0

    def start_solving():
        """Attempts to find a solution for the current puzzle and starts animating it."""
        nonlocal solving, solution_moves, move_count
        solution_moves = search.search(puzzle)
        solving = True
        move_count = 0

    def game_loop():
        """Continuously updates the game window based on the current state."""
        nonlocal solving, move_count
        canvas.delete("all")
        for i, num in enumerate(puzzle):
            x, y = i % N, i // N
            fill_color = "#d3d3d3" if num == 0 else "#%02x%02x%02x" % hash_num_to_rgb(num)
            canvas.create_rectangle(x * 100, y * 100, (x + 1) * 100, (y + 1) * 100, fill=fill_color, outline="#000000")
            if num != 0:
                canvas.create_text(x * 100 + 50, y * 100 + 50, text=str(num), font=("Arial", 24, "bold"), fill="#000000")

        if solving:
            solving, move_count = next_move(move_count, solution_moves)

        root.after(100, game_loop)

    root = tk.Tk()
    root.title("8-Puzzle")
    root.configure(bg="#ececec")
    root.resizable(False, False)  # Disable window resizing
    root.bind("<Key>", lambda event: press_key(event))
    root.geometry(f"{N * 100}x{N * 100 + 70}")

    # Menu bar setup
    menu = tk.Menu(root)
    root.config(menu=menu)

    filemenu = tk.Menu(menu, tearoff=0)
    filemenu.add_command(label='Change Level', command=lambda: change_level(root, canvas, button_frame))
    filemenu.add_command(label='Import Photo', command=import_photo)
    filemenu.add_separator()
    filemenu.add_command(label='Exit', command=root.quit)
    menu.add_cascade(label='File', menu=filemenu)

    helpmenu = tk.Menu(menu, tearoff=0)
    helpmenu.add_command(label='How to play', command=lambda: messagebox.showinfo("How to play", "Use the arrow keys "
                                                                                                 "(Up, Down, Left, "
                                                                                                 "Right) on your "
                                                                                                 "keyboard to slide "
                                                                                                 "the empty space "
                                                                                                 "tile and rearrange "
                                                                                                 "the numbered tiles. "
                                                                                                 "Try to solve the "
                                                                                                 "puzzle by arranging "
                                                                                                 "the numbers in "
                                                                                                 "ascending order."))

    helpmenu.add_command(label='About', command=lambda: messagebox.showinfo("About", "The 8-Puzzle is a classic "
                                                                                     "sliding tile puzzle. It "
                                                                                     "consists of a square frame with "
                                                                                     "8 numbered tiles and an empty "
                                                                                     "space. The goal is to rearrange "
                                                                                     "the tiles using the empty space "
                                                                                     "to achieve a specific order, "
                                                                                     "typically with numbers "
                                                                                     "increasing left to right and "
                                                                                     "top to bottom.  This refactored "
                                                                                     "code provides a graphical user "
                                                                                     "interface for the game, "
                                                                                     "allowing you to shuffle the "
                                                                                     "puzzle, solve it automatically, "
                                                                                     "change the puzzle size, "
                                                                                     "and potentially customize tile "
                                                                                     "colors.  Use the arrow keys to "
                                                                                     "move the tiles and have fun!"))
    menu.add_cascade(label='Help', menu=helpmenu)

    # Canvas setup
    canvas = tk.Canvas(root, width=N * 100, height=N * 100 + 50, bg="#f0f0f0", highlightthickness=0)
    canvas.pack()

    # Button frame setup
    button_frame = tk.Frame(root, bg="#f0f0f0")
    button_frame.place(relx=0.5, rely=(N * 100+20) / (N * 100 + 50), anchor=tk.CENTER)

    # Shuffle and Solve buttons
    shuffle_button = tk.Button(button_frame, text="Shuffle", command=lambda: shuffle_puzzle(), width=10, height=2, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
    shuffle_button.pack(side=tk.LEFT, padx=10, pady=10)

    solve_button = tk.Button(button_frame, text="Solve", command=start_solving, width=10, height=2, bg="#2196F3", fg="white", font=("Arial", 12, "bold"))
    solve_button.pack(side=tk.RIGHT, padx=10, pady=10)

    # Start game loop
    game_loop()
    root.mainloop()


if __name__ == "__main__":
    main()
