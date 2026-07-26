"""Presentation-ready diagnostics DTOs — internal ops only (P2-MS007).

Must never be exposed on student-facing routes or templates.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.infrastructure.adapters.experience_observation.health import (
    PipelineHealthReport,
)
from app.infrastructure.adapters.experience_observation.journey_trace import (
    JourneyTrace,
)


@dataclass(frozen=True)
class FeatureFlagDiagnostics:
    """Feature-flag projection for ops dashboards (no educational meaning)."""

    enable_experience_diagnostics: bool = False
    enable_experience_observation: bool = False
    enable_evidence_platform: bool = False
    enable_unified_journey: bool = False

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "enable_evidence_platform": self.enable_evidence_platform,
            "enable_experience_diagnostics": self.enable_experience_diagnostics,
            "enable_experience_observation": self.enable_experience_observation,
            "enable_unified_journey": self.enable_unified_journey,
        }


@dataclass(frozen=True)
class ObservationCounters:
    """Aggregate publish counters — no student identifiers."""

    observations_published: int = 0
    observations_accepted: int = 0
    observations_rejected: int = 0
    observations_skipped: int = 0
    journey_events_traced: int = 0
    intake_latency_ms_sum: float = 0.0
    intake_latency_ms_count: int = 0
    mean_intake_latency_ms: float = 0.0

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "intake_latency_ms_count": self.intake_latency_ms_count,
            "intake_latency_ms_sum": round(self.intake_latency_ms_sum, 3),
            "journey_events_traced": self.journey_events_traced,
            "mean_intake_latency_ms": self.mean_intake_latency_ms,
            "observations_accepted": self.observations_accepted,
            "observations_published": self.observations_published,
            "observations_rejected": self.observations_rejected,
            "observations_skipped": self.observations_skipped,
        }


@dataclass(frozen=True)
class PublisherHealthSummary:
    """Publisher health projection for ops surfaces."""

    available: bool = False
    enabled: bool = False
    publisher_id: str = ""
    publisher_version: str = ""
    evidence_bound: bool = False

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "available": self.available,
            "enabled": self.enabled,
            "evidence_bound": self.evidence_bound,
            "publisher_id": self.publisher_id,
            "publisher_version": self.publisher_version,
        }


@dataclass(frozen=True)
class ExperienceDiagnosticsDashboard:
    """Internal-only diagnostics dashboard model.

    Presentation-ready for founder / ops tooling. Must not be rendered
    into student Experience templates or public APIs.
    """

    diagnostics_enabled: bool
    feature_flags: FeatureFlagDiagnostics
    counters: ObservationCounters
    publisher_health: PublisherHealthSummary
    pipeline_health: PipelineHealthReport
    recent_traces: tuple[JourneyTrace, ...] = field(default_factory=tuple)
    audience: str = "internal_ops"
    influences_student: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "diagnostics_enabled", bool(self.diagnostics_enabled))
        object.__setattr__(self, "recent_traces", tuple(self.recent_traces))
        object.__setattr__(self, "audience", (self.audience or "internal_ops").strip())
        object.__setattr__(self, "influences_student", False)

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "audience": self.audience,
            "counters": self.counters.to_canonical_dict(),
            "diagnostics_enabled": self.diagnostics_enabled,
            "feature_flags": self.feature_flags.to_canonical_dict(),
            "influences_student": self.influences_student,
            "pipeline_health": self.pipeline_health.to_canonical_dict(),
            "publisher_health": self.publisher_health.to_canonical_dict(),
            "recent_traces": [t.to_canonical_dict() for t in self.recent_traces],
        }
