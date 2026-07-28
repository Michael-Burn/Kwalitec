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
class TelemetrySnapshot:
    """Aggregated migration metrics for RI-005 readiness."""

    total_requests: int = 0
    educational_intelligence_count: int = 0
    fallback_count: int = 0
    migrated_users: frozenset[int] = field(default_factory=frozenset)
    fallback_users: frozenset[int] = field(default_factory=frozenset)
    fallback_by_reason: dict[str, int] = field(default_factory=dict)

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
            "fallback_by_reason": dict(self.fallback_by_reason),
        }
