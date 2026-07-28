"""Deterministic preferred-authority routing (RI-001).

Selects Educational Intelligence vs Runtime A compatibility from SCI and
persisted Educational Decision presence only. Never ranks topics or invents
recommendations.
"""

from __future__ import annotations

from app.application.runtime_integration.dto import FallbackReason, RoutingDecision
from app.models.student_curriculum_binding import SciStudentCurriculumInstance


def list_active_instances(student_id: int) -> tuple[SciStudentCurriculumInstance, ...]:
    """Active SCI rows for a student, stable order (lowest id first)."""
    rows = (
        SciStudentCurriculumInstance.query.filter_by(
            student_id=int(student_id),
            is_active=True,
        )
        .order_by(SciStudentCurriculumInstance.id.asc())
        .all()
    )
    return tuple(rows)


def resolve_active_instance(
    student_id: int,
    *,
    subject_code: str | None = None,
) -> SciStudentCurriculumInstance | None:
    """Pick one active SCI: prefer subject match, else lowest id."""
    instances = list_active_instances(student_id)
    if not instances:
        return None
    if subject_code:
        wanted = subject_code.strip().upper()
        for instance in instances:
            if str(instance.subject_code or "").strip().upper() == wanted:
                return instance
    return instances[0]


def decide_authority(
    *,
    integration_enabled: bool,
    instance: SciStudentCurriculumInstance | None,
    decision_count: int,
    preferred_subject: str | None = None,
) -> RoutingDecision:
    """Return a deterministic routing decision.

    Args:
        integration_enabled: Feature flag for preferred-authority routing.
        instance: Active SCI when present.
        decision_count: Persisted EI-007 decisions for the instance.
        preferred_subject: Optional subject hint used for telemetry context.
    """
    if not integration_enabled:
        return RoutingDecision(
            use_educational_intelligence=False,
            subject_code=preferred_subject,
            fallback_reason=FallbackReason.RUNTIME_INTEGRATION_DISABLED,
            missing_prerequisite="ENABLE_RUNTIME_INTEGRATION",
        )

    if instance is None:
        reason = FallbackReason.NO_ACTIVE_SCI
        missing = "active_student_curriculum_instance"
        if preferred_subject and not preferred_subject.strip():
            reason = FallbackReason.SUBJECT_UNRESOLVED
            missing = "subject_code"
        return RoutingDecision(
            use_educational_intelligence=False,
            subject_code=preferred_subject,
            fallback_reason=reason,
            missing_prerequisite=missing,
        )

    subject = str(instance.subject_code or preferred_subject or "") or None
    if decision_count < 1:
        return RoutingDecision(
            use_educational_intelligence=False,
            instance_id=instance.instance_id,
            subject_code=subject,
            fallback_reason=FallbackReason.NO_EDUCATIONAL_DECISIONS,
            missing_prerequisite="ere_educational_decisions",
        )

    return RoutingDecision(
        use_educational_intelligence=True,
        instance_id=instance.instance_id,
        subject_code=subject,
        fallback_reason=None,
        missing_prerequisite=None,
    )
