import pytest
from game_board import Board


def test_display_initial_state():
    board = Board()
    expected_initial_state = [[" " for _ in range(3)] for _ in range(3)]
    assert board.display() == expected_initial_state, "Initial board state should be empty."


def test_is_full_initial_state():
    board = Board()
    assert not board.is_full(), "Board should not be full when initialized."


def test_is_full_after_filling_board():
    board = Board()
    board.board = [["X", "O", "X"], ["X", "X", "O"], ["O", "X", "O"]]
    assert board.is_full(), "Board should be full when all cells are filled."


def test_is_full_with_empty_cells():
    board = Board()
    board.board = [["X", "O", "X"], ["X", " ", "O"], ["O", "X", "O"]]
    assert not board.is_full(), "Board should not be full when there are empty cells."


if __name__ == "main":
    pytest.main()
