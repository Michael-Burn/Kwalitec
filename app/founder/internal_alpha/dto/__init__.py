"""DTOs and transfer shapes for Internal Alpha exports (serialisation only)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class DuplicateRelation:
    """A detected duplicate relationship between two feedback items.

    ``source_id`` is considered a duplicate of ``target_id``.
    Relationships only — never remove feedback automatically.
    """

    source_id: str
    target_id: str
    reason: str
    similarity: float


@dataclass(frozen=True)
class ValidationIssue:
    """One validation problem discovered before processing."""

    code: str
    message: str
    path: str | None = None


@dataclass(frozen=True)
class ValidationReport:
    """Aggregated validation outcome for a week folder."""

    ok: bool
    issues: tuple[ValidationIssue, ...]

    @property
    def errors(self) -> tuple[ValidationIssue, ...]:
        return self.issues


def classified_feedback_to_dict(item: Any) -> dict[str, Any]:
    """Serialise ClassifiedFeedback for JSON export (no business logic)."""

    fi = item.feedback_item
    return {
        "id": fi.id,
        "filename": fi.filename,
        "contributor": fi.contributor,
        "week": fi.week,
        "raw_text": fi.raw_text,
        "created_at": fi.created_at.isoformat(),
        "category": item.category,
        "confidence": item.confidence,
        "duplicate_of": item.duplicate_of,
    }


def weekly_summary_to_dict(summary: Any) -> dict[str, Any]:
    """Serialise WeeklySummary for JSON export (no business logic)."""

    return {
        "week": summary.week,
        "total_feedback": summary.total_feedback,
        "category_counts": dict(summary.category_counts),
        "duplicate_count": summary.duplicate_count,
        "contributor_counts": dict(summary.contributor_counts),
        "generated_at": summary.generated_at.isoformat(),
    }


def duplicate_relations_to_dict(
    relations: tuple[DuplicateRelation, ...],
) -> Mapping[str, Any]:
    """Serialise duplicate relations for JSON export."""

    return {
        "duplicate_count": len(relations),
        "relations": [
            {
                "source_id": r.source_id,
                "target_id": r.target_id,
                "reason": r.reason,
                "similarity": r.similarity,
            }
            for r in relations
        ],
    }
