"""DTOs for Runtime Integration Preferred Authority routing (RI-001)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from app.application.educational_experience_engine.dto import SurfaceBundle


class AuthoritySource(StrEnum):
    """Which pipeline produced the educational surface payload."""

    EDUCATIONAL_INTELLIGENCE = "educational_intelligence"
    RUNTIME_A_COMPATIBILITY = "runtime_a_compatibility"


class FallbackReason(StrEnum):
    """Measurable reasons Runtime A compatibility was selected."""

    RUNTIME_INTEGRATION_DISABLED = "runtime_integration_disabled"
    NO_ACTIVE_SCI = "no_active_sci"
    NO_EDUCATIONAL_DECISIONS = "no_educational_decisions"
    SUBJECT_UNRESOLVED = "subject_unresolved"


class IntegrationSurface(StrEnum):
    """Student surfaces that request educational experience payloads."""

    DASHBOARD = "dashboard"
    DAILY_MISSION = "daily_mission"
    COACH = "coach"
    REVISION_PLANNER = "revision_planner"
    STUDY_SESSION = "study_session"
    RECOMMENDATION = "recommendation"
    HOME = "home"


@dataclass(frozen=True)
class SurfaceExperienceBundle:
    """Preferred-authority experience bundle for one primary decision."""

    instance_id: str
    decision_id: str
    surfaces: SurfaceBundle
    authority: AuthoritySource = AuthoritySource.EDUCATIONAL_INTELLIGENCE

    def to_dict(self) -> dict[str, Any]:
        return {
            "instance_id": self.instance_id,
            "decision_id": self.decision_id,
            "authority": self.authority.value,
            "surfaces": self.surfaces.to_dict(),
        }


@dataclass(frozen=True)
class IntegrationResult:
    """Outcome of preferred-authority routing for one surface request.

    Exactly one of ``experience`` or ``compatibility_payload`` is populated
    according to ``authority``. Controllers consume this DTO — they do not
    re-select educational actions.
    """

    authority: AuthoritySource
    surface: IntegrationSurface
    student_id: int
    subject_code: str | None = None
    instance_id: str | None = None
    decision_id: str | None = None
    experience: SurfaceExperienceBundle | None = None
    compatibility_payload: Any = None
    fallback_reason: FallbackReason | None = None
    missing_prerequisite: str | None = None

    @property
    def uses_educational_intelligence(self) -> bool:
        return self.authority is AuthoritySource.EDUCATIONAL_INTELLIGENCE

    def to_dict(self) -> dict[str, Any]:
        return {
            "authority": self.authority.value,
            "surface": self.surface.value,
            "student_id": self.student_id,
            "subject_code": self.subject_code,
            "instance_id": self.instance_id,
            "decision_id": self.decision_id,
            "experience": (
                None if self.experience is None else self.experience.to_dict()
            ),
            "fallback_reason": (
                None if self.fallback_reason is None else self.fallback_reason.value
            ),
            "missing_prerequisite": self.missing_prerequisite,
            "compatibility_payload_present": self.compatibility_payload is not None,
        }


@dataclass(frozen=True)
class RoutingDecision:
    """Deterministic preferred-authority selection (no educational math)."""

    use_educational_intelligence: bool
    instance_id: str | None = None
    subject_code: str | None = None
    fallback_reason: FallbackReason | None = None
    missing_prerequisite: str | None = None


@dataclass
class FallbackEvent:
    """One recorded Runtime A fallback invocation."""

    student_id: int
    subject: str | None
    reason: FallbackReason
    timestamp: str
    missing_prerequisite: str | None
    surface: IntegrationSurface
    instance_id: str | None = None


@dataclass
class AdoptionEvent:
    """One recorded Educational Intelligence path success."""

    student_id: int
    subject: str | None
    timestamp: str
    surface: IntegrationSurface
    instance_id: str
    decision_id: str


@dataclass
class SurfaceUsageStats:
    """Route-level Educational Intelligence vs fallback counts."""

    surface: str
    educational_intelligence_count: int = 0
    fallback_count: int = 0

    @property
    def total(self) -> int:
        return self.educational_intelligence_count + self.fallback_count

    @property
    def ei_usage_pct(self) -> float:
        if self.total <= 0:
            return 0.0
        return 100.0 * self.educational_intelligence_count / self.total

    def to_dict(self) -> dict[str, Any]:
        return {
            "surface": self.surface,
            "educational_intelligence_count": self.educational_intelligence_count,
            "fallback_count": self.fallback_count,
            "total": self.total,
            "ei_usage_pct": self.ei_usage_pct,
        }


@dataclass
class TelemetrySnapshot:
    """Aggregated migration metrics for RI-002 / RI-005 readiness."""

    total_requests: int = 0
    educational_intelligence_count: int = 0
    fallback_count: int = 0
    migrated_users: frozenset[int] = field(default_factory=frozenset)
    fallback_users: frozenset[int] = field(default_factory=frozenset)
    fallback_by_reason: dict[str, int] = field(default_factory=dict)
    by_surface: dict[str, SurfaceUsageStats] = field(default_factory=dict)
    daily_ei_counts: dict[str, int] = field(default_factory=dict)
    daily_fallback_counts: dict[str, int] = field(default_factory=dict)

    @property
    def fallback_rate(self) -> float:
        if self.total_requests <= 0:
            return 0.0
        return self.fallback_count / self.total_requests

    @property
    def educational_intelligence_adoption_pct(self) -> float:
        if self.total_requests <= 0:
            return 0.0
        return 100.0 * self.educational_intelligence_count / self.total_requests

    @property
    def experience_model_generation_rate(self) -> float:
        """Share of RIS requests that produced Experience Models (0–1)."""
        if self.total_requests <= 0:
            return 0.0
        return self.educational_intelligence_count / self.total_requests

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_requests": self.total_requests,
            "educational_intelligence_count": self.educational_intelligence_count,
            "fallback_count": self.fallback_count,
            "fallback_rate": self.fallback_rate,
            "migrated_user_count": len(self.migrated_users),
            "fallback_user_count": len(self.fallback_users),
            "educational_intelligence_adoption_pct": (
                self.educational_intelligence_adoption_pct
            ),
            "experience_model_generation_rate": (
                self.experience_model_generation_rate
            ),
            "fallback_by_reason": dict(self.fallback_by_reason),
            "by_surface": {
                key: stats.to_dict() for key, stats in sorted(self.by_surface.items())
            },
            "daily_ei_counts": dict(sorted(self.daily_ei_counts.items())),
            "daily_fallback_counts": dict(sorted(self.daily_fallback_counts.items())),
        }


class InventoryStatus(StrEnum):
    """Lifecycle status for a Runtime A / legacy dependency."""

    ACTIVE = "active"
    DEPRECATED = "deprecated"
    REMOVABLE = "removable"
    BLOCKED = "blocked"


class RetirementGateId(StrEnum):
    """Measurable exit criteria for Runtime A recommendation authority."""

    SCI_COVERAGE = "sci_coverage"
    PUBLISHED_CURRICULUM_COVERAGE = "published_curriculum_coverage"
    EDUCATIONAL_DECISION_COVERAGE = "educational_decision_coverage"
    FALLBACK_RATE = "fallback_rate"
    EXPERIENCE_MODEL_RATE = "experience_model_rate"
    INTEGRATION_TESTS = "integration_tests"
    NO_ACTIVE_RUNTIME_A_AUTHORITY = "no_active_runtime_a_authority"


@dataclass(frozen=True)
class CoverageMetric:
    """Numerator / denominator coverage with explainable definition."""

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


@dataclass(frozen=True)
class AdoptionMetricsReport:
    """RI-002 adoption metrics assembled from DB coverage + RIS telemetry."""

    sci_coverage: CoverageMetric
    published_curriculum_coverage: CoverageMetric
    educational_decision_coverage: CoverageMetric
    experience_model_generation_rate: float
    runtime_a_fallback_rate: float
    educational_intelligence_request_pct: float
    route_level_usage: tuple[SurfaceUsageStats, ...]
    fallback_by_reason: dict[str, int]
    telemetry: TelemetrySnapshot
    computed_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "sci_coverage": self.sci_coverage.to_dict(),
            "published_curriculum_coverage": (
                self.published_curriculum_coverage.to_dict()
            ),
            "educational_decision_coverage": (
                self.educational_decision_coverage.to_dict()
            ),
            "experience_model_generation_rate": self.experience_model_generation_rate,
            "runtime_a_fallback_rate": self.runtime_a_fallback_rate,
            "educational_intelligence_request_pct": (
                self.educational_intelligence_request_pct
            ),
            "route_level_usage": [s.to_dict() for s in self.route_level_usage],
            "fallback_by_reason": dict(self.fallback_by_reason),
            "telemetry": self.telemetry.to_dict(),
            "computed_at": self.computed_at,
        }


@dataclass(frozen=True)
class InventoryEntry:
    """One remaining Runtime A / legacy / compatibility dependency."""

    entry_id: str
    component: str
    path: str
    category: str
    status: InventoryStatus
    notes: str
    blocks_retirement: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "component": self.component,
            "path": self.path,
            "category": self.category,
            "status": self.status.value,
            "notes": self.notes,
            "blocks_retirement": self.blocks_retirement,
        }


@dataclass(frozen=True)
class RuntimeInventoryReport:
    """Machine-readable inventory of remaining Runtime A dependencies."""

    generated_at: str
    entries: tuple[InventoryEntry, ...]

    def counts_by_status(self) -> dict[str, int]:
        counts: dict[str, int] = {s.value: 0 for s in InventoryStatus}
        for entry in self.entries:
            counts[entry.status.value] = counts.get(entry.status.value, 0) + 1
        return counts

    def to_dict(self) -> dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "counts_by_status": self.counts_by_status(),
            "entries": [e.to_dict() for e in self.entries],
        }


@dataclass(frozen=True)
class RetirementGate:
    """One documented, evaluable Runtime A retirement criterion."""

    gate_id: RetirementGateId
    title: str
    description: str
    operator: str
    threshold: float
    unit: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "gate_id": self.gate_id.value,
            "title": self.title,
            "description": self.description,
            "operator": self.operator,
            "threshold": self.threshold,
            "unit": self.unit,
        }


@dataclass(frozen=True)
class GateEvaluation:
    """Result of evaluating one retirement gate against live metrics."""

    gate: RetirementGate
    observed: float
    passed: bool
    evidence: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "gate": self.gate.to_dict(),
            "observed": self.observed,
            "passed": self.passed,
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class RetirementReadinessReport:
    """Aggregate readiness assessment for Runtime A removal (RI-005 input)."""

    metrics: AdoptionMetricsReport
    inventory: RuntimeInventoryReport
    gate_evaluations: tuple[GateEvaluation, ...]
    ready_for_retirement: bool
    assessed_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "metrics": self.metrics.to_dict(),
            "inventory": self.inventory.to_dict(),
            "gate_evaluations": [g.to_dict() for g in self.gate_evaluations],
            "ready_for_retirement": self.ready_for_retirement,
            "passed_gate_count": sum(1 for g in self.gate_evaluations if g.passed),
            "total_gate_count": len(self.gate_evaluations),
            "assessed_at": self.assessed_at,
        }
