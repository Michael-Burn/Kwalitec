"""Mission presentation helpers for Quick Check entry (ILE-001B).

Assembles entry-card contracts and WTForms for Mission / Session templates.
No planning heuristics or educational intelligence.
"""

from __future__ import annotations

from dataclasses import dataclass

from flask import has_request_context

from app.application.adaptive_assessment.localisation import resolve_copy
from app.application.adaptive_assessment.quick_check_contracts import (
    QuickCheckMissionCardContract,
)
from app.application.adaptive_assessment.quick_check_experience import (
    QuickCheckExperienceService,
    get_quick_check_experience_service,
)
from app.application.adaptive_assessment.session_registry import SessionTypeId
from app.application.adaptive_assessment.telemetry import (
    TelemetryEventName,
    build_telemetry_event,
)
from app.presentation.adaptive_assessment.forms import (
    DeferQuickCheckForm,
    StartQuickCheckForm,
    WhyThisForm,
)
from app.presentation.adaptive_assessment.views import pop_mission_ack


@dataclass(frozen=True)
class QuickCheckMissionEmbed:
    """Everything a Mission/Session template needs for the entry card."""

    card: QuickCheckMissionCardContract
    start_form: StartQuickCheckForm
    why_form: WhyThisForm
    defer_form: DeferQuickCheckForm
    mission_ack: str
    available: bool


def build_mission_quick_check_embed(
    *,
    mission_ref: str,
    subject_code: str = "",
    cohort_id: str | None = None,
    return_endpoint: str = "",
    return_session_id: str = "",
    service: QuickCheckExperienceService | None = None,
    emit_viewed: bool = True,
) -> QuickCheckMissionEmbed | None:
    """Return embed payload when Quick Check is available; else ``None``.

    Args:
        mission_ref: Mission or session id string used as experience linkage.
        subject_code: Optional subject for flag gating.
        cohort_id: Optional cohort for flag gating.
        return_endpoint: Flask endpoint name for Mission return.
        return_session_id: Session Experience id when returning to ``/session``.
        service: Optional injected experience service.
        emit_viewed: When True, record AdaptiveAssessmentViewed telemetry.
    """
    svc = service or get_quick_check_experience_service()
    if not svc.is_available(
        subject_code=subject_code or None, cohort_id=cohort_id
    ):
        return None
    card = svc.mission_card(
        subject_code=subject_code or None, cohort_id=cohort_id
    )
    if emit_viewed:
        svc.telemetry.record(
            build_telemetry_event(
                TelemetryEventName.ADAPTIVE_ASSESSMENT_VIEWED,
                session_type_id=SessionTypeId.QUICK_CHECK,
                subject_code=subject_code,
                payload={"surface": "mission_entry_card"},
            )
        )

    start_form = StartQuickCheckForm()
    start_form.mission_ref.data = mission_ref
    start_form.subject_code.data = subject_code
    start_form.return_endpoint.data = return_endpoint
    start_form.return_session_id.data = return_session_id
    start_form.submit.label.text = resolve_copy("quick_check.invitation.cta")

    why_form = WhyThisForm()
    why_form.mission_ref.data = mission_ref
    why_form.subject_code.data = subject_code
    why_form.submit.label.text = resolve_copy("quick_check.invitation.why_this")

    defer_form = DeferQuickCheckForm()
    defer_form.mission_ref.data = mission_ref
    defer_form.subject_code.data = subject_code
    defer_form.return_endpoint.data = return_endpoint
    defer_form.return_session_id.data = return_session_id
    defer_form.submit.label.text = resolve_copy("action.defer")

    _ = mission_ref  # linkage carried on forms
    ack = ""
    if has_request_context():
        ack = pop_mission_ack()
    return QuickCheckMissionEmbed(
        card=card,
        start_form=start_form,
        why_form=why_form,
        defer_form=defer_form,
        mission_ack=ack,
        available=True,
    )
