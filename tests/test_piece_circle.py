from patchwork.core.piece_circle import PieceCircle
from patchwork.core.pieces import Piece


def make_piece(piece_id: str) -> Piece:
    return Piece(
        id=piece_id,
        cells=frozenset({(0, 0)}),
        button_cost=1,
        time_cost=1,
    )


def test_next_three_returns_pieces_after_marker() -> None:
    circle = PieceCircle(
        pieces=[make_piece("a"), make_piece("b"), make_piece("c"), make_piece("d")],
        marker_index=0,
    )

    assert [piece.id for piece in circle.next_three()] == ["b", "c", "d"]


def test_next_three_wraps_around_circle() -> None:
    circle = PieceCircle(
        pieces=[make_piece("a"), make_piece("b"), make_piece("c"), make_piece("d")],
        marker_index=2,
    )

    assert [piece.id for piece in circle.next_three()] == ["d", "a", "b"]


def test_next_three_returns_remaining_pieces_when_fewer_than_three_exist() -> None:
    circle = PieceCircle(
        pieces=[make_piece("a"), make_piece("b")],
        marker_index=0,
    )

    assert [piece.id for piece in circle.next_three()] == ["b", "a"]
