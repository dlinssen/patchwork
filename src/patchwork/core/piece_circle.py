from dataclasses import dataclass

from .pieces import Piece

@dataclass
class PieceCircle:
    pieces: list[Piece]
    marker_index: int = 0

    def next_three(self) -> list[Piece]:
        return [
            self.pieces[(self.marker_index + i) % len(self.pieces)]
            for i in range(1, min(4, len(self.pieces) + 1))
        ]