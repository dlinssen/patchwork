from dataclasses import dataclass

from .pieces import Piece


@dataclass
class PieceCircle:
    """Circular ordering of unbought patches and the neutral marker."""

    pieces: list[Piece]
    marker_index: int = 0

    def next_three(self) -> list[Piece]:
        """Return the three buyable pieces after the marker, wrapping around."""

        return [
            # Modulo indexing turns the flat list into a circle.
            self.pieces[(self.marker_index + i) % len(self.pieces)]
            for i in range(1, min(4, len(self.pieces) + 1))
        ]
