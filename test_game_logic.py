import unittest
from game_logic import GameLogic

class TestGameLogic(unittest.TestCase):

    def test_init_correct_board_size(self):
        # Test initialization of the board with different sizes
        for size in [3, 5, 8]:
            game = GameLogic(size)
            self.assertEqual(len(game.board), size)
            self.assertEqual(len(game.board[0]), size)

    def test_init_game_mode(self):
        # Test initialization of the game mode
        game = GameLogic(5, "general")
        self.assertEqual(game.game_mode, "general")

    def test_start_new_game(self):
        # Test if a new game starts with specified settings
        game = GameLogic(5, "simple")
        self.assertEqual(game.size, 5)
        self.assertEqual(game.game_mode, "simple")
        self.assertFalse(game.game_over)
        self.assertEqual(game.current_player, 'blue')

    def test_make_move_simple(self):
        # Test making a move in a simple game
        game = GameLogic(3, "simple")
        result = game.make_move(0, 0, 'S')
        self.assertTrue(result)
        self.assertEqual(game.board[0][0], 'S')

    def test_make_move_general(self):
        # Test making a move in a general game
        game = GameLogic(3, "general")
        result = game.make_move(1, 1, 'O')
        self.assertTrue(result)
        self.assertEqual(game.board[1][1], 'O')

    def test_invalid_move(self):
        # Test attempting an invalid move
        game = GameLogic(3, "simple")
        game.make_move(0, 0, 'S')  # Valid move
        result = game.make_move(0, 0, 'O')  # Invalid move, spot taken
        self.assertFalse(result)

    def test_game_over_condition(self):
        # Test game over condition in a simple game
        game = GameLogic(3, "simple")
        game.make_move(0, 0, 'S')
        game.make_move(0, 1, 'O')
        game.make_move(0, 2, 'S')
        game.blue_score = 1  # Simulate scoring to trigger game over
        self.assertTrue(game.game_over)

    def test_get_winner(self):
        # Test correctly identifying the winner
        game = GameLogic(3, "simple")
        game.blue_score = 2
        game.red_score = 1
        game.game_over = True
        self.assertEqual(game.get_winner(), 'blue')

if __name__ == '__main__':
    unittest.main()

