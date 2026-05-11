from dataclasses import dataclass

from .pieces import Placement


class Action:
    """Marker base class for all player actions."""

    pass


@dataclass(frozen=True)
class BuyPieceAction(Action):
    """Buy a piece from the circle and place it on the active player's board."""

    piece_id: str
    placement: Placement


@dataclass(frozen=True)
class PassAction(Action):
    """Pass instead of buying a patch."""

    # In the full rules, passing moves this player ahead of the opponent
    # and awards buttons for the spaces crossed.
    pass
