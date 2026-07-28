"""Immutable Adaptive Assessment product contracts — presentation only.

Describe session metadata, student-facing content, explanation metadata,
and Mission presentation. No educational intelligence.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.application.adaptive_assessment.accessibility import (
    AccessibilityMetadata,
    accessibility_for_session,
)
from app.application.adaptive_assessment.copy_registry import get_copy
from app.application.adaptive_assessment.localisation import resolve_copy
from app.application.adaptive_assessment.session_registry import (
    SessionTypeDefinition,
    get_session_type,
)


@dataclass(frozen=True)
class SessionPresentationContract:
    """Presentation contract for one Adaptive Assessment session type."""

    session_type_id: str
    display_name: str
    short_description: str
    icon_token: str
    colour_token: str
    expected_duration_label: str
    educational_intent: str
    mission_compatible: bool
    tutor_compatible: bool
    entry_frame: str
    accessibility: AccessibilityMetadata


@dataclass(frozen=True)
class StudentFacingContentContract:
    """Student-facing copy bundle for Adaptive Assessment chrome."""

    continue_learning: str
    strengthen_understanding: str
    build_confidence: str
    defer_label: str
    pause_label: str
    why_am_i_seeing_this: str
    why_body: str
    not_enough_evidence: str
    gather_more: str
    use_to_guide: str
    readiness_non_guarantee: str
    unavailable: str


@dataclass(frozen=True)
class ExplanationPresentationContract:
    """Explainability presentation metadata (why / next / uncertain)."""

    why_control_label: str
    why_body: str
    uncertainty_headline: str
    uncertainty_invite: str
    accessible_explain_label: str


@dataclass(frozen=True)
class MissionPresentationContract:
    """How an Adaptive Assessment step may present inside a Mission."""

    session_type_id: str
    mission_compatible: bool
    step_label: str
    effort_label: str
    defer_allowed_copy: str
    continue_copy: str


@dataclass(frozen=True)
class AdaptiveAssessmentProductContracts:
    """Bundle of immutable presentation contracts for Adaptive Assessment."""

    sessions: tuple[SessionPresentationContract, ...]
    content: StudentFacingContentContract
    explanation: ExplanationPresentationContract


def build_student_facing_content_contract() -> StudentFacingContentContract:
    """Build the shared student-facing content contract from the copy bank."""
    return StudentFacingContentContract(
        continue_learning=resolve_copy("action.continue_learning"),
        strengthen_understanding=resolve_copy(
            "action.strengthen_understanding"
        ),
        build_confidence=resolve_copy("action.build_confidence"),
        defer_label=resolve_copy("action.defer"),
        pause_label=resolve_copy("action.pause"),
        why_am_i_seeing_this=resolve_copy("explain.why_am_i_seeing_this"),
        why_body=resolve_copy("explain.why_body"),
        not_enough_evidence=resolve_copy(
            "uncertainty.not_enough_evidence"
        ),
        gather_more=resolve_copy("uncertainty.gather_more"),
        use_to_guide=resolve_copy("feedback.use_to_guide"),
        readiness_non_guarantee=resolve_copy("readiness.non_guarantee"),
        unavailable=resolve_copy("empty.adaptive_assessment_unavailable"),
    )


def build_explanation_presentation_contract() -> (
    ExplanationPresentationContract
):
    """Build explanation presentation metadata."""
    return ExplanationPresentationContract(
        why_control_label=resolve_copy("explain.why_am_i_seeing_this"),
        why_body=resolve_copy("explain.why_body"),
        uncertainty_headline=resolve_copy(
            "uncertainty.not_enough_evidence"
        ),
        uncertainty_invite=resolve_copy("uncertainty.gather_more"),
        accessible_explain_label=get_copy("a11y.explain_button").default,
    )


def build_session_presentation_contract(
    session_type_id: str,
) -> SessionPresentationContract:
    """Build a presentation contract for one session type."""
    session: SessionTypeDefinition = get_session_type(session_type_id)
    return SessionPresentationContract(
        session_type_id=session.identifier,
        display_name=session.display_name,
        short_description=session.short_description,
        icon_token=session.icon_token,
        colour_token=session.colour_token,
        expected_duration_label=session.expected_duration_label,
        educational_intent=session.educational_intent,
        mission_compatible=session.mission_compatible,
        tutor_compatible=session.tutor_compatible,
        entry_frame=resolve_copy(session.student_facing_copy_key),
        accessibility=accessibility_for_session(session.identifier),
    )


def build_mission_presentation_contract(
    session_type_id: str,
) -> MissionPresentationContract:
    """Build Mission presentation metadata for a session type."""
    session = get_session_type(session_type_id)
    return MissionPresentationContract(
        session_type_id=session.identifier,
        mission_compatible=session.mission_compatible,
        step_label=session.display_name,
        effort_label=session.expected_duration_label,
        defer_allowed_copy=resolve_copy("action.defer"),
        continue_copy=resolve_copy("action.continue_learning"),
    )


def build_product_contracts() -> AdaptiveAssessmentProductContracts:
    """Build the full immutable product contract bundle."""
    from app.application.adaptive_assessment.session_registry import (
        iter_session_types,
    )

    sessions = tuple(
        build_session_presentation_contract(s.identifier)
        for s in iter_session_types()
    )
    return AdaptiveAssessmentProductContracts(
        sessions=sessions,
        content=build_student_facing_content_contract(),
        explanation=build_explanation_presentation_contract(),
    )
