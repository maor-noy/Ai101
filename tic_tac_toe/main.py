import tkinter as tk
from tkinter import messagebox
import random

# Global variables to maintain the game state
game_active = True
current_player = 'X'
game_board = ['' for _ in range(9)]
winning_pattern = []
bot_active = False
cells = []


def toggle_bot():
    global bot_active
    bot_active = not bot_active


def reset_board():
    global game_board, game_active, current_player
    game_board = ['' for _ in range(9)]
    for cell in cells:
        cell.config(text='', state=tk.NORMAL, bg='white')
    current_player = 'X'
    game_active = True


def handle_click(index):
    global game_active, current_player
    if not game_active or game_board[index]:
        return

    update_cell(index, current_player)

    if check_winner():
        game_active = False
        highlight_winner_cells()
        messagebox.showinfo("Game Over", f"Player {current_player} wins!")
    elif check_tie():
        game_active = False
        messagebox.showinfo("Game Over", "It's a tie!")
    else:
        current_player = 'O' if current_player == 'X' else 'X'
        if bot_active and current_player == 'O':
            bot_move()


def update_cell(index, player):
    global game_board
    game_board[index] = player
    cells[index].config(text=player, state=tk.DISABLED, disabledforeground="#3498db" if player == 'X' else "#e74c3c")


def check_winner():
    win_patterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]

    for pattern in win_patterns:
        a, b, c = pattern
        if game_board[a] and game_board[a] == game_board[b] == game_board[c]:
            global winning_pattern
            winning_pattern = pattern
            return True
    return False


def check_tie():
    return all(game_board)


def highlight_winner_cells():
    for index in winning_pattern:
        cells[index].config(bg='#2ecc71')


def bot_move():
    empty_cells = [i for i, cell in enumerate(game_board) if not cell]
    index = random.choice(empty_cells)
    handle_click(index)


def create_widgets(_root):
    title_label = tk.Label(root, text="Tic Tac Toe", font=("Arial", 24, "bold"), bg='#2980b9', fg='white')
    title_label.pack(pady=20)

    switch_frame = tk.Frame(root, bg='#2980b9')
    switch_frame.pack(pady=10)

    switch_label = tk.Label(switch_frame, text="Computer player:", font=("Arial", 12, "bold"), bg='#2980b9', fg='white')
    switch_label.pack(side=tk.LEFT)

    switch_var = tk.IntVar()
    switch = tk.Checkbutton(switch_frame, variable=switch_var, command=toggle_bot, font=("Arial", 12, "bold"),
                            bg='#2980b9', fg='white', selectcolor='#27ae60')
    switch.pack(side=tk.LEFT)

    board_frame = tk.Frame(root, bg='#2980b9')
    board_frame.pack(pady=10)

    global cells
    for i in range(9):
        cell = tk.Button(board_frame, text='', font=("Brush Script MT", 32, "bold"), width=5, height=2,
                         command=lambda j=i: handle_click(j), bg='white', fg='#2c3e50', activebackground='#bdc3c7',
                         relief='ridge', bd=5)
        cell.grid(row=i // 3, column=i % 3, padx=5, pady=5)
        cells.append(cell)

    reset_button = tk.Button(root, text="Reset Board", font=("Arial", 12, "bold"), command=reset_board,
                             bg='#c0392b', fg='white', activebackground='#e74c3c', relief='raised', bd=5)
    reset_button.pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tic Tac Toe")
    root.configure(bg='#2980b9')

    create_widgets(root)
    reset_board()

    root.mainloop()
