from dataclasses import dataclass

from .board import Board

@dataclass
class PlayerState:
    board: Board
    buttons: int = 5
    time: int = 0