"""Revision projection — today's highest-value revision options.

Consumes Adaptive Decision outputs only (via application ports).
Never calculates revision priority or educational ROI.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.student_experience.recommendation_explanation import (
    RecommendationExplanation,
)


@dataclass(frozen=True)
class RevisionOption:
    """One student-facing revision candidate."""

    option_id: str
    topic_title: str
    priority_label: str = ""
    estimated_study_minutes: int | None = None
    expected_benefit: str = ""
    explanation: RecommendationExplanation | None = None
    is_primary: bool = False

    @classmethod
    def create(
        cls,
        option_id: str,
        topic_title: str,
        *,
        priority_label: str = "",
        estimated_study_minutes: int | None = None,
        expected_benefit: str = "",
        explanation: RecommendationExplanation | None = None,
        is_primary: bool = False,
    ) -> RevisionOption:
        """Build a revision option."""
        minutes = estimated_study_minutes
        if minutes is not None and minutes < 0:
            raise ValueError("estimated_study_minutes must be non-negative")
        return cls(
            option_id=_require_non_empty(option_id, "option_id"),
            topic_title=_require_non_empty(topic_title, "topic_title"),
            priority_label=(priority_label or "").strip(),
            estimated_study_minutes=minutes,
            expected_benefit=(expected_benefit or "").strip(),
            explanation=explanation,
            is_primary=bool(is_primary),
        )


@dataclass(frozen=True)
class RevisionProjection:
    """Domain projection for the Revision experience."""

    student_id: str
    primary: RevisionOption | None = None
    alternatives: tuple[RevisionOption, ...] = field(default_factory=tuple)
    empty_message: str = ""

    @classmethod
    def create(
        cls,
        student_id: str,
        *,
        primary: RevisionOption | None = None,
        alternatives: list[RevisionOption] | tuple[RevisionOption, ...] | None = None,
        empty_message: str = "",
    ) -> RevisionProjection:
        """Build a revision projection."""
        alts = tuple(alternatives or ())
        if primary is None and not alts:
            msg = (empty_message or "").strip() or (
                "No revision is recommended right now. Keep going with "
                "today's session."
            )
        else:
            msg = (empty_message or "").strip()
        return cls(
            student_id=_require_non_empty(student_id, "student_id"),
            primary=primary,
            alternatives=alts,
            empty_message=msg,
        )

    @property
    def has_revision(self) -> bool:
        return self.primary is not None

    @property
    def option_count(self) -> int:
        return (1 if self.primary else 0) + len(self.alternatives)


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
