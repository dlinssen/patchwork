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
