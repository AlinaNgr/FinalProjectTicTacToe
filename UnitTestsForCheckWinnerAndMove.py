import unittest
from typing import Optional

class TestTicTacToe(unittest.TestCase):

    def setUp(self):
        # Inițializez un board gol pentru fiecare test
        self.board = [[" " for _ in range(3)] for _ in range(3)]

    def check_winner(self) -> Optional[str]:
        # Codul pe care îl testăm (deja dat)
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] != " ":
                return row[0]

        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != " ":
                return self.board[0][col]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != " ":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != " ":
            return self.board[0][2]

        return None

    def make_move(self, row: int, col: int, player: str) -> bool:
        # Codul pe care îl testăm (deja dat)
        if self.board[row][col] == " ":
            self.board[row][col] = player
            return True
        return False

    def test_check_winner_row(self):
        # Test pentru câștig pe un rând
        self.board = [["X", "X", "X"],
                      [" ", "O", " "],
                      ["O", " ", "O"]]
        self.assertEqual(self.check_winner(), "X")

    def test_check_winner_column(self):
        # Test pentru câștig pe o coloană
        self.board = [["X", "O", " "],
                      ["X", "O", " "],
                      ["X", " ", "O"]]
        self.assertEqual(self.check_winner(), "X")

    def test_check_winner_diagonal1(self):
        # Test pentru câștig pe prima diagonală
        self.board = [["O", "X", " "],
                      ["X", "O", " "],
                      [" ", "X", "O"]]
        self.assertEqual(self.check_winner(), "O")

    def test_check_winner_diagonal2(self):
        # Test pentru câștig pe a doua diagonală
        self.board = [["X", " ", "O"],
                      ["X", "O", " "],
                      ["O", " ", " "]]
        self.assertEqual(self.check_winner(), "O")

    def test_no_winner(self):
        # Test când nu există câștigător
        self.board = [["X", "O", "X"],
                      ["O", "X", "O"],
                      ["O", "X", "O"]]
        self.assertIsNone(self.check_winner())

    def test_make_move_valid(self):
        # Test pentru mișcare validă
        self.assertTrue(self.make_move(0, 0, "X"))
        self.assertEqual(self.board[0][0], "X")

    def test_make_move_invalid(self):
        # Test pentru mișcare invalidă (loc deja ocupat)
        self.board[0][0] = "O"
        self.assertFalse(self.make_move(0, 0, "X"))
        self.assertEqual(self.board[0][0], "O")

if __name__ == "__main__":
    unittest.main()
