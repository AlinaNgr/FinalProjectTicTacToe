import unittest
from app.game import Board


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_initial_board_empty(self):
        expected = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.assertEqual(self.board.display(), expected)

    def test_is_full_false(self):
        self.assertFalse(self.board.is_full())

    def test_is_full_true(self):
        full_board = [["X", "O", "X"], ["O", "X", "O"], ["X", "X", "O"]]
        self.board = Board(full_board)
        self.assertTrue(self.board.is_full())

    def test_check_winner_row(self):
        self.board = Board([["X", "X", "X"], [" ", "O", " "], ["O", " ", " "]])
        self.assertEqual(self.board.check_winner(), "X")

    def test_check_winner_column(self):
        self.board = Board([["O", "X", " "], ["O", "X", " "], ["O", " ", "X"]])
        self.assertEqual(self.board.check_winner(), "O")

    def test_check_winner_diagonal(self):
        self.board = Board([["X", " ", "O"], [" ", "X", " "], ["O", " ", "X"]])
        self.assertEqual(self.board.check_winner(), "X")

    def test_check_winner_no_winner(self):
        self.board = Board([["X", "O", "X"], ["O", "X", "O"], ["O", "X", "O"]])
        self.assertIsNone(self.board.check_winner())

    def test_make_move_valid(self):
        self.assertTrue(self.board.make_move(0, 0, "X"))
        self.assertEqual(self.board.display()[0][0], "X")

    def test_make_move_invalid(self):
        self.board.make_move(0, 0, "X")
        self.assertFalse(self.board.make_move(0, 0, "O"))  # Already occupied


if __name__ == "__main__":
    unittest.main()