"""DTOs for Founder Validation metrics and workflows (FV-001).

Observational only — no educational reasoning or recommendation payloads.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.application.runtime_integration.dto import CoverageMetric


@dataclass(frozen=True, slots=True)
class RateMetric:
    """Explainable numerator / denominator rate."""

    metric_id: str
    label: str
    numerator: int
    denominator: int
    definition: str

    @property
    def ratio(self) -> float:
        if self.denominator <= 0:
            return 0.0
        return self.numerator / self.denominator

    @property
    def pct(self) -> float:
        return 100.0 * self.ratio

    def to_dict(self) -> dict[str, Any]:
        return {
            "metric_id": self.metric_id,
            "label": self.label,
            "numerator": self.numerator,
            "denominator": self.denominator,
            "ratio": self.ratio,
            "pct": self.pct,
            "definition": self.definition,
        }


@dataclass(frozen=True, slots=True)
class LatencyMetric:
    """Latency summary in milliseconds."""

    metric_id: str
    label: str
    sample_count: int
    mean_ms: float | None
    p95_ms: float | None
    definition: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "metric_id": self.metric_id,
            "label": self.label,
            "sample_count": self.sample_count,
            "mean_ms": self.mean_ms,
            "p95_ms": self.p95_ms,
            "definition": self.definition,
        }


@dataclass(frozen=True, slots=True)
class WorkflowStep:
    """One step on the Version 1 student journey under validation."""

    step_id: str
    name: str
    surface: str
    ei_touchpoint: str
    journal_required: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "step_id": self.step_id,
            "name": self.name,
            "surface": self.surface,
            "ei_touchpoint": self.ei_touchpoint,
            "journal_required": self.journal_required,
        }


@dataclass(frozen=True, slots=True)
class FounderValidationMetricsReport:
    """Baseline product metrics for FV-001 dogfooding."""

    onboarding_completion: RateMetric
    sci_creation_success: CoverageMetric
    experience_model_generation: RateMetric
    runtime_a_fallback: RateMetric
    session_completion: RateMetric
    evidence_recording_success: RateMetric
    decision_refresh_latency: LatencyMetric
    system_failures: int
    lifecycle_failures: RateMetric
    computed_at: str
    notes: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "onboarding_completion": self.onboarding_completion.to_dict(),
            "sci_creation_success": self.sci_creation_success.to_dict(),
            "experience_model_generation": self.experience_model_generation.to_dict(),
            "runtime_a_fallback": self.runtime_a_fallback.to_dict(),
            "session_completion": self.session_completion.to_dict(),
            "evidence_recording_success": self.evidence_recording_success.to_dict(),
            "decision_refresh_latency": self.decision_refresh_latency.to_dict(),
            "system_failures": self.system_failures,
            "lifecycle_failures": self.lifecycle_failures.to_dict(),
            "computed_at": self.computed_at,
            "notes": list(self.notes),
        }
