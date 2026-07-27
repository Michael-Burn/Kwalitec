"""Mastery per curriculum concept — evidence-backed inference."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum


class MasteryTrend(StrEnum):
    """Directional mastery trend derived from recent outcomes."""

    IMPROVING = "improving"
    STABLE = "stable"
    DECLINING = "declining"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class MasteryRecord:
    """Mastery inference for one curriculum concept.

    Evolves from educational reasoning, not simple averages.
    """

    mastery_id: str
    twin_id: str
    concept_id: str
    concept_title: str = ""
    mastery_score: float = 0.0
    confidence: float = 0.0
    trend: MasteryTrend = MasteryTrend.UNKNOWN
    evidence_count: int = 0
    supporting_evidence: tuple[str, ...] = ()
    last_updated: datetime | None = None
    reason: str = ""

    def __post_init__(self) -> None:
        if not (self.mastery_id or "").strip():
            raise ValueError("mastery_id is required")
        if not (self.concept_id or "").strip():
            raise ValueError("concept_id is required")
        object.__setattr__(self, "mastery_score", _clamp(self.mastery_score))
        object.__setattr__(self, "confidence", _clamp(self.confidence))
        trend = (
            self.trend
            if isinstance(self.trend, MasteryTrend)
            else MasteryTrend(str(self.trend))
        )
        object.__setattr__(self, "trend", trend)
        when = self.last_updated
        if when is not None and when.tzinfo is not None:
            object.__setattr__(
                self, "last_updated", when.astimezone(UTC).replace(tzinfo=None)
            )
        object.__setattr__(
            self, "supporting_evidence", tuple(self.supporting_evidence or ())
        )


@dataclass(frozen=True)
class MasteryMap:
    """Collection of mastery records keyed by concept."""

    records: tuple[MasteryRecord, ...] = ()

    def by_concept(self) -> dict[str, MasteryRecord]:
        return {r.concept_id: r for r in self.records}

    def get(self, concept_id: str) -> MasteryRecord | None:
        return self.by_concept().get(concept_id)

    def with_record(self, record: MasteryRecord) -> MasteryMap:
        others = tuple(r for r in self.records if r.concept_id != record.concept_id)
        return MasteryMap(records=(*others, record))

    @classmethod
    def empty(cls) -> MasteryMap:
        return cls(records=())


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, float(value)))
