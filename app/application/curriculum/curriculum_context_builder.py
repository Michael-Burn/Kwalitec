"""CurriculumContextBuilder — Application Integration for syllabus context.

Loads official curriculum via ``CurriculumService``, traverses with canonical
helpers only, and emits an immutable domain ``CurriculumContext``.

Owns construction and validation. Never scores readiness, selects next
actions, packages recommendations, composes missions, or mutates Twin /
curriculum rows. Does not import Flask request/session globals.
"""

from __future__ import annotations

from app.domain.readiness.curriculum_context import (
    CurriculumContext,
    CurriculumFormat,
    CurriculumTopicRef,
)
from app.models.curriculum import Curriculum, Section, Topic
from app.services.curriculum_service import CurriculumService


class CurriculumContextBuildError(Exception):
    """Base class for CurriculumContextBuilder fail-closed outcomes."""


class MissingCurriculumError(CurriculumContextBuildError):
    """Target curriculum cannot be resolved or loaded."""


class InvalidCurriculumError(CurriculumContextBuildError):
    """Loaded curriculum is unlawful for domain CurriculumContext emission."""


class UnsupportedCurriculumVersionError(CurriculumContextBuildError):
    """Curriculum format is not a supported V1/V2 contract."""


class CurriculumContextBuilder:
    """Construct immutable CurriculumContext from Curriculum authority.

    Entry for Educational Orchestration (and only production Integration path)
    to obtain syllabus denominator context. Format detection follows the same
    section-presence branch as ``CurriculumService.get_all_topics_ordered``.
    """

    @staticmethod
    def build(curriculum_id: int | None) -> CurriculumContext:
        """Load a curriculum by identity and emit CurriculumContext.

        Args:
            curriculum_id: Persisted curriculum primary key.

        Returns:
            Frozen domain CurriculumContext for one composition pass.

        Raises:
            MissingCurriculumError: Identity missing or curriculum not found.
            InvalidCurriculumError: Curriculum cannot form a lawful denominator.
            UnsupportedCurriculumVersionError: Format is not supported V1/V2.
        """
        if curriculum_id is None:
            raise MissingCurriculumError("curriculum_id is required")
        if not isinstance(curriculum_id, int) or curriculum_id <= 0:
            raise MissingCurriculumError(
                f"curriculum_id must be a positive integer, got {curriculum_id!r}"
            )

        curriculum = CurriculumService.get_curriculum_by_id(curriculum_id)
        if curriculum is None:
            raise MissingCurriculumError(
                f"curriculum not found for id={curriculum_id}"
            )
        return CurriculumContextBuilder.build_from_curriculum(curriculum)

    @staticmethod
    def build_from_curriculum(curriculum: Curriculum) -> CurriculumContext:
        """Traverse a loaded curriculum and emit CurriculumContext.

        Args:
            curriculum: ORM curriculum row already loaded via Curriculum paths.

        Returns:
            Frozen domain CurriculumContext for one composition pass.

        Raises:
            MissingCurriculumError: Curriculum argument is absent / identity blank.
            InvalidCurriculumError: Traversal cannot produce a lawful denominator.
            UnsupportedCurriculumVersionError: Format is not supported V1/V2.
        """
        if curriculum is None:
            raise MissingCurriculumError("curriculum is required")

        curriculum_identity = _curriculum_identity(curriculum)
        if not curriculum_identity:
            raise MissingCurriculumError("curriculum identity is empty")

        sections = CurriculumService.get_sections(curriculum)
        fmt = _detect_format(sections)
        ordered_topics = CurriculumService.get_all_topics_ordered(curriculum)

        if not ordered_topics:
            raise InvalidCurriculumError(
                f"curriculum {curriculum_identity!r} has no traversable topics"
            )

        section_by_pk = {section.id: section for section in sections}
        topic_refs = tuple(
            _topic_ref(topic, fmt=fmt, section_by_pk=section_by_pk)
            for topic in ordered_topics
        )
        section_ids = tuple(_section_identity(section) for section in sections)

        if fmt is CurriculumFormat.V2 and not section_ids:
            raise InvalidCurriculumError(
                f"curriculum {curriculum_identity!r} tagged V2 without section ids"
            )
        if fmt is CurriculumFormat.V1 and section_ids:
            raise InvalidCurriculumError(
                f"curriculum {curriculum_identity!r} tagged V1 with section ids"
            )

        try:
            return CurriculumContext.create(
                curriculum_identity,
                format=fmt,
                topics=topic_refs,
                section_ids=section_ids,
            )
        except ValueError as exc:
            raise InvalidCurriculumError(str(exc)) from exc


def _curriculum_identity(curriculum: Curriculum) -> str:
    """Stable string identity for domain CurriculumContext / Twin linkage."""
    if getattr(curriculum, "id", None) is None:
        return ""
    return str(curriculum.id)


def _detect_format(sections: list[Section]) -> CurriculumFormat:
    """Map section presence to V1/V2 — same branch as canonical traversal."""
    if sections:
        return CurriculumFormat.V2
    return CurriculumFormat.V1


def _section_identity(section: Section) -> str:
    """Prefer official syllabus id, then code, then persisted primary key."""
    if section.official_id and str(section.official_id).strip():
        return str(section.official_id).strip()
    if section.code and str(section.code).strip():
        return str(section.code).strip()
    return str(section.id)


def _topic_ref(
    topic: Topic,
    *,
    fmt: CurriculumFormat,
    section_by_pk: dict[int, Section],
) -> CurriculumTopicRef:
    """Project one ORM topic into a domain CurriculumTopicRef."""
    topic_id = str(topic.id).strip()
    if not topic_id:
        raise InvalidCurriculumError("topic identity is empty")

    if fmt is CurriculumFormat.V1:
        return CurriculumTopicRef.create(
            topic_id,
            weight=float(topic.syllabus_weight),
            section_id=None,
        )

    if topic.section_id is None:
        raise InvalidCurriculumError(
            f"V2 topic id={topic.id} is missing section_id"
        )
    section = section_by_pk.get(topic.section_id)
    if section is None:
        raise InvalidCurriculumError(
            f"V2 topic id={topic.id} references unknown section_id={topic.section_id}"
        )

    weight = (
        float(section.exam_weight)
        if section.exam_weight is not None
        else None
    )
    return CurriculumTopicRef.create(
        topic_id,
        weight=weight,
        section_id=_section_identity(section),
    )
