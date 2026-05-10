import pytest

from patchwork.core.board import Board
from patchwork.core.pieces import Placement


def test_fresh_board_can_place_inside_empty_cells() -> None:
    board = Board(size=3)
    placement = Placement(
        piece_id="corner",
        cells=frozenset({(0, 0), (0, 1), (1, 0)}),
    )

    assert board.can_place(placement)


def test_place_marks_cells_as_occupied() -> None:
    board = Board(size=3)
    placement = Placement(
        piece_id="domino",
        cells=frozenset({(1, 1), (1, 2)}),
    )

    board.place(placement)

    assert board.occupied == {(1, 1), (1, 2)}
    assert board.count_empty_cells() == 7


def test_cannot_place_over_existing_cells() -> None:
    board = Board(size=3)
    first = Placement(piece_id="single", cells=frozenset({(1, 1)}))
    overlapping = Placement(
        piece_id="domino",
        cells=frozenset({(1, 1), (1, 2)}),
    )

    board.place(first)

    assert not board.can_place(overlapping)
    with pytest.raises(ValueError, match="Invalid placement"):
        board.place(overlapping)


def test_cannot_place_outside_board() -> None:
    board = Board(size=3)
    placement = Placement(
        piece_id="too_wide",
        cells=frozenset({(0, 2), (0, 3)}),
    )

    assert not board.can_place(placement)
    with pytest.raises(ValueError, match="Invalid placement"):
        board.place(placement)
