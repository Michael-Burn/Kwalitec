"""Decision explanation — evidence-backed rationale for a recommendation."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.adaptive_learning.intervention_priority import (
    InterventionPriority,
    PriorityBand,
)
from app.domain.student_twin.confidence_band import ConfidenceBand


@dataclass(frozen=True)
class DecisionExplanation:
    """Explainable rationale attached to every adaptive recommendation.

    Every recommendation must include evidence considered, decision rationale,
    priority, expected educational benefit, and confidence.
    """

    evidence_considered: tuple[str, ...]
    rationale: str
    priority_score: float
    priority_band: PriorityBand
    expected_educational_benefit: str
    confidence: ConfidenceBand
    detail_lines: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        *,
        evidence_considered: list[str] | tuple[str, ...] | None = None,
        rationale: str,
        priority: InterventionPriority | float,
        expected_educational_benefit: str,
        confidence: ConfidenceBand | str,
        detail_lines: list[str] | tuple[str, ...] | None = None,
    ) -> DecisionExplanation:
        """Construct a DecisionExplanation."""
        reason = (rationale or "").strip()
        if not reason:
            raise ValueError("rationale must be a non-empty string")
        benefit = (expected_educational_benefit or "").strip()
        if not benefit:
            raise ValueError("expected_educational_benefit must be a non-empty string")
        if isinstance(priority, InterventionPriority):
            score = priority.score
            band = priority.band
        else:
            from app.domain.adaptive_learning.intervention_priority import (
                priority_band_from_score,
            )

            score = float(priority)
            if score < 0.0 or score > 1.0:
                raise ValueError("priority must be in [0, 1]")
            band = priority_band_from_score(score)
        band_conf = (
            confidence
            if isinstance(confidence, ConfidenceBand)
            else ConfidenceBand(str(confidence).strip().lower())
        )
        evidence = tuple(
            e.strip() for e in (evidence_considered or ()) if (e or "").strip()
        )
        details = tuple(
            d.strip() for d in (detail_lines or ()) if (d or "").strip()
        )
        return cls(
            evidence_considered=evidence,
            rationale=reason,
            priority_score=score,
            priority_band=band,
            expected_educational_benefit=benefit,
            confidence=band_conf,
            detail_lines=details,
        )

    @property
    def has_evidence(self) -> bool:
        """True when at least one evidence id was considered."""
        return bool(self.evidence_considered)
