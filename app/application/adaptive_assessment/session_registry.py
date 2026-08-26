"""Adaptive Assessment session type registry — product metadata only.

Describes learner-visible session types. No selection, scoring, or Twin logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class SessionTypeId(StrEnum):
    """Stable identifiers for Adaptive Assessment session types."""

    QUICK_CHECK = "quick_check"
    DEEP_CHECK = "deep_check"
    RECOVERY_CHECK = "recovery_check"
    CONFIDENCE_CHECK = "confidence_check"
    REVISION_CHECK = "revision_check"
    READINESS_CHECK = "readiness_check"


@dataclass(frozen=True)
class SessionTypeDefinition:
    """Immutable product metadata for one learner-visible session type.

    Attributes:
        identifier: Stable machine id (``SessionTypeId`` value).
        display_name: Student-facing name.
        short_description: One-line purpose.
        icon_token: Design-system icon token (no asset binding here).
        colour_token: Design-system colour token.
        expected_duration_minutes: Typical duration band midpoint (minutes).
        expected_duration_label: Student-facing duration estimate.
        educational_intent: Product intent label (not an algorithm).
        student_facing_copy_key: Key into the copy registry for entry frame.
        mission_compatible: Whether the type may appear inside a Mission.
        tutor_compatible: Whether Tutor explanation may attach after.
    """

    identifier: str
    display_name: str
    short_description: str
    icon_token: str
    colour_token: str
    expected_duration_minutes: int
    expected_duration_label: str
    educational_intent: str
    student_facing_copy_key: str
    mission_compatible: bool
    tutor_compatible: bool


SESSION_TYPES: dict[str, SessionTypeDefinition] = {
    SessionTypeId.QUICK_CHECK: SessionTypeDefinition(
        identifier=SessionTypeId.QUICK_CHECK,
        display_name="Quick Check",
        short_description=(
            "A short formative probe to keep today's plan accurate."
        ),
        icon_token="aa.icon.quick_check",
        colour_token="aa.colour.calm_teal",
        expected_duration_minutes=5,
        expected_duration_label="About 3–8 minutes",
        educational_intent="daily_checkpoint",
        student_facing_copy_key="session.quick_check.frame",
        mission_compatible=True,
        tutor_compatible=True,
    ),
    SessionTypeId.DEEP_CHECK: SessionTypeDefinition(
        identifier=SessionTypeId.DEEP_CHECK,
        display_name="Deep Check",
        short_description=(
            "A careful confirmation of understanding, still formative."
        ),
        icon_token="aa.icon.deep_check",
        colour_token="aa.colour.steady_blue",
        expected_duration_minutes=15,
        expected_duration_label="About 10–20 minutes",
        educational_intent="knowledge_confirmation",
        student_facing_copy_key="session.deep_check.frame",
        mission_compatible=True,
        tutor_compatible=True,
    ),
    SessionTypeId.RECOVERY_CHECK: SessionTypeDefinition(
        identifier=SessionTypeId.RECOVERY_CHECK,
        display_name="Recovery Check",
        short_description=(
            "A gentle re-entry check after struggle or time away."
        ),
        icon_token="aa.icon.recovery_check",
        colour_token="aa.colour.warm_amber",
        expected_duration_minutes=8,
        expected_duration_label="Short to moderate. Take your time",
        educational_intent="gentle_reorientation",
        student_facing_copy_key="session.recovery_check.frame",
        mission_compatible=True,
        tutor_compatible=True,
    ),
    SessionTypeId.CONFIDENCE_CHECK: SessionTypeDefinition(
        identifier=SessionTypeId.CONFIDENCE_CHECK,
        display_name="Confidence Check",
        short_description=(
            "Align how sure you feel with what the evidence shows."
        ),
        icon_token="aa.icon.confidence_check",
        colour_token="aa.colour.soft_navy",
        expected_duration_minutes=6,
        expected_duration_label="About 5–10 minutes",
        educational_intent="confidence_calibration",
        student_facing_copy_key="session.confidence_check.frame",
        mission_compatible=True,
        tutor_compatible=True,
    ),
    SessionTypeId.REVISION_CHECK: SessionTypeDefinition(
        identifier=SessionTypeId.REVISION_CHECK,
        display_name="Revision Check",
        short_description="See what still holds from earlier learning.",
        icon_token="aa.icon.revision_check",
        colour_token="aa.colour.forest_green",
        expected_duration_minutes=10,
        expected_duration_label="Short to moderate",
        educational_intent="durability_verification",
        student_facing_copy_key="session.revision_check.frame",
        mission_compatible=True,
        tutor_compatible=True,
    ),
    SessionTypeId.READINESS_CHECK: SessionTypeDefinition(
        identifier=SessionTypeId.READINESS_CHECK,
        display_name="Readiness Check",
        short_description=(
            "An honest sample to guide remaining study, not a predicted result."
        ),
        icon_token="aa.icon.readiness_check",
        colour_token="aa.colour.slate",
        expected_duration_minutes=15,
        expected_duration_label="Moderate: within your time budget",
        educational_intent="bounded_readiness_honesty",
        student_facing_copy_key="session.readiness_check.frame",
        mission_compatible=True,
        tutor_compatible=True,
    ),
}


def get_session_type(identifier: str | SessionTypeId) -> SessionTypeDefinition:
    """Return the session type definition or raise ``KeyError``."""
    key = str(identifier)
    if key not in SESSION_TYPES:
        raise KeyError(f"unknown Adaptive Assessment session type: {key}")
    return SESSION_TYPES[key]


def iter_session_types() -> tuple[SessionTypeDefinition, ...]:
    """Return all registered session types in stable registry order."""
    return tuple(SESSION_TYPES[key] for key in SESSION_TYPES)
