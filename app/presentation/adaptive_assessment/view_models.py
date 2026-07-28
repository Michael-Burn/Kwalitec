"""View-model helpers for Quick Check templates."""

from __future__ import annotations

from dataclasses import dataclass

from app.application.adaptive_assessment.localisation import resolve_copy
from app.application.adaptive_assessment.quick_check_experience import (
    QuickCheckSurfaceSnapshot,
)


@dataclass(frozen=True)
class QuickCheckPageViewModel:
    """Template-facing page shell for Quick Check surfaces."""

    experience_id: str
    mission_ref: str
    phase: str
    subject_code: str
    page_eyebrow: str
    page_title: str
    page_description: str
    focus_label: str
    snapshot: QuickCheckSurfaceSnapshot
    return_endpoint: str
    return_session_id: str
    mission_ack: str


def page_from_snapshot(
    snapshot: QuickCheckSurfaceSnapshot,
    *,
    return_endpoint: str = "",
    return_session_id: str = "",
) -> QuickCheckPageViewModel:
    """Map an experience snapshot to a template view model."""
    title = resolve_copy("session.quick_check.name")
    description = ""
    if snapshot.introduction is not None:
        description = snapshot.introduction.duration_label
    elif snapshot.card is not None:
        description = snapshot.card.duration_label
    elif snapshot.completion is not None:
        description = snapshot.completion.use_to_guide
    return QuickCheckPageViewModel(
        experience_id=snapshot.experience_id,
        mission_ref=snapshot.mission_ref,
        phase=snapshot.phase,
        subject_code=snapshot.subject_code,
        page_eyebrow=resolve_copy("session.quick_check.name"),
        page_title=title,
        page_description=description,
        focus_label=snapshot.focus_label,
        snapshot=snapshot,
        return_endpoint=return_endpoint,
        return_session_id=return_session_id,
        mission_ack=resolve_copy("quick_check.mission.evidence_ack"),
    )
