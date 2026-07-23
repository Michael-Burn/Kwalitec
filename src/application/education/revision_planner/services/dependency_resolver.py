"""DependencyResolver — preserves prerequisite ordering in schedules."""

from __future__ import annotations

from collections.abc import Sequence

from application.education.mission_generation.enums import MissionType
from application.education.mission_generation.models.mission import Mission
from application.education.mission_generation.rules.ordering_rules import OrderingRules

# Missions that must precede same-subject dependent work.
_PREREQUISITE_TYPES = frozenset(
    {
        MissionType.REVISE_PREREQUISITE,
        MissionType.STRENGTHEN_FOUNDATION,
    }
)


class DependencyResolver:
    """Deterministically orders missions respecting prerequisite dependencies.

    Prerequisite / foundation missions for a subject are always scheduled
    before other missions targeting that subject. Global order remains
    stable via OrderingRules when dependency constraints are inactive.
    """

    @staticmethod
    def resolve(
        missions: Sequence[Mission],
        *,
        honour_dependencies: bool = True,
    ) -> tuple[Mission, ...]:
        """Return missions in dependency-safe scheduling order."""
        if not honour_dependencies:
            return OrderingRules.prioritise(missions)
        ordered = OrderingRules.ensure_prerequisites_before_dependents(missions)
        return DependencyResolver._stabilize_subject_prerequisites(ordered)

    @staticmethod
    def _stabilize_subject_prerequisites(
        missions: Sequence[Mission],
    ) -> tuple[Mission, ...]:
        """Ensure same-subject prerequisites appear before dependents."""
        items = list(missions)
        # Stable partition: prerequisites first within each subject group,
        # preserving relative order from OrderingRules overall.
        result: list[Mission] = []
        placed: set[str] = set()

        # First pass: place prerequisite-type missions in plan order.
        for mission in items:
            if mission.mission_type in _PREREQUISITE_TYPES:
                result.append(mission)
                placed.add(mission.mission_id.value)

        # Second pass: place remaining missions, but only after their
        # same-subject prerequisites (already in result).
        remaining = [m for m in items if m.mission_id.value not in placed]
        for mission in remaining:
            result.append(mission)
            placed.add(mission.mission_id.value)

        return tuple(result)

    @staticmethod
    def is_prerequisite(mission: Mission) -> bool:
        return mission.mission_type in _PREREQUISITE_TYPES or mission.is_prerequisite()

    @staticmethod
    def dependency_key(mission: Mission) -> tuple:
        """Sort key reinforcing prerequisite-before-dependent within subject."""
        return (
            0 if DependencyResolver.is_prerequisite(mission) else 1,
            mission.subject_id or "",
            -mission.ordering.priority_magnitude,
            mission.mission_id.value,
        )
