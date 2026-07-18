"""Weakness profile — topics needing educational attention."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from app.domain.student_twin.confidence_band import ConfidenceBand


class WeaknessKind(StrEnum):
    """Kinds of educational weakness the Twin may surface."""

    LOW_MASTERY = "low_mastery"
    LOW_RETENTION = "low_retention"
    LOW_CONFIDENCE = "low_confidence"
    CONFLICTING_EVIDENCE = "conflicting_evidence"
    STALE_EVIDENCE = "stale_evidence"


@dataclass(frozen=True)
class WeaknessItem:
    """A single explainable weakness entry."""

    topic_id: str
    kind: WeaknessKind
    severity: float
    confidence: ConfidenceBand
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)
    rationale: str = ""

    @classmethod
    def create(
        cls,
        topic_id: str,
        kind: WeaknessKind | str,
        severity: float,
        *,
        confidence: ConfidenceBand | str = ConfidenceBand.LOW,
        evidence_ids: list[str] | tuple[str, ...] | None = None,
        rationale: str = "",
    ) -> WeaknessItem:
        """Construct a WeaknessItem."""
        tid = _require_non_empty(topic_id, "topic_id")
        wk = kind if isinstance(kind, WeaknessKind) else WeaknessKind(str(kind))
        sev = _unit_interval(severity, "severity")
        band = (
            confidence
            if isinstance(confidence, ConfidenceBand)
            else ConfidenceBand(str(confidence).strip().lower())
        )
        return cls(
            topic_id=tid,
            kind=wk,
            severity=sev,
            confidence=band,
            evidence_ids=tuple(evidence_ids or ()),
            rationale=(rationale or "").strip(),
        )


@dataclass(frozen=True)
class WeaknessProfile:
    """Ordered weakness items (highest severity first when built by analyser)."""

    items: tuple[WeaknessItem, ...] = field(default_factory=tuple)
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def empty(cls) -> WeaknessProfile:
        """Return an empty weakness profile."""
        return cls()

    @classmethod
    def create(
        cls,
        items: list[WeaknessItem] | tuple[WeaknessItem, ...] | None = None,
        *,
        evidence_ids: list[str] | tuple[str, ...] | None = None,
    ) -> WeaknessProfile:
        """Construct a WeaknessProfile."""
        return cls(
            items=tuple(items or ()),
            evidence_ids=tuple(evidence_ids or ()),
        )

    @property
    def topic_ids(self) -> tuple[str, ...]:
        """Distinct topic ids appearing in weaknesses (order preserved)."""
        seen: set[str] = set()
        ordered: list[str] = []
        for item in self.items:
            if item.topic_id not in seen:
                seen.add(item.topic_id)
                ordered.append(item.topic_id)
        return tuple(ordered)

    @property
    def is_empty(self) -> bool:
        """True when no weaknesses are recorded."""
        return not self.items


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _unit_interval(value: float, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ValueError(f"{field_name} must be a number in [0, 1]")
    numeric = float(value)
    if numeric < 0.0 or numeric > 1.0:
        raise ValueError(f"{field_name} must be in [0, 1]")
    return numeric
