class GameLogic:
    def __init__(self, size, gamemode="simple"):
        self.size = size
        self.gamemode = gamemode  # "simple" or "general"
        self.board = [['' for _ in range(size)] for _ in range(size)]
        self.currentplayer = 'blue'  # 'blue' or 'red'
        self.gameover = False
        self.bluescore = 0
        self.redscore = 0

    def makemove(self, row, col, piece):
        # Try to make a move on the board. Output is True if move is valid, False if not.

        if not self.is_valid_move(row, col):
            return False

        self.board[row][col] = piece
        self.checksos(row, col, piece)
        
        if not self.gamemode == "general":
            if self.bluescore > 0 or self.redscore > 0:
                self.gameover = True
        elif self.is_board_full():
            self.gameover = True

        if not self.gameover:
            self.currentplayer = 'red' if self.currentplayer == 'blue' else 'blue'
        
        return True

    def is_valid_move(self, row, col):
        #Check if is valid.
        return (0 <= row < self.size and 
                0 <= col < self.size and 
                self.board[row][col] == '' and 
                not self.gameover)

    def checksos(self, row, col, piece):
        #check if creates SOS
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        for dx, dy in directions:
            if piece == 'S':
                #Check for "SOS" 
                try:
                    if (self.board[row + dx][col + dy] == 'O' and 
                        self.board[row + 2*dx][col + 2*dy] == 'S'):
                        if self.currentplayer == 'blue':
                            self.bluescore += 1
                        else:
                            self.redscore += 1
                except IndexError:
                    continue
            elif piece == 'O':
                # Check for SOS with O in the middle
                try:
                    if (self.board[row - dx][col - dy] == 'S' and 
                        self.board[row + dx][col + dy] == 'S'):
                        if self.currentplayer == 'blue':
                            self.bluescore += 1
                        else:
                            self.redscore += 1
                except IndexError:
                    continue

    def is_board_full(self):
        #check if board is full
        return all(all(cell != '' for cell in row) for row in self.board)

    def get_winner(self):
        #gets the winner
        if not self.gameover:
            return None
        if self.bluescore > self.redscore:
            return 'blue'
        elif self.redscore > self.bluescore:
            return 'red'
        return 'tie'
