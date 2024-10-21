import unittest
from unittest.mock import MagicMock
from app.game import Board
from app.ai import TicTacToeAI  # Replace 'your_module' with the actual module name


class TestTicTacToeAI(unittest.TestCase):
    def setUp(self):
        self.board = MagicMock(spec=Board)
        self.ai = TicTacToeAI(self.board)

    def test_minimax_winner_O(self):
        self.board.check_winner.return_value = "O"
        score = self.ai.minimax(0, True)
        self.assertEqual(score, 1)

    def test_minimax_winner_X(self):
        self.board.check_winner.return_value = "X"
        score = self.ai.minimax(0, True)
        self.assertEqual(score, -1)

    def test_minimax_draw(self):
        self.board.check_winner.return_value = None
        self.board.is_full.return_value = True
        score = self.ai.minimax(0, True)
        self.assertEqual(score, 0)

    def test_find_best_move(self):
        self.board.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]  # Empty board
        self.board.check_winner.return_value = None
        self.board.is_full.return_value = False

        # Mocking the minimax call to return specific scores based on the moves
        self.ai.minimax = MagicMock(side_effect=[1, -1, 1, 0, 1, -1, 1, 0, -1])

        best_move = self.ai.find_best_move()
        self.assertEqual(best_move, (0, 0))  # Example best move; adjust based on your logic


if __name__ == '__main__':
    unittest.main()
