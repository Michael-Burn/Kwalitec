"""Outbound port for publishing application events."""

from __future__ import annotations

from abc import ABC, abstractmethod

from application.events.base import ApplicationEvent


class ApplicationEventPublisher(ABC):
    """Publishes application coordination events (not domain events)."""

    @abstractmethod
    def publish(self, event: ApplicationEvent) -> None:
        """Publish a single application event."""
