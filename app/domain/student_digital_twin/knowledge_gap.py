"""Knowledge gap inferences — must cite curriculum retrieval evidence."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum


class GapSeverity(StrEnum):
    """Severity of an identified knowledge gap."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass(frozen=True)
class KnowledgeGap:
    """Evidence-backed knowledge gap for one curriculum concept.

    Every gap MUST reference evidence obtained via CurriculumRetrievalService.
    Heuristics that bypass retrieval are forbidden.
    """

    gap_id: str
    twin_id: str
    concept_id: str
    concept_title: str = ""
    severity: GapSeverity = GapSeverity.MEDIUM
    confidence: float = 0.0
    likely_prerequisite_id: str = ""
    likely_prerequisite_title: str = ""
    supporting_evidence: tuple[str, ...] = ()
    retrieval_log_id: str | None = None
    estimated_recovery_effort: float = 0.0
    reason: str = ""
    identified_at: datetime | None = None

    def __post_init__(self) -> None:
        if not (self.gap_id or "").strip():
            raise ValueError("gap_id is required")
        if not (self.concept_id or "").strip():
            raise ValueError("concept_id is required")
        if not self.supporting_evidence:
            raise ValueError(
                "knowledge gaps require supporting evidence from "
                "CurriculumRetrievalService"
            )
        object.__setattr__(self, "confidence", _clamp(self.confidence))
        object.__setattr__(
            self,
            "estimated_recovery_effort",
            max(0.0, float(self.estimated_recovery_effort)),
        )
        severity = (
            self.severity
            if isinstance(self.severity, GapSeverity)
            else GapSeverity(str(self.severity))
        )
        object.__setattr__(self, "severity", severity)
        when = self.identified_at
        if when is not None and when.tzinfo is not None:
            object.__setattr__(
                self, "identified_at", when.astimezone(UTC).replace(tzinfo=None)
            )
        object.__setattr__(
            self, "supporting_evidence", tuple(self.supporting_evidence)
        )


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, float(value)))
