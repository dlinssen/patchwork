from dataclasses import dataclass

from .board import Board


@dataclass
class PlayerState:
    """Mutable state for one player during a game."""

    board: Board
    buttons: int = 5
    time: int = 0
    button_income: int = 0
