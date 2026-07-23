"""CalendarProvider — supply calendar day metadata for planning."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date


class CalendarProvider(ABC):
    """Outbound port for calendar day metadata.

    Implementations live in infrastructure. Providing calendar context is
    never educational reasoning or schedule composition.
    """

    @abstractmethod
    def list_dates(self, *, start: date, end: date) -> tuple[date, ...]:
        """Return calendar dates in ``[start, end]`` inclusive."""

    @abstractmethod
    def is_working_day(self, day: date) -> bool:
        """Return whether ``day`` is a normal working / study day."""
