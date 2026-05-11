from dataclasses import dataclass, field

from .pieces import Coord, Placement


@dataclass
class Board:
    """A player's 9x9 quilt board and its occupied cells."""

    size: int = 9
    occupied: set[Coord] = field(default_factory=set)

    def can_place(self, placement: Placement) -> bool:
        """Return whether all placement cells fit inside empty board squares."""

        return all(
            0 <= r < self.size and
            0 <= c < self.size and
            (r, c) not in self.occupied
            for r, c in placement.cells
        )

    def place(self, placement: Placement) -> None:
        """Place a patch on the board, or reject it if it does not fit."""

        if not self.can_place(placement):
            raise ValueError("Invalid placement")
        self.occupied.update(placement.cells)

    def count_empty_cells(self) -> int:
        """Count board squares that are still empty."""

        return self.size**2 - len(self.occupied)
