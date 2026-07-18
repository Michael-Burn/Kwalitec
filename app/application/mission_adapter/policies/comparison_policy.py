"""Stateless structural comparison rules for dual-engine validation.

Never compares generated educational content.
"""

from __future__ import annotations

from app.application.mission_adapter.dto.comparison_result import DimensionMatch
from app.application.mission_adapter.dto.mission_snapshot import MissionSnapshot


class ComparisonPolicy:
    """Deterministic structural comparison dimensions (stateless)."""

    DIMENSIONS: tuple[str, ...] = (
        "journey_selected",
        "topic_selected",
        "session_selected",
        "estimated_effort",
        "mission_type",
        "revision_recommendation",
        "ordering",
        "explanation_metadata",
    )

    # Fields that must never be compared (educational content).
    FORBIDDEN_FIELDS: frozenset[str] = frozenset(
        {
            "title",
            "body",
            "content",
            "explanation_text",
            "study_content",
            "generated_text",
        }
    )

    @staticmethod
    def extract_values(snapshot: MissionSnapshot) -> dict[str, str]:
        """Extract comparable structural values from a snapshot."""
        return {
            "journey_selected": snapshot.journey_id,
            "topic_selected": snapshot.topic_id,
            "session_selected": snapshot.session_id,
            "estimated_effort": snapshot.effort,
            "mission_type": snapshot.mission_type,
            "revision_recommendation": str(snapshot.is_revision).lower(),
            "ordering": str(snapshot.sequence_index),
            "explanation_metadata": ",".join(sorted(snapshot.explanation_keys)),
        }

    @staticmethod
    def compare_dimensions(
        v1: MissionSnapshot,
        v2: MissionSnapshot,
    ) -> tuple[DimensionMatch, ...]:
        """Compare all structural dimensions between two snapshots."""
        left = ComparisonPolicy.extract_values(v1)
        right = ComparisonPolicy.extract_values(v2)
        matches: list[DimensionMatch] = []
        for name in ComparisonPolicy.DIMENSIONS:
            lv = left[name]
            rv = right[name]
            matches.append(
                DimensionMatch(
                    name=name,
                    matched=lv == rv,
                    v1_value=lv,
                    v2_value=rv,
                )
            )
        return tuple(matches)

    @staticmethod
    def all_matched(dimensions: tuple[DimensionMatch, ...]) -> bool:
        """True when every dimension matched."""
        return all(d.matched for d in dimensions)

    @staticmethod
    def divergence_count(dimensions: tuple[DimensionMatch, ...]) -> int:
        """Count of mismatched dimensions."""
        return sum(1 for d in dimensions if not d.matched)

    @staticmethod
    def is_forbidden_field(name: str) -> bool:
        """True when ``name`` is educational content and must not be compared."""
        return name.lower() in ComparisonPolicy.FORBIDDEN_FIELDS
