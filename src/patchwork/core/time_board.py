from dataclasses import dataclass


@dataclass(frozen=True)
class TimeTrackEvents:
    income_positions: tuple[int, ...] = ()
    special_patch_positions: tuple[int, ...] = ()

    @property
    def has_income(self) -> bool:
        return bool(self.income_positions)

    @property
    def has_special_patch(self) -> bool:
        return bool(self.special_patch_positions)


@dataclass
class TimeBoard:
    max_time: int = 53
    income_positions: frozenset[int] = frozenset()
    special_patch_positions: frozenset[int] = frozenset()

    def crossed_positions(self, start: int, end: int) -> tuple[int, ...]:
        if start < 0:
            raise ValueError("start time cannot be negative")
        if end < start:
            raise ValueError("end time cannot be before start time")

        capped_end = min(end, self.max_time)
        return tuple(range(start + 1, capped_end + 1))

    def events_between(self, start: int, end: int) -> TimeTrackEvents:
        crossed = set(self.crossed_positions(start, end))
        return TimeTrackEvents(
            income_positions=tuple(
                sorted(crossed.intersection(self.income_positions))
            ),
            special_patch_positions=tuple(
                sorted(crossed.intersection(self.special_patch_positions))
            ),
        )

    def claim_special_patch(self, position: int) -> bool:
        if position not in self.special_patch_positions:
            return False

        remaining_positions = set(self.special_patch_positions)
        remaining_positions.remove(position)
        self.special_patch_positions = frozenset(remaining_positions)
        return True
