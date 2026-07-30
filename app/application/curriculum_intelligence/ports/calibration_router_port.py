"""CalibrationRouter port — maps Founder style settings to regen subset.

No UI and no generation reruns in Phase A — interface + default mapping only.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.curriculum_intelligence.generation import (
    CalibrationProfile,
    DifficultyBiasStyle,
    GenerationIndex,
    GranularityStyle,
    HierarchyStyle,
    TopicDensityStyle,
)


class CalibrationRouter(ABC):
    """Select which generation indices must regenerate for a profile change."""

    @abstractmethod
    def select_generations(
        self,
        profile: CalibrationProfile,
        *,
        previous: CalibrationProfile | None = None,
    ) -> tuple[int, ...]:
        """Return ordered generation indices to regenerate (inclusive cascade)."""


class DefaultCalibrationRouter(CalibrationRouter):
    """Canonical mapping from EI-001 §8.3 (no execution in Phase A)."""

    def select_generations(
        self,
        profile: CalibrationProfile,
        *,
        previous: CalibrationProfile | None = None,
    ) -> tuple[int, ...]:
        # First save: compare against balanced defaults. Identical defaults
        # seed the profile only (no regen). Non-default styles still cascade
        # from the earliest changed dimension through Gen 7.
        baseline = previous or default_calibration_profile(
            profile_id="__defaults__",
            workspace_id=profile.workspace_id,
            created_at_iso=profile.created_at_iso,
        )

        start: int | None = None
        if profile.hierarchy != baseline.hierarchy:
            start = int(GenerationIndex.HIERARCHY)
        if (
            profile.granularity != baseline.granularity
            or profile.topic_density != baseline.topic_density
        ):
            candidate = int(GenerationIndex.CONCEPT_FORMATION)
            start = candidate if start is None else min(start, candidate)
        if profile.difficulty_bias != baseline.difficulty_bias:
            candidate = int(GenerationIndex.OBJECTIVE_INTELLIGENCE)
            start = candidate if start is None else min(start, candidate)

        if start is None:
            return ()
        return tuple(range(start, int(GenerationIndex.CERTIFICATION) + 1))


def default_calibration_profile(
    *,
    profile_id: str,
    workspace_id: str,
    created_at_iso: str,
) -> CalibrationProfile:
    """Balanced defaults for Founder calibration."""
    return CalibrationProfile(
        profile_id=profile_id,
        workspace_id=workspace_id,
        granularity=GranularityStyle.BALANCED,
        hierarchy=HierarchyStyle.BALANCED,
        topic_density=TopicDensityStyle.BALANCED,
        difficulty_bias=DifficultyBiasStyle.BALANCED,
        created_at_iso=created_at_iso,
    )
