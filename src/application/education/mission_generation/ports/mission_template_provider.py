"""MissionTemplateProvider — supply structural mission templates."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping

from application.education.mission_generation.enums import MissionType


class MissionTemplateProvider(ABC):
    """Inbound port for optional mission template catalogues.

    Templates are structural hints (step skeletons, default durations).
    Implementations live in infrastructure. This port never estimates
    mastery or generates recommendations.
    """

    @abstractmethod
    def template_for(self, mission_type: MissionType) -> Mapping[str, object] | None:
        """Return an optional structural template for ``mission_type``."""

    @abstractmethod
    def available_types(self) -> tuple[MissionType, ...]:
        """Return mission types that have templates available."""
