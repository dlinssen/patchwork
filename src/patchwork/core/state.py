from dataclasses import dataclass, field

from .player import PlayerState
from .piece_circle import PieceCircle
from .time_board import TimeBoard

@dataclass
class GameState:
    players: list[PlayerState]
    piece_circle: PieceCircle
    time_board: TimeBoard = field(default_factory=TimeBoard)
