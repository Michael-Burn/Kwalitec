"""Result types for coverage reconciliation (dual-source eligibility)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class CoverageDisplay:
    """Student-facing coverage numbers derived from reconciled eligibility.

    Covered units are CONFIRMED_COVERED plus HISTORICALLY_COMPLETED only.
    Ambiguous historical activity and NOT_COVERED never inflate the count.
    """

    covered_count: int
    topic_count: int
    coverage_ratio: float
    coverage_percent: int
    coverage_label: str
    confirmed_covered_count: int
    historically_completed_count: int


@dataclass(frozen=True)
class EvidenceProvenance:
    """One evidence sighting with enough detail to audit the verdict."""

    source: str
    accepted: bool
    reason: str
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CanonicalCoverageVerdict:
    """Reconciled coverage posture for one canonical curriculum topic."""

    canonical_id: str
    curriculum_version: str
    title: str
    legacy_completion_present: bool
    legacy_completion_accepted: bool
    verified_completion_present: bool
    verified_completion_accepted: bool
    mapping_status: str | None
    evidence_sources: tuple[str, ...]
    eligibility: str
    reasoning: str
    provenance: tuple[EvidenceProvenance, ...] = ()


@dataclass(frozen=True)
class UnmappedHistoricalActivity:
    """Historical activity that cannot be bound to an active canonical topic."""

    kind: str
    source_system: str
    source_id: str
    source_version: str | None
    mapping_status: str | None
    eligibility: str
    reasoning: str
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class LearnerCoverageReconciliation:
    """Full shadow reconciliation for one learner and curriculum version."""

    user_id: int
    user_email: str | None
    curriculum_version: str
    canonical_verdicts: tuple[CanonicalCoverageVerdict, ...]
    unmapped_activity: tuple[UnmappedHistoricalActivity, ...]
    summary: dict[str, int]
