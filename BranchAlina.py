def check_winner(self) -> Optional[str]:
    # Check rows
    for row in self.board:
        if row[0] == row[1] == row[2] and row[0] != " ":
            return row[0]

    # Check columns
    for col in range(3):
        if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != " ":
            return self.board[0][col]

    # Check diagonals
    if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != " ":
        return self.board[0][0]
    if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != " ":
        return self.board[0][2]

    return None


def make_move(self, row: int, col: int, player: str) -> bool:
    if self.board[row][col] == " ":
        self.board[row][col] = player
        return True