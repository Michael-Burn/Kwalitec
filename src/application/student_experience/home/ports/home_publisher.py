"""HomePublisher — publish composed home artefacts outbound."""

from __future__ import annotations

from abc import ABC, abstractmethod

from application.student_experience.home.models.home_snapshot import HomeSnapshot
from application.student_experience.home.models.home_view_model import HomeViewModel


class HomePublisher(ABC):
    """Outbound port for publishing composed home views.

    Implementations live in infrastructure. Publishing is notification /
    persistence wiring — never educational reasoning.
    """

    @abstractmethod
    def publish_home(self, home: HomeViewModel) -> None:
        """Publish a composed ``HomeViewModel``."""

    @abstractmethod
    def publish_snapshot(self, snapshot: HomeSnapshot) -> None:
        """Publish a composed ``HomeSnapshot``."""
