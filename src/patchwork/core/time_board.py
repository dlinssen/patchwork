from dataclasses import dataclass


@dataclass(frozen=True)
class TimeTrackEvents:
    """Events crossed by a single move along the time track."""

    income_positions: tuple[int, ...] = ()
    special_patch_positions: tuple[int, ...] = ()

    @property
    def has_income(self) -> bool:
        """Return whether this move crossed at least one income marker."""

        return bool(self.income_positions)

    @property
    def has_special_patch(self) -> bool:
        """Return whether this move crossed at least one 1x1 patch marker."""

        return bool(self.special_patch_positions)


@dataclass
class TimeBoard:
    """The central time track and its one-time/recurring event positions."""

    max_time: int = 53
    income_positions: frozenset[int] = frozenset(5,11,17,23,29,35,41,47,53)
    special_patch_positions: frozenset[int] = frozenset(26,32,38,44,50)

    def crossed_positions(self, start: int, end: int) -> tuple[int, ...]:
        """Return positions crossed when moving from start to end."""

        if start < 0:
            raise ValueError("start time cannot be negative")
        if end < start:
            raise ValueError("end time cannot be before start time")

        # The starting space is not crossed; the destination space is.
        capped_end = min(end, self.max_time)
        return tuple(range(start + 1, capped_end + 1))

    def events_between(self, start: int, end: int) -> TimeTrackEvents:
        """Return all time-track events crossed by this movement."""

        crossed = set(self.crossed_positions(start, end))
        return TimeTrackEvents(
            # Income markers can be crossed by both players, so they stay put.
            income_positions=tuple(
                sorted(crossed.intersection(self.income_positions))
            ),
            # Special patch markers are claimed later by the first player to cross.
            special_patch_positions=tuple(
                sorted(crossed.intersection(self.special_patch_positions))
            ),
        )

    def claim_special_patch(self, position: int) -> bool:
        """Remove a 1x1 patch marker if it is still available."""

        if position not in self.special_patch_positions:
            return False

        remaining_positions = set(self.special_patch_positions)
        remaining_positions.remove(position)
        self.special_patch_positions = frozenset(remaining_positions)
        return True
