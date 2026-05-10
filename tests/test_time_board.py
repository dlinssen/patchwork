import pytest

from patchwork.core.time_board import TimeBoard


def test_crossed_positions_excludes_start_and_includes_end() -> None:
    board = TimeBoard(max_time=10)

    assert board.crossed_positions(start=4, end=7) == (5, 6, 7)


def test_crossed_positions_caps_at_max_time() -> None:
    board = TimeBoard(max_time=10)

    assert board.crossed_positions(start=8, end=12) == (9, 10)


def test_events_between_reports_income_and_special_patches_crossed() -> None:
    board = TimeBoard(
        max_time=20,
        income_positions=frozenset({5, 11, 17}),
        special_patch_positions=frozenset({8, 14}),
    )

    events = board.events_between(start=4, end=12)

    assert events.income_positions == (5, 11)
    assert events.special_patch_positions == (8,)
    assert events.has_income
    assert events.has_special_patch


def test_claim_special_patch_only_succeeds_once() -> None:
    board = TimeBoard(
        max_time=20,
        special_patch_positions=frozenset({8}),
    )

    assert board.claim_special_patch(8)
    assert not board.claim_special_patch(8)
    assert board.special_patch_positions == frozenset()


def test_crossed_positions_rejects_backwards_movement() -> None:
    board = TimeBoard(max_time=10)

    with pytest.raises(ValueError, match="before start"):
        board.crossed_positions(start=7, end=4)
