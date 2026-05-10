from dataclasses import dataclass

from .pieces import Placement


class Action:
    """Marker base class for all player actions."""

    pass


@dataclass(frozen=True)
class BuyPieceAction(Action):
    piece_id: str
    placement: Placement


@dataclass(frozen=True)
class PassAction(Action):
    # this moves your time one ahead of the other player
    pass
