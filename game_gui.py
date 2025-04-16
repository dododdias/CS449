import tkinter as tk
from tkinter import ttk
from game_logic import SimpleGameLogic, GeneralGameLogic
from game_logic import HumanPlayer, ComputerPlayer

class SOSGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SOS Game")
        self.root.geometry("800x600")
        
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        ttk.Label(title_frame, text="SOS", font=('Arial', 16, 'bold')).grid(row=0, column=0, padx=20)
        
        self.game_mode = tk.StringVar(value="simple")
        ttk.Radiobutton(title_frame, text="Simple game", variable=self.game_mode, value="simple").grid(row=0, column=1, padx=10)
        ttk.Radiobutton(title_frame, text="General game", variable=self.game_mode, value="general").grid(row=0, column=2, padx=10)
        
        ttk.Label(title_frame, text="Board size").grid(row=0, column=3, padx=20)
        self.size_var = tk.StringVar(value="8")
        size_entry = ttk.Entry(title_frame, textvariable=self.size_var, width=3)
        size_entry.grid(row=0, column=4)

        # Blue player setup
        blue_frame = ttk.Frame(main_frame)
        blue_frame.grid(row=1, column=0, padx=20)
        ttk.Label(blue_frame, text="Blue player", font=('Arial', 12, 'bold'), foreground='blue').pack(pady=5)
        self.blue_s = tk.StringVar(value="S")
        ttk.Radiobutton(blue_frame, text="S", variable=self.blue_s, value="S").pack(pady=2)
        ttk.Radiobutton(blue_frame, text="O", variable=self.blue_s, value="O").pack(pady=2)

        ttk.Label(blue_frame, text="Player Type").pack(pady=(10, 2))
        self.blue_player_type = tk.StringVar(value="Human")
        ttk.Radiobutton(blue_frame, text="Human", variable=self.blue_player_type, value="Human").pack()
        ttk.Radiobutton(blue_frame, text="Computer", variable=self.blue_player_type, value="Computer").pack()

        # Game board frame
        self.game_frame = ttk.Frame(main_frame)
        self.game_frame.grid(row=1, column=1)

        # Red player setup
        red_frame = ttk.Frame(main_frame)
        red_frame.grid(row=1, column=2, padx=20)
        ttk.Label(red_frame, text="Red player", font=('Arial', 12, 'bold'), foreground='red').pack(pady=5)
        self.red_s = tk.StringVar(value="S")
        ttk.Radiobutton(red_frame, text="S", variable=self.red_s, value="S").pack(pady=2)
        ttk.Radiobutton(red_frame, text="O", variable=self.red_s, value="O").pack(pady=2)

        ttk.Label(red_frame, text="Player Type").pack(pady=(10, 2))
        self.red_player_type = tk.StringVar(value="Human")
        ttk.Radiobutton(red_frame, text="Human", variable=self.red_player_type, value="Human").pack()
        ttk.Radiobutton(red_frame, text="Computer", variable=self.red_player_type, value="Computer").pack()

        # Info display
        self.info_frame = ttk.Frame(main_frame)
        self.info_frame.grid(row=2, column=0, columnspan=3, pady=20)

        self.turn_label = ttk.Label(self.info_frame, text="Current turn: Blue", font=('Arial', 12))
        self.turn_label.pack()

        self.score_label = ttk.Label(self.info_frame, text="Blue: 0 - Red: 0", font=('Arial', 12))
        self.score_label.pack()

        # New Game button
        ttk.Button(main_frame, text="New Game", command=self.start_new_game).grid(row=3, column=0, columnspan=3)

        # Game init
        self.game = None
        self.buttons = []
        self.start_new_game()

    def start_new_game(self):
        try:
            size = int(self.size_var.get())
            if size < 3:
                size = 3
            elif size > 12:
                size = 12
            self.size_var.set(str(size))
        except ValueError:
            size = 8
            self.size_var.set("8")

        # Game logic
        if self.game_mode.get() == "simple":
            self.game = SimpleGameLogic(size)
        else:
            self.game = GeneralGameLogic(size)

        # Define players
        self.blue_player = HumanPlayer("blue") if self.blue_player_type.get() == "Human" else ComputerPlayer("blue")
        self.red_player = HumanPlayer("red") if self.red_player_type.get() == "Human" else ComputerPlayer("red")

        # Reset GUI board
        for widget in self.game_frame.winfo_children():
            widget.destroy()

        self.buttons = []
        for i in range(size):
            row_buttons = []
            for j in range(size):
                button = ttk.Button(self.game_frame, text='', width=3,
                                    command=lambda r=i, c=j: self.make_move(r, c))
                button.grid(row=i, column=j, padx=1, pady=1)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        self.update_display()
        self.root.after(300, self.try_computer_move)

    def make_move(self, row, col):
        if self.game.game_over:
            return

        current_piece = self.blue_s.get() if self.game.current_player == 'blue' else self.red_s.get()
        if self.game.make_move(row, col, current_piece):
            self.buttons[row][col].configure(text=current_piece)
            self.update_display()

            if self.game.game_over:
                self.show_game_over()
            else:
                self.root.after(300, self.try_computer_move)

    def update_display(self):
        color = 'blue' if self.game.current_player == 'blue' else 'red'
        self.turn_label.configure(text=f"Current turn: {self.game.current_player.title()}", foreground=color)
        self.score_label.configure(text=f"Blue: {self.game.blue_score} - Red: {self.game.red_score}")

    def show_game_over(self):
        winner = self.game.get_winner()
        message = "Game Over! "
        if winner == 'tie':
            message += "It's a tie!"
        else:
            message += f"{winner.title()} wins!"

        top = tk.Toplevel(self.root)
        top.title("Game Over")
        ttk.Label(top, text=message, padding=20).pack()
        ttk.Button(top, text="OK", command=top.destroy).pack()

    def try_computer_move(self):
        current_player = self.blue_player if self.game.current_player == 'blue' else self.red_player

        if isinstance(current_player, ComputerPlayer) and not self.game.game_over:
            move = current_player.choose_move(self.game)
            if move:
                row, col, piece = move  # ← agora vem a letra junto
                self.game.make_move(row, col, piece)
                self.buttons[row][col].configure(text=piece)
                self.update_display()

                if self.game.game_over:
                    self.show_game_over()
                else:
                    self.root.after(500, self.try_computer_move)
