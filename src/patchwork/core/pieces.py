from dataclasses import dataclass

Coord = tuple[int, int]


@dataclass(frozen=True)
class Piece:
    """A patch shape with its cost, time advance, and income value."""

    id: str
    cells: frozenset[Coord]   # Local shape coordinates, e.g. {(0,0), (1,0), (1,1)}.
    button_cost: int
    time_cost: int
    button_income: int = 0


@dataclass(frozen=True)
class Placement:
    """A specific positioned version of a piece on a player's board."""

    piece_id: str
    cells: frozenset[Coord]   # Transformed + positioned cells on board.


def rotate(cells: set[Coord]) -> set[Coord]:
    """Rotate cells 90 degrees clockwise around the local origin."""

    # Grid coordinates are (row, col). The usual 90-degree transform
    # (x, y) -> (y, -x) becomes (row, col) -> (col, -row).
    return {(c, -r) for r, c in cells}


def flip(cells: set[Coord]) -> set[Coord]:
    """Mirror cells horizontally around the local vertical axis."""

    # Keep rows fixed and negate columns to reflect the shape left-to-right.
    return {(r, -c) for r, c in cells}


def normalize(cells: set[Coord]) -> frozenset[Coord]:
    """Move a transformed shape so its top-left cell starts at row/col 0."""

    # Rotation/flip can produce negative coordinates. Subtracting the minima
    # preserves the shape while making it easy to slide across the board.
    min_r = min(r for r, _ in cells)
    min_c = min(c for _, c in cells)
    return frozenset((r - min_r, c - min_c) for r, c in cells)
