from fastapi import HTTPException, Depends, status, Request
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from schema import UserCreate, Client
from models import User, GameState
from database import SessionLocal
import json

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Utility functions
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate) -> Client:
    db_user = get_user_by_username(db, user.username)
    if db_user is not None:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Creează starea jocului cu tabloul serializat ca JSON
    db_game_state = GameState(user_id=db_user.id, board=json.dumps([[" " for _ in range(3)] for _ in range(3)]),
                              current_player="X")
    db.add(db_game_state)
    db.commit()
    db.refresh(db_game_state)
    return Client(user_id=db_user.id, username=db_user.username)


def get_game_state(db: Session, user_id: int, game_id: int) -> Optional[GameState]:
    return db.query(GameState).filter(GameState.user_id == user_id, GameState.id == game_id).first()

# Authenticated User dependency
def get_current_user(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user


# Board management
class Board:
    def _init_(self, board: Optional[List[List[str]]] = None):
        self.board = board or [[" " for _ in range(3)] for _ in range(3)]

    def display(self) -> List[List[str]]:
        return self.board

    def is_full(self) -> bool:
        return all(cell != " " for row in self.board for cell in row)

    def check_winner(self) -> Optional[str]:
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
        if self.board[row][col] == " ":
            self.board[row][col] = player
            return True
        return False


# TicTacToe game management
class TicTacToe:
    def _init_(self, board: Optional[List[List[str]]] = None, current_player: str = "X"):
        self.board = Board(board)
        self.current_player = current_player

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def minimax(self, depth: int, is_maximizing: bool) -> int:
        winner = self.board.check_winner()
        if winner == "O":
            return 1
        elif winner == "X":
            return -1
        elif self.board.is_full():
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board.board[i][j] == " ":
                        self.board.board[i][j] = "O"
                        score = self.minimax(depth + 1, False)
                        self.board.board[i][j] = " "
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board.board[i][j] == " ":
                        self.board.board[i][j] = "X"
                        score = self.minimax(depth + 1, True)
                        self.board.board[i][j] = " "
                        best_score = min(score, best_score)
            return best_score

    def find_best_move(self) -> Optional[Tuple[int, int]]:
        best_move = None
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if self.board.board[i][j] == " ":
                    self.board.board[i][j] = "O"
                    score = self.minimax(0, False)
                    self.board.board[i][j] = " "
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        return best_move
