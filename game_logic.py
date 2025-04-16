import random
class BaseGameLogic:
    def __init__(self, size):
        self.size = size
        self.board = [['' for _ in range(size)] for _ in range(size)]
        self.current_player = 'blue'  # 'blue' or 'red'
        self.game_over = False
        self.blue_score = 0
        self.red_score = 0

    def make_move(self, row, col, piece):
        """
        Attempts to make a move on the board.
        Returns True if move is valid, False otherwise.
        """
        if not self.is_valid_move(row, col):
            return False

        self.board[row][col] = piece
        self.check_sos(row, col, piece)
        
        self.check_game_over()
        
        if not self.game_over:
            self.current_player = 'red' if self.current_player == 'blue' else 'blue'
        
        return True

    def is_valid_move(self, row, col):
        """Check if the move is valid."""
        return (0 <= row < self.size and 
                0 <= col < self.size and 
                self.board[row][col] == '' and 
                not self.game_over)

    def check_sos(self, row, col, piece):
        """Check if the move creates an SOS."""
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        for dx, dy in directions:
            if piece == 'S':
                # Check for "SOS" pattern
                try:
                    if (self.board[row + dx][col + dy] == 'O' and 
                        self.board[row + 2*dx][col + 2*dy] == 'S'):
                        if self.current_player == 'blue':
                            self.blue_score += 1
                        else:
                            self.red_score += 1
                except IndexError:
                    continue
            elif piece == 'O':
                # Check for "SOS" pattern with O in the middle
                try:
                    if (self.board[row - dx][col - dy] == 'S' and 
                        self.board[row + dx][col + dy] == 'S'):
                        if self.current_player == 'blue':
                            self.blue_score += 1
                        else:
                            self.red_score += 1
                except IndexError:
                    continue

    def is_board_full(self):
        """Check if the board is full."""
        return all(all(cell != '' for cell in row) for row in self.board)

    def check_game_over(self):
        """Check if game should be over (to be implemented by subclasses)"""
        raise NotImplementedError

    def get_winner(self):
        """Returns the winner of the game."""
        if not self.game_over:
            return None
        if self.blue_score > self.red_score:
            return 'blue'
        elif self.red_score > self.blue_score:
            return 'red'
        return 'tie'


class SimpleGameLogic(BaseGameLogic):
    def check_game_over(self):
        """Simple game ends when first SOS is created or board is full with no SOS"""
        if self.blue_score > 0 or self.red_score > 0:
            self.game_over = True
        elif self.is_board_full():
            self.game_over = True


class GeneralGameLogic(BaseGameLogic):
    def check_game_over(self):
        """General game ends when board is full"""
        if self.is_board_full():
            self.game_over = True


class Player:
    def __init__(self, color):
        self.color = color  # 'blue' or 'red'

    def choose_move(self, game):
        """To be overridden in subclasses"""
        pass

class HumanPlayer(Player):
    def choose_move(self, game):
        """O input do humano vem pela GUI, então não faz nada aqui"""
        return None  # Será ignorado

class ComputerPlayer(Player):
    def choose_move(self, game):
        empty_cells = [(i, j) for i in range(game.size) for j in range(game.size) if game.board[i][j] == '']
        if not empty_cells:
            return None
        row, col = random.choice(empty_cells)
        piece = random.choice(['S', 'O'])  # ← o computador escolhe a letra também
        return row, col, piece
