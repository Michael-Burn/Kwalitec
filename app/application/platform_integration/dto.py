"""DTOs for the Founder → Student bridge (PI-002A)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from app.application.educational_runtime_engine.coexistence import (
    RuntimeAuthority,
)


@dataclass(frozen=True)
class PublishedSubjectOffer:
    """A founder-published subject visible in student discovery."""

    subject_code: str
    title: str
    version_label: str
    package_id: int
    curriculum_identity: str
    source: str = "published_curriculum"


@dataclass(frozen=True)
class RoutingDecision:
    """Auditable runtime selection for one enrolment attempt."""

    subject_code: str
    category_code: str
    runtime_authority: RuntimeAuthority
    reason: str
    published_package_id: int | None
    curriculum_identity: str | None
    discovery_enabled: bool
    enrolment_enabled: bool
    flags_snapshot: dict[str, Any]


@dataclass(frozen=True)
class EnrolmentBridgeResult:
    """Outcome of a bridged enrolment attempt."""

    runtime_authority: RuntimeAuthority
    routing: RoutingDecision
    audit_id: str
    # Runtime C fields (None for Runtime A)
    enrolment_id: str | None = None
    curriculum_identity: str | None = None
    # Runtime A fields (None for Runtime C)
    study_plan_id: int | None = None
    redirect_target: str = "student_home"
    message: str = ""


@dataclass(frozen=True)
class RoutingAuditSnapshot:
    """Persisted routing audit row."""

    audit_id: str
    user_id: int
    subject_code: str
    category_code: str
    runtime_authority: str
    decision_reason: str
    published_package_id: int | None
    curriculum_identity: str | None
    enrolment_id: str | None
    study_plan_id: int | None
    flags_json: dict[str, Any]
    created_at: datetime | None = None
