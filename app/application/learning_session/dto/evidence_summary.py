"""Immutable summary of evidence collected during a Learning Session."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvidenceSummary:
    """Compact evidence posture for a single Learning Session.

    Never estimates mastery. Reports structural attribution only.

    Attributes:
        evidence_count: Number of journey-attributed evidence items on the session.
        evidence_types: Distinct evidence type values observed (stable order).
        confidence_levels: Distinct qualitative confidence levels observed.
        has_evidence: True when at least one evidence item is attached.
        session_id: Session identity the summary describes.
    """

    evidence_count: int
    evidence_types: tuple[str, ...]
    confidence_levels: tuple[str, ...]
    has_evidence: bool
    session_id: str
