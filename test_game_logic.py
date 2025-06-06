import unittest
from game_logic import SimpleGameLogic, GeneralGameLogic
from game_logic import ComputerPlayer

class TestSimpleGameLogic(unittest.TestCase):

    def setUp(self):
        self.game = SimpleGameLogic(size=3)

    def test_initial_conditions(self):
        self.assertFalse(self.game.game_over)
        self.assertEqual(self.game.blue_score, 0)
        self.assertEqual(self.game.red_score, 0)

    def test_valid_move(self):
        result = self.game.make_move(0, 0, 'S')
        self.assertTrue(result)
        self.assertEqual(self.game.board[0][0], 'S')

    def test_invalid_move_out_of_bounds(self):
        result = self.game.make_move(-1, 0, 'S')
        self.assertFalse(result)

    def test_invalid_move_on_filled_cell(self):
        self.game.make_move(1, 1, 'O')
        result = self.game.make_move(1, 1, 'S')
        self.assertFalse(result)

    def test_sos_detection(self):
        self.game.make_move(0, 0, 'S')  # Blue
        self.game.make_move(1, 1, 'O')  # Red
        result = self.game.make_move(2, 2, 'S')  # Blue forms SOS
        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.blue_score, 1)
        self.assertEqual(self.game.get_winner(), 'blue')


class TestGeneralGameLogic(unittest.TestCase):

    def setUp(self):
        self.game = GeneralGameLogic(size=3)

    def test_game_not_over_on_first_sos(self):
        self.game.make_move(0, 0, 'S')  # Blue
        self.game.make_move(0, 1, 'O')  # Red
        self.game.make_move(0, 2, 'S')  # Blue forms SOS
        self.assertFalse(self.game.game_over)
        self.assertEqual(self.game.blue_score, 1)


class TestGameSetup(unittest.TestCase):

    def test_choose_board_size_simple_game(self):
        game = SimpleGameLogic(size=5)
        self.assertEqual(len(game.board), 5)
        self.assertEqual(len(game.board[0]), 5)

    def test_choose_board_size_general_game(self):
        game = GeneralGameLogic(size=7)
        self.assertEqual(len(game.board), 7)
        self.assertEqual(len(game.board[0]), 7)

    def test_new_simple_game_conditions(self):
        game = SimpleGameLogic(size=4)
        self.assertEqual(game.blue_score, 0)
        self.assertEqual(game.red_score, 0)
        self.assertFalse(game.game_over)
        self.assertTrue(all(cell == '' for row in game.board for cell in row))

    def test_new_general_game_conditions(self):
        game = GeneralGameLogic(size=4)
        self.assertEqual(game.blue_score, 0)
        self.assertEqual(game.red_score, 0)
        self.assertFalse(game.game_over)
        self.assertTrue(all(cell == '' for row in game.board for cell in row))

class TestComputerPlayer(unittest.TestCase):
    def test_computer_can_make_move(self):
        game = SimpleGameLogic(3)
        computer = ComputerPlayer("blue")
        move = computer.choose_move(game)
        self.assertIsNotNone(move)
        row, col, piece = move
        self.assertIn((row, col), [(i, j) for i in range(3) for j in range(3)])
        self.assertIn(piece, ['S', 'O'])
        self.assertEqual(game.board[row][col], '')
    
    def test_full_game_between_computers(self):
        game = SimpleGameLogic(3)
        blue = ComputerPlayer("blue")
        red = ComputerPlayer("red")

        while not game.game_over:
            current = blue if game.current_player == 'blue' else red
            move = current.choose_move(game)
            if move:
                row, col, piece = move
                game.make_move(row, col, piece)
            else:
                break  # no moves left

        self.assertTrue(game.game_over)

    def test_computer_picks_valid_cell_and_piece(self):
        game = SimpleGameLogic(3)
        computer = ComputerPlayer("blue")
        move = computer.choose_move(game)
        self.assertIsNotNone(move)
        row, col, piece = move
        self.assertTrue(0 <= row < 3 and 0 <= col < 3)
        self.assertIn(piece, ['S', 'O'])
        self.assertEqual(game.board[row][col], '')

if __name__ == "__main__":
    unittest.main()
