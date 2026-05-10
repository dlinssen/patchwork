import pytest

from patchwork.core.board import Board
from patchwork.core.piece_circle import PieceCircle
from patchwork.core.pieces import Piece
from patchwork.core.player import PlayerState
from patchwork.core.rules import GameEngine
from patchwork.core.state import GameState
from patchwork.core.time_board import TimeBoard


def make_state(
    players: list[PlayerState],
    time_board: TimeBoard | None = None,
) -> GameState:
    return GameState(
        players=players,
        piece_circle=PieceCircle(
            pieces=[
                Piece(
                    id="single",
                    cells=frozenset({(0, 0)}),
                    button_cost=1,
                    time_cost=1,
                )
            ]
        ),
        time_board=time_board or TimeBoard(),
    )


def test_active_player_is_player_with_lowest_time() -> None:
    engine = GameEngine()
    state = make_state(
        players=[
            PlayerState(board=Board(), time=6),
            PlayerState(board=Board(), time=3),
        ]
    )

    assert engine.active_player_index(state) == 1


def test_advance_player_time_returns_new_state_and_leaves_original_unchanged() -> None:
    engine = GameEngine()
    state = make_state(
        players=[
            PlayerState(board=Board(), time=2),
            PlayerState(board=Board(), time=5),
        ],
        time_board=TimeBoard(max_time=10),
    )

    next_state, result = engine.advance_player_time(state, player_index=0, steps=4)

    assert state.players[0].time == 2
    assert next_state.players[0].time == 6
    assert result.start_time == 2
    assert result.end_time == 6


def test_advance_player_time_applies_income_for_crossed_income_positions() -> None:
    engine = GameEngine()
    state = make_state(
        players=[
            PlayerState(board=Board(), buttons=5, time=2, button_income=3),
            PlayerState(board=Board()),
        ],
        time_board=TimeBoard(max_time=20, income_positions=frozenset({5, 11})),
    )

    next_state, result = engine.advance_player_time(state, player_index=0, steps=10)

    assert result.events.income_positions == (5, 11)
    assert next_state.players[0].buttons == 11


def test_advance_player_time_claims_crossed_special_patch_positions() -> None:
    engine = GameEngine()
    state = make_state(
        players=[
            PlayerState(board=Board(), time=2),
            PlayerState(board=Board()),
        ],
        time_board=TimeBoard(
            max_time=20,
            special_patch_positions=frozenset({4, 9}),
        ),
    )

    next_state, result = engine.advance_player_time(state, player_index=0, steps=5)

    assert result.events.special_patch_positions == (4,)
    assert next_state.time_board.special_patch_positions == frozenset({9})


def test_advance_player_time_rejects_negative_steps() -> None:
    engine = GameEngine()
    state = make_state(players=[PlayerState(board=Board())])

    with pytest.raises(ValueError, match="negative"):
        engine.advance_player_time(state, player_index=0, steps=-1)


def test_game_is_over_once_all_players_reach_end_of_time_board() -> None:
    engine = GameEngine()
    state = make_state(
        players=[
            PlayerState(board=Board(), time=10),
            PlayerState(board=Board(), time=10),
        ],
        time_board=TimeBoard(max_time=10),
    )

    assert engine.is_game_over(state)
