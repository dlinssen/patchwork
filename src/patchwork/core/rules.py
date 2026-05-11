from copy import deepcopy
from dataclasses import dataclass

from .state import GameState
from .time_board import TimeTrackEvents
from .actions import Action


@dataclass(frozen=True)
class TimeAdvanceResult:
    """Details produced by advancing one player on the time track."""

    player_index: int
    start_time: int
    end_time: int
    events: TimeTrackEvents


class GameEngine:
    """Pure rules layer for deriving turns and applying state transitions."""

    def active_player_index(self, state: GameState) -> int:
        """Return the player who is furthest behind on the time track."""

        return min(
            range(len(state.players)),
            key=lambda player_index: state.players[player_index].time,
        )

    def is_game_over(self, state: GameState) -> bool:
        """Return whether all players have reached the end of the time board."""

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
        """Return a new state after moving one player's time marker."""

        if steps < 0:
            raise ValueError("steps cannot be negative")

        # Keep transitions non-destructive so tests and future ML search can
        # evaluate moves without mutating the state they started from.
        next_state = deepcopy(state)
        player = next_state.players[player_index]
        start_time = player.time
        end_time = min(start_time + steps, next_state.time_board.max_time)
        events = next_state.time_board.events_between(start_time, end_time)

        player.time = end_time
        player.buttons += player.button_income * len(events.income_positions)

        # Income markers remain for later crossings; special patches are claimed
        # by the first player to cross their positions.
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
        """Apply a player action and return the resulting game state."""

        raise NotImplementedError(f"Cannot apply action yet: {action!r}")
