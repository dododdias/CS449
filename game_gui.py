import tkinter as tk
from tkinter import ttk
from game_logic import SimpleGameLogic, GeneralGameLogic

class SOSGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SOS Game")
        self.root.geometry("800x600")
        
        # Main
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title and game setup frame
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        ttk.Label(title_frame, text="SOS", font=('Arial', 16, 'bold')).grid(row=0, column=0, padx=20)
        
        # Game mode selection
        self.game_mode = tk.StringVar(value="simple")
        ttk.Radiobutton(title_frame, text="Simple game", variable=self.game_mode, 
                       value="simple").grid(row=0, column=1, padx=10)
        ttk.Radiobutton(title_frame, text="General game", variable=self.game_mode, 
                       value="general").grid(row=0, column=2, padx=10)
        
        # Board size selection
        ttk.Label(title_frame, text="Board size").grid(row=0, column=3, padx=20)
        self.size_var = tk.StringVar(value="8")
        size_entry = ttk.Entry(title_frame, textvariable=self.size_var, width=3)
        size_entry.grid(row=0, column=4)
        
        # Player frames
        # Blue player frame (left side)
        blue_frame = ttk.Frame(main_frame)
        blue_frame.grid(row=1, column=0, padx=20)
        ttk.Label(blue_frame, text="Blue player", font=('Arial', 12, 'bold'),
                 foreground='blue').pack(pady=5)
        self.blue_s = tk.StringVar(value="S")
        ttk.Radiobutton(blue_frame, text="S", variable=self.blue_s, 
                       value="S").pack(pady=2)
        ttk.Radiobutton(blue_frame, text="O", variable=self.blue_s, 
                       value="O").pack(pady=2)
        
        # Game board frame (center)
        self.game_frame = ttk.Frame(main_frame)
        self.game_frame.grid(row=1, column=1)
        
        # Red player frame (right side)
        red_frame = ttk.Frame(main_frame)
        red_frame.grid(row=1, column=2, padx=20)
        ttk.Label(red_frame, text="Red player", font=('Arial', 12, 'bold'),
                 foreground='red').pack(pady=5)
        self.red_s = tk.StringVar(value="S")
        ttk.Radiobutton(red_frame, text="S", variable=self.red_s, 
                       value="S").pack(pady=2)
        ttk.Radiobutton(red_frame, text="O", variable=self.red_s, 
                       value="O").pack(pady=2)
        
        # Current turn and score labels
        self.info_frame = ttk.Frame(main_frame)
        self.info_frame.grid(row=2, column=0, columnspan=3, pady=20)
        
        self.turn_label = ttk.Label(self.info_frame, text="Current turn: Blue", 
                                  font=('Arial', 12))
        self.turn_label.pack()
        
        self.score_label = ttk.Label(self.info_frame, text="Blue: 0 - Red: 0", 
                                   font=('Arial', 12))
        self.score_label.pack()
        
        # New Game button
        ttk.Button(main_frame, text="New Game", 
                  command=self.start_new_game).grid(row=3, column=0, columnspan=3)
        
        # Initialize game
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
            
        # Create the appropriate game instance based on mode
        if self.game_mode.get() == "simple":
            self.game = SimpleGameLogic(size)
        else:
            self.game = GeneralGameLogic(size)
        
        # Clear existing board
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        
        # Create new board
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

    def make_move(self, row, col):
        current_piece = self.blue_s.get() if self.game.current_player == 'blue' else self.red_s.get()
        if self.game.make_move(row, col, current_piece):
            self.buttons[row][col].configure(text=current_piece)
            self.update_display()
            
            if self.game.game_over:
                self.show_game_over()

    def update_display(self):
        # Update turn indicator
        color = 'blue' if self.game.current_player == 'blue' else 'red'
        self.turn_label.configure(text=f"Current turn: {self.game.current_player.title()}",
                                foreground=color)
        
        # Update score
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
