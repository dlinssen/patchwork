from dataclasses import dataclass

from .pieces import Placement

@dataclass(frozen=True)
class BuyPieceAction:
    piece_id: str
    placement: Placement

@dataclass(frozen=True)
class PassAction:
    # this moves your time one ahead of the other player
    pass