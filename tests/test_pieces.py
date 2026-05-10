from patchwork.core.pieces import flip, normalize, rotate


def test_rotate_turns_cells_90_degrees_clockwise_around_origin() -> None:
    cells = {(0, 0), (1, 0), (2, 0), (2, 1)}

    assert rotate(cells) == {(0, 0), (0, -1), (0, -2), (1, -2)}


def test_flip_reflects_cells_horizontally_around_origin() -> None:
    cells = {(0, 0), (1, 0), (1, 1), (2, 1)}

    assert flip(cells) == {(0, 0), (1, 0), (1, -1), (2, -1)}


def test_normalize_moves_shape_to_top_left_origin() -> None:
    cells = {(0, 0), (0, -1), (0, -2), (1, -2)}

    assert normalize(cells) == frozenset({(0, 2), (0, 1), (0, 0), (1, 0)})


def test_rotate_then_normalize_produces_usable_board_coordinates() -> None:
    cells = {(0, 0), (1, 0), (2, 0), (2, 1)}

    assert normalize(rotate(cells)) == frozenset({(0, 2), (0, 1), (0, 0), (1, 0)})


def test_flip_then_normalize_produces_mirrored_shape() -> None:
    cells = {(0, 0), (1, 0), (1, 1), (2, 1)}

    assert normalize(flip(cells)) == frozenset({(0, 1), (1, 1), (1, 0), (2, 0)})
