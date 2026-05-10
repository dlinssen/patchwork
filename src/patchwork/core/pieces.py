from dataclasses import dataclass

Coord = tuple[int, int]

@dataclass(frozen=True)
class Piece:
    id: str
    cells: frozenset[Coord]   # shape coordinates, e.g. {(0,0), (1,0), (1,1)}
    button_cost: int
    time_cost: int
    button_income: int = 0

@dataclass(frozen=True)
class Placement:
    piece_id: str
    cells: frozenset[Coord]   # transformed + positioned cells on board

def rotate(cells: set[Coord]) -> set[Coord]:
    # 90 degree rotation
    return {(c, -r) for r, c in cells}

def flip(cells: set[Coord]) -> set[Coord]:
    # flip over the y-axis
    return {(r, -c) for r, c in cells}

def normalize(cells: set[Coord]) -> frozenset[Coord]:
    # find the minimum (negative) row and col and subtract it
    min_r = min(r for r, _ in cells)
    min_c = min(c for _, c in cells)
    return frozenset((r - min_r, c - min_c) for r, c in cells)
