"""Stateless intervention policy — Phase 1 revision selection rules."""

from __future__ import annotations

from app.domain.adaptive_learning.intervention_type import (
    PHASE1_IMPLEMENTED_TYPES,
    InterventionType,
    is_phase1_implemented,
)


class InterventionPolicy:
    """Rules for selecting educational interventions.

    Phase 1: REVISION only. Other types remain domain vocabulary.
    """

    MAX_REVISION_INTERVENTIONS = 3
    MAX_CANDIDATES_EVALUATED = 20
    DEFAULT_INTERVENTION_TYPE = InterventionType.REVISION

    @staticmethod
    def phase1_types() -> frozenset[InterventionType]:
        """Return intervention types implemented in Phase 1."""
        return PHASE1_IMPLEMENTED_TYPES

    @staticmethod
    def is_supported(intervention_type: InterventionType | str) -> bool:
        """True when the type is implemented in the current phase."""
        return is_phase1_implemented(intervention_type)

    @staticmethod
    def assert_supported(intervention_type: InterventionType | str) -> None:
        """Raise ValueError when the type is not Phase-1 implemented."""
        if not is_phase1_implemented(intervention_type):
            token = (
                intervention_type.value
                if isinstance(intervention_type, InterventionType)
                else str(intervention_type)
            )
            raise ValueError(
                f"intervention type not implemented in Phase 1: {token!r}"
            )

    @staticmethod
    def max_interventions() -> int:
        """Maximum revision interventions in one plan."""
        return InterventionPolicy.MAX_REVISION_INTERVENTIONS

    @staticmethod
    def should_recommend_revision(
        *,
        candidate_count: int,
        top_priority: float,
        min_priority: float,
    ) -> bool:
        """True when at least one candidate clears the revision threshold."""
        return candidate_count > 0 and top_priority >= min_priority
