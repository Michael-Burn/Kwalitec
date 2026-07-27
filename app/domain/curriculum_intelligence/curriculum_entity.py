"""Curriculum knowledge entities produced by deterministic mapping.

These are CIP knowledge entities — not Student Twin runtime entities and not
ORM models. Persistence adapters map them into normalised tables.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class CurriculumEntityKind(StrEnum):
    """Hierarchy kinds for mapped curriculum knowledge."""

    SUBJECT = "subject"
    MODULE = "module"
    LEARNING_OBJECTIVE = "learning_objective"
    TOPIC = "topic"
    SUBTOPIC = "subtopic"
    CONCEPT = "concept"
    FORMULA = "formula"
    EXAMPLE = "example"
    PRACTICE_QUESTION = "practice_question"
    SOURCE_REFERENCE = "source_reference"


# Parent → allowed child kinds (deterministic hierarchy constraints).
ENTITY_CHILD_KINDS: dict[CurriculumEntityKind, frozenset[CurriculumEntityKind]] = {
    CurriculumEntityKind.SUBJECT: frozenset(
        {
            CurriculumEntityKind.MODULE,
            CurriculumEntityKind.LEARNING_OBJECTIVE,
            CurriculumEntityKind.TOPIC,
            CurriculumEntityKind.SOURCE_REFERENCE,
        }
    ),
    CurriculumEntityKind.MODULE: frozenset(
        {
            CurriculumEntityKind.LEARNING_OBJECTIVE,
            CurriculumEntityKind.TOPIC,
            CurriculumEntityKind.SOURCE_REFERENCE,
        }
    ),
    CurriculumEntityKind.LEARNING_OBJECTIVE: frozenset(
        {
            CurriculumEntityKind.TOPIC,
            CurriculumEntityKind.CONCEPT,
            CurriculumEntityKind.SOURCE_REFERENCE,
        }
    ),
    CurriculumEntityKind.TOPIC: frozenset(
        {
            CurriculumEntityKind.SUBTOPIC,
            CurriculumEntityKind.CONCEPT,
            CurriculumEntityKind.FORMULA,
            CurriculumEntityKind.EXAMPLE,
            CurriculumEntityKind.PRACTICE_QUESTION,
            CurriculumEntityKind.SOURCE_REFERENCE,
        }
    ),
    CurriculumEntityKind.SUBTOPIC: frozenset(
        {
            CurriculumEntityKind.CONCEPT,
            CurriculumEntityKind.FORMULA,
            CurriculumEntityKind.EXAMPLE,
            CurriculumEntityKind.PRACTICE_QUESTION,
            CurriculumEntityKind.SOURCE_REFERENCE,
        }
    ),
    CurriculumEntityKind.CONCEPT: frozenset(
        {
            CurriculumEntityKind.FORMULA,
            CurriculumEntityKind.EXAMPLE,
            CurriculumEntityKind.PRACTICE_QUESTION,
            CurriculumEntityKind.SOURCE_REFERENCE,
        }
    ),
    CurriculumEntityKind.FORMULA: frozenset({CurriculumEntityKind.SOURCE_REFERENCE}),
    CurriculumEntityKind.EXAMPLE: frozenset({CurriculumEntityKind.SOURCE_REFERENCE}),
    CurriculumEntityKind.PRACTICE_QUESTION: frozenset(
        {CurriculumEntityKind.SOURCE_REFERENCE}
    ),
    CurriculumEntityKind.SOURCE_REFERENCE: frozenset(),
}


@dataclass(frozen=True)
class CurriculumKnowledgeEntity:
    """One mapped curriculum knowledge node with provenance."""

    entity_id: str
    kind: CurriculumEntityKind
    title: str
    body: str
    parent_id: str | None
    child_ids: tuple[str, ...]
    source_document_id: int
    source_pages: tuple[int, ...]
    version_label: str
    confidence: float
    needs_review: bool
    structural_node_id: str | None = None
    attributes: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class CurriculumMap:
    """Full deterministic mapping result for one document."""

    map_id: str
    document_id: int
    parse_id: str
    subject_code: str
    version_label: str
    entities: tuple[CurriculumKnowledgeEntity, ...]
    diagnostics: tuple[str, ...] = ()
    uncertain_count: int = 0
