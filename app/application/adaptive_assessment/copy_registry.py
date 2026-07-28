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
    # --- ILE-001B Quick Check learner experience ---
    AdaptiveAssessmentCopy(
        key="quick_check.invitation.headline",
        default="Let's strengthen today's understanding.",
        description="Mission entry card invitation line",
    ),
    AdaptiveAssessmentCopy(
        key="quick_check.invitation.cta",
        default="Continue",
        description="Primary Mission entry CTA",
    ),
    AdaptiveAssessmentCopy(
        key="quick_check.invitation.why_this",
        default="Why this?",
        description="Secondary Mission entry explain control",
    ),
    AdaptiveAssessmentCopy(
        key="quick_check.invitation.tutor_available",
        default="Tutor explanation available.",
        description="Tutor availability note on entry card",
    ),
    AdaptiveAssessmentCopy(
        key="quick_check.intro.title",
        default="Why this check?",
        description="Learner introduction headline",
    ),
    AdaptiveAssessmentCopy(
        key="quick_check.intro.begin",
        default="Begin",
        description="Start questions from introduction",
    ),
    AdaptiveAssessmentCopy(
        key="quick_check.progress.making",
        default="Making progress",
        description="Calm progress label — no question numbering",
    ),
    AdaptiveAssessmentCopy(
        key="quick_check.progress.almost",
        default="Almost there",
        description="Calm late-progress label",
    ),
    AdaptiveAssessmentCopy(
        key="quick_check.progress.steady",
        default="Take your time",
        description="Calm early-progress label",
    ),
    AdaptiveAssessmentCopy(
        key="quick_check.hint.label",
        default="Hint",
        description="Hint control label",
    ),
    AdaptiveAssessmentCopy(
        key="quick_check.hint.request",
        default="Show a hint",
        description="Request hint CTA",
    ),
    AdaptiveAssessmentCopy(
        key="quick_check.action.next",
        default="Continue",
        description="Advance to next prompt",
    ),
    AdaptiveAssessmentCopy(
        key="quick_check.action.resume",
        default="Resume",
        description="Resume a paused Quick Check",
    ),
    AdaptiveAssessmentCopy(
        key="quick_check.paused.body",
        default=(
            "Your Quick Check is paused. Resume when you are ready — "
            "there is no rush."
        ),
        description="Pause surface body",
    ),
    AdaptiveAssessmentCopy(
        key="quick_check.reflection.title",
        default="A moment to reflect",
        description="Reflection step headline",
    ),
    AdaptiveAssessmentCopy(
        key="quick_check.reflection.prompt",
        default=(
            "What feels clearer now, and what would you still like to "
            "practise?"
        ),
        description="Reflection prompt",
    ),
    AdaptiveAssessmentCopy(
        key="quick_check.reflection.continue",
        default="Continue",
        description="Leave reflection toward completion",
    ),
    AdaptiveAssessmentCopy(
        key="quick_check.completion.thank_you",
        default="Thank you",
        description="Completion thank-you headline",
    ),
    AdaptiveAssessmentCopy(
        key="quick_check.completion.evidence",
        default=(
            "We gathered useful evidence about how today's ideas are "
            "settling."
        ),
        description="What evidence was collected",
    ),
    AdaptiveAssessmentCopy(
        key="quick_check.completion.uncertain",
        default=(
            "Some parts may still feel uncertain — that is expected and "
            "helps guide practice."
        ),
        description="What remains uncertain",
    ),
    AdaptiveAssessmentCopy(
        key="quick_check.completion.mission_benefit",
        default=(
            "Today's Mission can use this to stay accurate and supportive."
        ),
        description="How today's Mission may benefit",
    ),
    AdaptiveAssessmentCopy(
        key="quick_check.completion.return",
        default="Return to Mission",
        description="Primary return CTA after completion",
    ),
    AdaptiveAssessmentCopy(
        key="quick_check.mission.evidence_ack",
        default="We've gathered useful evidence.",
        description="Mission acknowledgement after Quick Check return",
    ),
    AdaptiveAssessmentCopy(
        key="quick_check.response.prompt",
        default="Your thoughts",
        description="Free-response field label",
    ),
    AdaptiveAssessmentCopy(
        key="a11y.quick_check.pause",
        default="Pause this Quick Check",
        description="Accessible name for pause control",
    ),
    AdaptiveAssessmentCopy(
        key="a11y.quick_check.resume",
        default="Resume this Quick Check",
        description="Accessible name for resume control",
    ),
    AdaptiveAssessmentCopy(
        key="a11y.quick_check.progress",
        default="Quick Check progress",
        description="Accessible name for calm progress indicator",
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
