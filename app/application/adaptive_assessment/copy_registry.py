"""Adaptive Assessment copy registry — centralised student-facing strings.

English defaults only. Tone follows USER_EXPERIENCE_PHILOSOPHY.md and
ILE-001 design pack. No hard-coded UI strings should bypass this registry
for Adaptive Assessment surfaces.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AdaptiveAssessmentCopy:
    """One localisable copy entry.

    Attributes:
        key: Stable message id (dot-separated).
        default: English default text (may include ``{placeholders}``).
        description: Translator / product note (not shown to students).
        pluralizable: When True, ``default`` may use plural forms via the
            localisation catalogue (``one`` / ``other``).
    """

    key: str
    default: str
    description: str = ""
    pluralizable: bool = False


# Canonical Adaptive Assessment copy bank (ILE-001A).
_COPY: tuple[AdaptiveAssessmentCopy, ...] = (
    AdaptiveAssessmentCopy(
        key="session.quick_check.name",
        default="Quick Check",
        description="Session type display name",
    ),
    AdaptiveAssessmentCopy(
        key="session.deep_check.name",
        default="Deep Check",
        description="Session type display name",
    ),
    AdaptiveAssessmentCopy(
        key="session.recovery_check.name",
        default="Recovery Check",
        description="Session type display name",
    ),
    AdaptiveAssessmentCopy(
        key="session.confidence_check.name",
        default="Confidence Check",
        description="Session type display name",
    ),
    AdaptiveAssessmentCopy(
        key="session.revision_check.name",
        default="Revision Check",
        description="Session type display name",
    ),
    AdaptiveAssessmentCopy(
        key="session.readiness_check.name",
        default="Readiness Check",
        description="Session type display name",
    ),
    AdaptiveAssessmentCopy(
        key="session.quick_check.frame",
        default="Quick check — helps keep today's plan accurate.",
        description="Entry frame before first item",
    ),
    AdaptiveAssessmentCopy(
        key="session.deep_check.frame",
        default="Careful check on this topic — no grades, clearer next steps.",
        description="Entry frame before first item",
    ),
    AdaptiveAssessmentCopy(
        key="session.recovery_check.frame",
        default="Gentle check to restart accurately — take your time.",
        description="Entry frame before first item",
    ),
    AdaptiveAssessmentCopy(
        key="session.confidence_check.frame",
        default=(
            "Confidence check — helps align how sure you feel with what "
            "the evidence shows."
        ),
        description="Entry frame before first item",
    ),
    AdaptiveAssessmentCopy(
        key="session.revision_check.frame",
        default="Revision check — see what still feels solid.",
        description="Entry frame before first item",
    ),
    AdaptiveAssessmentCopy(
        key="session.readiness_check.frame",
        default=(
            "Readiness check — guides what to study next; it does not "
            "predict your result."
        ),
        description="Entry frame before first item",
    ),
    AdaptiveAssessmentCopy(
        key="action.continue_learning",
        default="Continue Learning",
        description="Primary post-check CTA",
    ),
    AdaptiveAssessmentCopy(
        key="action.strengthen_understanding",
        default="Strengthen Understanding",
        description="Recovery / reinforcement CTA",
    ),
    AdaptiveAssessmentCopy(
        key="action.build_confidence",
        default="Build Confidence",
        description="Confidence-oriented next step CTA",
    ),
    AdaptiveAssessmentCopy(
        key="action.defer",
        default="Not now",
        description="Decline / defer a check when Mission policy allows",
    ),
    AdaptiveAssessmentCopy(
        key="action.pause",
        default="Pause",
        description="Pause an in-progress check",
    ),
    AdaptiveAssessmentCopy(
        key="explain.why_am_i_seeing_this",
        default="Why am I seeing this?",
        description="Explainability disclosure control label",
    ),
    AdaptiveAssessmentCopy(
        key="explain.why_body",
        default=(
            "This check helps gather evidence so today's plan stays accurate. "
            "Your answers inform what to study next — they are not a grade."
        ),
        description="Default why-framing body",
    ),
    AdaptiveAssessmentCopy(
        key="uncertainty.not_enough_evidence",
        default="Not enough evidence yet",
        description="Honest uncertainty headline",
    ),
    AdaptiveAssessmentCopy(
        key="uncertainty.gather_more",
        default="Let's gather a little more information",
        description="Invite further evidence without pressure",
    ),
    AdaptiveAssessmentCopy(
        key="feedback.use_to_guide",
        default="We'll use this to guide practice.",
        description="Post-check evidence use line",
    ),
    AdaptiveAssessmentCopy(
        key="readiness.non_guarantee",
        default=(
            "This guides what to study next. It does not predict your result."
        ),
        description="Mandatory non-guarantee for Readiness Check",
    ),
    AdaptiveAssessmentCopy(
        key="empty.adaptive_assessment_unavailable",
        default="Learning checks are not available right now.",
        description="Disabled / flagged-off empty state",
    ),
    AdaptiveAssessmentCopy(
        key="duration.about_minutes",
        default="About {count} minutes",
        description="Duration estimate with count interpolation",
        pluralizable=True,
    ),
    AdaptiveAssessmentCopy(
        key="a11y.session_region",
        default="Learning check: {session_name}",
        description="Accessible region label for a check",
    ),
    AdaptiveAssessmentCopy(
        key="a11y.explain_button",
        default="Explain why this learning check is shown",
        description="Accessible name for why control",
    ),
    AdaptiveAssessmentCopy(
        key="a11y.defer_button",
        default="Defer this learning check and continue studying",
        description="Accessible name for defer control",
    ),
)

COPY_KEYS: frozenset[str] = frozenset(entry.key for entry in _COPY)
_BY_KEY: dict[str, AdaptiveAssessmentCopy] = {entry.key: entry for entry in _COPY}


def get_copy(key: str) -> AdaptiveAssessmentCopy:
    """Return a copy entry or raise ``KeyError``."""
    if key not in _BY_KEY:
        raise KeyError(f"unknown Adaptive Assessment copy key: {key}")
    return _BY_KEY[key]


def iter_copy_entries() -> tuple[AdaptiveAssessmentCopy, ...]:
    """Return all registered copy entries in definition order."""
    return _COPY
