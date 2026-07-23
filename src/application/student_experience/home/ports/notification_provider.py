"""NotificationProvider — outbound notifications for the home surface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class HomeNotification:
    """Immutable notification projection for the home surface."""

    notification_id: str
    title: str
    body: str
    created_at: datetime
    is_read: bool = False


class NotificationProvider(ABC):
    """Outbound port for student notifications.

    Implementations live in infrastructure. Never performs educational
    reasoning.
    """

    @abstractmethod
    def list_notifications(
        self, student_id: str, *, limit: int = 5
    ) -> tuple[HomeNotification, ...]:
        """Return recent notifications for ``student_id``."""
