"""Clock — caller-supplied time source for Mission Execution.

Implementations live in infrastructure. The engine itself never calls
``datetime.now()``; command methods accept explicit ``at`` timestamps.
This port exists so adapters can inject a clock without leaking wall-clock
reads into application logic.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime


class Clock(ABC):
    """Outbound port for obtaining the current instant.

    Application code in this package must not call ``datetime.now``.
    Callers of ``MissionExecutionEngine`` supply ``at`` explicitly; a Clock
    implementation may be used by adapters to produce that value.
    """

    @abstractmethod
    def now(self) -> datetime:
        """Return the current instant according to this clock."""
