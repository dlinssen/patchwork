from copy import deepcopy
from dataclasses import dataclass

from .state import GameState
from .time_board import TimeTrackEvents
from .actions import Action


@dataclass(frozen=True)
class TimeAdvanceResult:
    player_index: int
    start_time: int
    end_time: int
    events: TimeTrackEvents


class GameEngine:
    def active_player_index(self, state: GameState) -> int:
        return min(
            range(len(state.players)),
            key=lambda player_index: state.players[player_index].time,
        )

    def is_game_over(self, state: GameState) -> bool:
        return all(
            player.time >= state.time_board.max_time
            for player in state.players
        )

    def advance_player_time(
        self,
        state: GameState,
        player_index: int,
        steps: int,
    ) -> tuple[GameState, TimeAdvanceResult]:
        if steps < 0:
            raise ValueError("steps cannot be negative")

        next_state = deepcopy(state)
        player = next_state.players[player_index]
        start_time = player.time
        end_time = min(start_time + steps, next_state.time_board.max_time)
        events = next_state.time_board.events_between(start_time, end_time)

        player.time = end_time
        player.buttons += player.button_income * len(events.income_positions)

        for patch_position in events.special_patch_positions:
            next_state.time_board.claim_special_patch(patch_position)

        return next_state, TimeAdvanceResult(
            player_index=player_index,
            start_time=start_time,
            end_time=end_time,
            events=events,
        )
    
    def apply_action(
        self,
        state: GameState,
        action: Action,
    ) -> GameState:
        # WIP
        raise NotImplementedError(f"Cannot apply action yet: {action!r}")
