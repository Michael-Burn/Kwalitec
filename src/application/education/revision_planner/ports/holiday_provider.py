"""HolidayProvider — supply holiday / non-study dates."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date


class HolidayProvider(ABC):
    """Outbound port for holiday and non-study calendar dates.

    Implementations live in infrastructure. Holiday lookup is never
    educational reasoning or schedule composition.
    """

    @abstractmethod
    def holidays_between(self, *, start: date, end: date) -> tuple[date, ...]:
        """Return holiday dates within ``[start, end]`` inclusive."""

    @abstractmethod
    def is_holiday(self, day: date) -> bool:
        """Return whether ``day`` is a holiday / non-study day."""
