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
        default="Quick check. Helps keep today's plan accurate.",
        description="Entry frame before first item",
    ),
    AdaptiveAssessmentCopy(
        key="session.deep_check.frame",
        default="Careful check on this topic. No grades, clearer next steps.",
        description="Entry frame before first item",
    ),
    AdaptiveAssessmentCopy(
        key="session.recovery_check.frame",
        default="Gentle check to restart accurately. Take your time.",
        description="Entry frame before first item",
    ),
    AdaptiveAssessmentCopy(
        key="session.confidence_check.frame",
        default=(
            "Confidence check. Helps align how sure you feel with what "
            "the evidence shows."
        ),
        description="Entry frame before first item",
    ),
    AdaptiveAssessmentCopy(
        key="session.revision_check.frame",
        default="Revision check. See what still feels solid.",
        description="Entry frame before first item",
    ),
    AdaptiveAssessmentCopy(
        key="session.readiness_check.frame",
        default=(
            "Readiness check. Guides what to study next; it does not "
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
            "This check helps keep today's plan accurate. "
            "Your answers inform what to study next, they are not a grade."
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
        description="Calm progress label: no question numbering",
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
            "Your Quick Check is paused. Resume when you are ready. "
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
            "Some parts may still feel uncertain, that is expected and "
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
    # --- ILE-001C Contextual intent & educational framing ---
    AdaptiveAssessmentCopy(
        key="framing.focus.fallback",
        default="today's focus",
        description="Fallback focus label when none provided",
    ),
    AdaptiveAssessmentCopy(
        key="framing.label.observation",
        default="Observation",
        description="Context / reflection observation heading",
    ),
    AdaptiveAssessmentCopy(
        key="framing.label.meaning",
        default="What this means",
        description="Educational meaning heading",
    ),
    AdaptiveAssessmentCopy(
        key="framing.label.purpose",
        default="Purpose",
        description="Context card purpose heading",
    ),
    AdaptiveAssessmentCopy(
        key="framing.label.benefit",
        default="Expected benefit",
        description="Context card benefit heading",
    ),
    AdaptiveAssessmentCopy(
        key="framing.label.learned",
        default="What you worked on",
        description="Educational summary learned heading",
    ),
    AdaptiveAssessmentCopy(
        key="framing.label.evidence",
        default="Evidence gathered",
        description="Educational summary evidence heading",
    ),
    AdaptiveAssessmentCopy(
        key="framing.label.next",
        default="What happens next",
        description="Educational summary next-step heading",
    ),
    AdaptiveAssessmentCopy(
        key="framing.label.recommendation",
        default="Recommendation",
        description="Recommendation frame headline label",
    ),
    AdaptiveAssessmentCopy(
        key="framing.label.reason",
        default="Reason",
        description="Recommendation reason heading",
    ),
    AdaptiveAssessmentCopy(
        key="framing.label.supporting_evidence",
        default="Supporting evidence",
        description="Recommendation evidence heading",
    ),
    AdaptiveAssessmentCopy(
        key="framing.label.confidence",
        default="Confidence",
        description="Qualitative confidence heading",
    ),
    AdaptiveAssessmentCopy(
        key="framing.label.expected_outcome",
        default="Expected benefit",
        description="Recommendation expected outcome heading",
    ),
    AdaptiveAssessmentCopy(
        key="framing.label.suggested_action",
        default="Suggested action",
        description="Reflection suggested action heading",
    ),
    AdaptiveAssessmentCopy(
        key="framing.label.student_choice",
        default="Your choice",
        description="Reflection student agency heading",
    ),
    AdaptiveAssessmentCopy(
        key="framing.context.title",
        default="Before you begin",
        description="Context Card title",
    ),
    AdaptiveAssessmentCopy(
        key="framing.context.observation",
        default=(
            "We've noticed your recent work on {focus} suggests a short "
            "review would help before moving forward."
        ),
        description="Context Card observation layer",
    ),
    AdaptiveAssessmentCopy(
        key="framing.context.meaning",
        default=(
            "That usually means understanding is forming, but stability "
            "is not yet clear for {focus}."
        ),
        description="Context Card educational meaning",
    ),
    AdaptiveAssessmentCopy(
        key="framing.context.purpose",
        default=(
            "This Quick Check gathers a little signal so today's Mission "
            "can stay accurate for {focus}."
        ),
        description="Context Card purpose",
    ),
    AdaptiveAssessmentCopy(
        key="framing.context.benefit",
        default=(
            "A clearer signal means more supportive next steps, not a grade."
        ),
        description="Context Card expected benefit",
    ),
    AdaptiveAssessmentCopy(
        key="framing.context.invitation",
        default="It should only take a few minutes. Begin when you are ready.",
        description="Context Card invitation",
    ),
    AdaptiveAssessmentCopy(
        key="framing.context.why_expanded",
        default=(
            "You are seeing this check because today's Mission focus on "
            "{focus} benefits from a short formative signal. Answers guide "
            "practice. They are not a grade."
        ),
        description="Expanded why-am-I-seeing-this on Context Card",
    ),
    AdaptiveAssessmentCopy(
        key="framing.summary.title",
        default="Educational summary",
        description="Educational Summary title",
    ),
    AdaptiveAssessmentCopy(
        key="framing.summary.learned",
        default=(
            "You spent a moment checking how {focus} is settling."
        ),
        description="What was learned (activity framing)",
    ),
    AdaptiveAssessmentCopy(
        key="framing.summary.evidence",
        default=(
            "We collected short formative signals about what feels clear "
            "and what still needs practice."
        ),
        description="What evidence was collected",
    ),
    AdaptiveAssessmentCopy(
        key="framing.summary.meaning",
        default=(
            "That helps today's Mission stay aligned with how the ideas "
            "are landing for you."
        ),
        description="What this means educationally",
    ),
    AdaptiveAssessmentCopy(
        key="framing.summary.next",
        default=(
            "Continue with your Mission. You can revisit anything that "
            "still feels unclear."
        ),
        description="What happens next",
    ),
    AdaptiveAssessmentCopy(
        key="framing.recommendation.continue_mission",
        default="Continue with {focus}.",
        description="Primary recommendation when guidance is warranted",
    ),
    AdaptiveAssessmentCopy(
        key="framing.recommendation.hold",
        default=(
            "Hold a firm next-step suggestion until we have clearer evidence."
        ),
        description="Recommendation when evidence is insufficient",
    ),
    AdaptiveAssessmentCopy(
        key="framing.recommendation.reason.insufficient",
        default=(
            "There is not enough recent evidence yet to justify a firm "
            "learning recommendation."
        ),
        description="Reason when insufficient",
    ),
    AdaptiveAssessmentCopy(
        key="framing.recommendation.reason.observation_only",
        default=(
            "We are still gathering signals on {focus}; interpretation "
            "would overclaim."
        ),
        description="Reason when observation-only",
    ),
    AdaptiveAssessmentCopy(
        key="framing.recommendation.reason.emerging",
        default=(
            "Early signals suggest continuing with {focus} is useful. "
            "still provisional."
        ),
        description="Reason when emerging",
    ),
    AdaptiveAssessmentCopy(
        key="framing.recommendation.reason.reliable",
        default=(
            "Recent observations indicate stable understanding across "
            "related ideas for {focus}."
        ),
        description="Reason when reliable / high",
    ),
    AdaptiveAssessmentCopy(
        key="framing.recommendation.supporting_evidence",
        default=(
            "Based on today's Mission context and this Quick Check on {focus}."
        ),
        description="Supporting evidence (presentation, non-technical)",
    ),
    AdaptiveAssessmentCopy(
        key="framing.recommendation.expected_outcome",
        default="Maintains learning momentum without overclaiming certainty.",
        description="Expected benefit of accepting guidance",
    ),
    AdaptiveAssessmentCopy(
        key="framing.recommendation.why_label",
        default="Why this recommendation?",
        description="Decision transparency expand control",
    ),
    AdaptiveAssessmentCopy(
        key="framing.recommendation.why_body",
        default=(
            "The suggestion follows from today's Mission focus on {focus} "
            "and the evidence gathered in this check. It is guidance only. "
            "you remain responsible for significant learning decisions."
        ),
        description="Expanded educational reasoning (no algorithms)",
    ),
    AdaptiveAssessmentCopy(
        key="framing.recommendation.accept",
        default="Continue with this suggestion",
        description="Accept recommendation CTA",
    ),
    AdaptiveAssessmentCopy(
        key="framing.recommendation.defer",
        default="Decide later",
        description="Defer recommendation CTA",
    ),
    AdaptiveAssessmentCopy(
        key="framing.recommendation.guidance_note",
        default="Recommendations are guidance only.",
        description="Agency reminder under recommendation",
    ),
    AdaptiveAssessmentCopy(
        key="framing.confidence.insufficient",
        default="Not enough yet",
        description="Confidence label: insufficient",
    ),
    AdaptiveAssessmentCopy(
        key="framing.confidence.observation_only",
        default="Still gathering",
        description="Confidence label: observation only",
    ),
    AdaptiveAssessmentCopy(
        key="framing.confidence.emerging",
        default="Emerging",
        description="Confidence label: emerging",
    ),
    AdaptiveAssessmentCopy(
        key="framing.confidence.reliable",
        default="Reliable",
        description="Confidence label: reliable",
    ),
    AdaptiveAssessmentCopy(
        key="framing.confidence.high",
        default="Strong",
        description="Confidence label: high (never certainty)",
    ),
    AdaptiveAssessmentCopy(
        key="framing.uncertainty.insufficient",
        default=(
            "There isn't enough evidence yet to confidently suggest a "
            "next step."
        ),
        description="Uncertainty when insufficient",
    ),
    AdaptiveAssessmentCopy(
        key="framing.uncertainty.observation_only",
        default=(
            "We'd like to observe one more session before making a "
            "recommendation."
        ),
        description="Uncertainty when observation-only",
    ),
    AdaptiveAssessmentCopy(
        key="framing.uncertainty.emerging",
        default=(
            "Evidence is limited; treat this as a gentle suggestion."
        ),
        description="Uncertainty when emerging",
    ),
    AdaptiveAssessmentCopy(
        key="framing.uncertainty.reliable",
        default=(
            "Evidence supports this step; some uncertainty always remains."
        ),
        description="Brief residual uncertainty when reliable",
    ),
    AdaptiveAssessmentCopy(
        key="framing.reflection.title",
        default="A moment to reflect",
        description="Framed reflection title",
    ),
    AdaptiveAssessmentCopy(
        key="framing.reflection.observation",
        default="You have just completed a short check on {focus}.",
        description="Reflection observation",
    ),
    AdaptiveAssessmentCopy(
        key="framing.reflection.meaning",
        default=(
            "Reflection helps separate what feels solid from what still "
            "needs practice."
        ),
        description="Reflection meaning",
    ),
    AdaptiveAssessmentCopy(
        key="framing.reflection.suggested_action",
        default=(
            "Continue Learning within today's Mission is a calm next step."
        ),
        description="Reflection suggested action",
    ),
    AdaptiveAssessmentCopy(
        key="framing.reflection.student_choice",
        default=(
            "You choose what to do next. Recommendations are guidance only."
        ),
        description="Reflection student choice prompt",
    ),
    AdaptiveAssessmentCopy(
        key="framing.reflection.choice_accept",
        default="Accept suggestion",
        description="Reflection choice: accept",
    ),
    AdaptiveAssessmentCopy(
        key="framing.reflection.choice_defer",
        default="Decide later",
        description="Reflection choice: defer",
    ),
    AdaptiveAssessmentCopy(
        key="framing.reflection.choice_own",
        default="Continue in my own way",
        description="Reflection choice: own path",
    ),
    AdaptiveAssessmentCopy(
        key="a11y.framing.why_recommendation",
        default="Explain why this recommendation is shown",
        description="Accessible name for why-recommendation control",
    ),
    AdaptiveAssessmentCopy(
        key="a11y.framing.context_card",
        default="Educational context before this learning check",
        description="Accessible label for Context Card region",
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
