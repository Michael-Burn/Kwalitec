"""Framework-free curriculum context for Readiness Aggregation.

Built outside the aggregator (via CurriculumService helpers in future
orchestration). Aggregation never loads ORM curricula or invents syllabus trees.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class CurriculumFormat(StrEnum):
    """Curriculum format tag for V1/V2-aware attribution."""

    V1 = "v1"
    V2 = "v2"


@dataclass(frozen=True)
class CurriculumTopicRef:
    """One syllabus topic identity with optional weight and section.

    Attributes:
        topic_id: Canonical curriculum topic identity.
        weight: Official exam weight when known (attribution emphasis only).
        section_id: V2 section identity when applicable; None for flat V1.
    """

    topic_id: str
    weight: float | None = None
    section_id: str | None = None

    @classmethod
    def create(
        cls,
        topic_id: str,
        *,
        weight: float | None = None,
        section_id: str | None = None,
    ) -> CurriculumTopicRef:
        """Construct a CurriculumTopicRef.

        Args:
            topic_id: Non-empty canonical topic identity.
            weight: Optional official weight.
            section_id: Optional V2 section identity.

        Returns:
            A frozen CurriculumTopicRef.

        Raises:
            ValueError: If ``topic_id`` is empty or blank.
        """
        normalized = topic_id.strip() if isinstance(topic_id, str) else ""
        if not normalized:
            raise ValueError("topic_id must be a non-empty string")
        return cls(topic_id=normalized, weight=weight, section_id=section_id)


@dataclass(frozen=True)
class CurriculumContext:
    """Syllabus denominator and weight context for one readiness derivation.

    Attributes:
        curriculum_id: Canonical curriculum identity matching Twin Identity.
        format: ``v1`` (flat) or ``v2`` (sectioned).
        topics: Ordered topic refs (display / traversal order).
        section_ids: Ordered section identities when format is V2; empty for V1.
    """

    curriculum_id: str
    format: CurriculumFormat
    topics: tuple[CurriculumTopicRef, ...] = ()
    section_ids: tuple[str, ...] = ()

    @classmethod
    def create(
        cls,
        curriculum_id: str,
        *,
        format: CurriculumFormat | str = CurriculumFormat.V1,
        topics: list[CurriculumTopicRef] | tuple[CurriculumTopicRef, ...] | None = None,
        section_ids: list[str] | tuple[str, ...] | None = None,
    ) -> CurriculumContext:
        """Construct a CurriculumContext.

        Args:
            curriculum_id: Non-empty curriculum identity.
            format: Curriculum format tag (``v1`` / ``v2``).
            topics: Optional ordered topic refs.
            section_ids: Optional ordered section ids (V2).

        Returns:
            A frozen CurriculumContext.

        Raises:
            ValueError: If ``curriculum_id`` is empty or format is invalid.
        """
        normalized = curriculum_id.strip() if isinstance(curriculum_id, str) else ""
        if not normalized:
            raise ValueError("curriculum_id must be a non-empty string")
        fmt = (
            format
            if isinstance(format, CurriculumFormat)
            else CurriculumFormat(str(format).strip().lower())
        )
        return cls(
            curriculum_id=normalized,
            format=fmt,
            topics=tuple(topics or ()),
            section_ids=tuple(section_ids or ()),
        )

    @property
    def topic_ids(self) -> tuple[str, ...]:
        """Ordered topic identities (canonical denominator ids)."""
        return tuple(ref.topic_id for ref in self.topics)

    def weight_for(self, topic_id: str) -> float | None:
        """Return official weight for ``topic_id`` when present."""
        for ref in self.topics:
            if ref.topic_id == topic_id:
                return ref.weight
        return None

    def high_weight_topic_ids(self, *, threshold: float = 0.0) -> frozenset[str]:
        """Topic ids whose weight is strictly above ``threshold``.

        Used for attribution emphasis only — not a composite scoring formula.
        Topics with ``None`` weight are excluded from the high-weight set.
        """
        return frozenset(
            ref.topic_id
            for ref in self.topics
            if ref.weight is not None and ref.weight > threshold
        )
