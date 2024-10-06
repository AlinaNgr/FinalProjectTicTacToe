from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Tuple

app = FastAPI()


class Board:
    def __init__(self):
        self.board = [[" "for _ in range(3)] for _ in range(3)]

    def display(self) -> List[List[str]]:
        return self.board

    def is_full(self) -> bool:
        return all(cell != " " for row in self.board for cell in row)