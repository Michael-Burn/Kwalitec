"""Immutable comparison snapshot DTO."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ComparisonSnapshot:
    """Deterministic deltas between two Twin snapshots."""

    twin_id: str
    baseline_version: str
    current_version: str
    mastery_delta: float
    readiness_delta: float
    confidence_delta: float
    retention_delta: float
    evidence_added: int

    @classmethod
    def create(
        cls,
        *,
        twin_id: str,
        baseline_version: str,
        current_version: str,
        mastery_delta: float,
        readiness_delta: float,
        confidence_delta: float,
        retention_delta: float,
        evidence_added: int,
    ) -> ComparisonSnapshot:
        """Construct a ComparisonSnapshot."""
        return cls(
            twin_id=twin_id,
            baseline_version=baseline_version,
            current_version=current_version,
            mastery_delta=mastery_delta,
            readiness_delta=readiness_delta,
            confidence_delta=confidence_delta,
            retention_delta=retention_delta,
            evidence_added=evidence_added,
        )

    @property
    def mastery_improved(self) -> bool:
        """True when mastery increased."""
        return self.mastery_delta > 0.0
