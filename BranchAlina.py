from fastapi import FastAPI, HTTPException

app = FastAPI()


class Board:
    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]

    def is_full(self):
        return all(cell != " " for row in self.board for cell in row)

    def check_winner(self):
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

    def make_move(self, row, col, player):
        if self.board[row][col] == " ":
            self.board[row][col] = player
            return True
        return False


class TicTacToe:
    def __init__(self):
        self.board = Board()
        self.current_player = "X"

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"


game = TicTacToe()


@app.get("/board")
def get_board():
    return {"board": game.board.board}


@app.post("/move")
def make_move(row: int, col: int):
    if row not in range(3) or col not in range(3):
        raise HTTPException(status_code=400, detail="Invalid move coordinates")

    if not game.board.make_move(row, col, game.current_player):
        raise HTTPException(status_code=400, detail="Invalid move, cell already taken")

    winner = game.board.check_winner()
    if winner:
        return {"message": f"Player {winner} wins!", "board": game.board.board}
    elif game.board.is_full():
        return {"message": "It's a tie!", "board": game.board.board}

    game.switch_player()
    return {"message": "Move successful", "board": game.board.board, "next_player": game.current_player}


@app.post("/reset")
def reset_game():
    global game
    game = TicTacToe()
    return {"message": "Game has been reset", "board": game.board.board}
