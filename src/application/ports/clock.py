"""Clock port — injectable time source for application timestamps."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime


class Clock(ABC):
    """Provides the current time for application coordination.

    Infrastructure supplies wall-clock or deterministic test clocks.
    Application services must not call ``datetime.now`` directly.
    """

    @abstractmethod
    def now(self) -> datetime:
        """Return a timezone-aware UTC timestamp."""
