"""Student-facing microcopy & identity helpers (PX-005 / PX-006).

Presentation only. Does not change educational packages, selection, Twin,
or Runtime authority. Founder gates D-EOS / D-IDENTITY recorded as provisional
in PX005 evidence until ratification. PX-006 adds performance/moments craft.
"""

from __future__ import annotations

from dataclasses import dataclass

# ── PX-B-038 / D-EOS (provisional) ──────────────────────────────────────────
# Retire "Education Operating System" on student paths. Single-source descriptor
# lives in brand_identity.PRODUCT_DESCRIPTOR; this module owns session/help/
# return/exam framing strings that are not brand constants.

# ── PX-B-040 — Session terminology ──────────────────────────────────────────
PRACTICE_RESULTS_EYEBROW = "Practice results"
PRACTICE_RESULTS_TITLE = "How did practice go?"
PRACTICE_RESULTS_PAGE_TITLE = "Practice results"
SESSION_FEEDBACK_EYEBROW = "Today's sitting"
SESSION_FEEDBACK_TITLE = "What happened today"

# ── PX-B-041 — Reflection value framing ─────────────────────────────────────
REFLECTION_VALUE_TITLE = "A moment to reflect"
REFLECTION_VALUE_FRAMING = (
    "Reflection helps separate what feels solid from what still needs practice. "
    "A short note is enough — skipping does not penalise you."
)
REFLECTION_ACTIVITY_LABEL = "Session reflection"
REFLECTION_EXPECTED_LABEL = "Capture what mattered in this sitting"

# ── PX-B-039 / D-IDENTITY (provisional) ─────────────────────────────────────
STUDENT_RELEASE_LABEL = "Private Beta"
STUDENT_WELCOME_TITLE = "New to Kwalitec?"
STUDENT_SUPPORT_TEAM = "the Kwalitec team"

# ── PX-B-042 — Help Centre ──────────────────────────────────────────────────
HELP_CENTRE_EYEBROW = "Help"
HELP_CENTRE_DESCRIPTION = (
    "How Kwalitec and Study Sensei work together on your educational journey — "
    "and how to get support when you need it."
)
HELP_FEEDBACK_CTA = "Send product feedback"

# ── PX-007 / WS-11 — Feedback identity (student-visible; close PX7-001/002) ──
FEEDBACK_RELEASE_EYEBROW = STUDENT_RELEASE_LABEL  # Private Beta — not Closed Beta
FEEDBACK_THANKS_FLASH = (
    "Thank you — your feedback helps improve Kwalitec during Private Beta."
)
FEEDBACK_SUGGEST_DESCRIPTION = (
    "Share one concrete idea that would make Kwalitec better for studying."
)
FEEDBACK_QUICK_DESCRIPTION = (
    "One quick answer helps improve Kwalitec for students like you."
)

# Extra FAQ rows (deferral / exam change) appended to Help popular topics.
HELP_FAQ_EXAM_CHANGE = (
    "How do I change my exam date or sitting?",
    "Open Study Plan from the main navigation and update your exam date. "
    "Your next Session updates from the revised plan — you do not need to "
    "rebuild your journey from scratch.",
)
HELP_FAQ_DEFERRAL = (
    "What if I need to pause or defer my studies?",
    "Take the break you need. When you return, open Home and follow today's "
    "authorised Session — Kwalitec does not invent catch-up work or penalise "
    "gaps. If your exam sitting changes, update Study Plan so guidance stays "
    "honest.",
)

# ── PX-B-043 — Diagnostic disclosure ────────────────────────────────────────
DIAGNOSTIC_SUMMARY = "Build information for support"
DIAGNOSTIC_SUPPORT_HINT = (
    "Share these details only if support asks — they are not part of studying."
)

# ── PX-B-008 — Continue Session contention ──────────────────────────────────
CONTINUE_CONTENTION_MESSAGE = (
    "Your session is still open. Wait a moment, then try Continue again — "
    "this is a temporary hiccup, not a study failure."
)
CONTINUE_RETRY_MESSAGE = (
    "We couldn't open your session just now. Your progress is safe — "
    "return to Home and tap Continue when you're ready."
)

# ── PX-B-009 — Honest wait / preparing ──────────────────────────────────────
PREPARING_MISSION_LABEL = "Preparing today's session…"
PREPARING_MISSION_SUPPORT = (
    "Your campaign journey is settling. This usually takes a moment — "
    "stay on this page or refresh shortly."
)

# ── PX-006 / WS-09 — Loading / skeleton coherence ───────────────────────────
SKELETON_MISSION_LABEL = "Opening today's session…"
SKELETON_PLAN_LABEL = "Loading your study plan…"
SKELETON_NAV_LABEL = "Loading…"

# ── PX-006 / WS-10 — Error Reference ID (PX-B-020) ──────────────────────────
ERROR_REFERENCE_LABEL = "Reference ID"
ERROR_REFERENCE_GUIDANCE = (
    "Copy this ID if you contact support or use Report a problem — "
    "it helps us find what went wrong."
)

# ── PX-006 / WS-10 — Session-complete celebration (PX-B-022) ─────────────────
SESSION_COMPLETE_SUPPORT = (
    "Well done for finishing today's sitting. Your progress is saved — "
    "return tomorrow for the next authorised step."
)
SESSION_COMPLETE_HISTORY_LINK = "Your session is saved in History"

# ── PX-006 / WS-10 — Preference stickiness (PX-B-049) ───────────────────────
PREFERENCE_APPEARANCE_STICKY = (
    "Choose Light, Dark, or System. System follows your device. "
    "Your choice is saved in this browser."
)
PREFERENCE_STUDY_SESSION_SCOPE = (
    "Saved for this signed-in session on this device. "
    "Account-wide study goals are not yet durable across browsers."
)
PREFERENCE_SAVED_LIVE = "Appearance saved"

# ── PX-006 / WS-10 — Continuity Front milestones (PX-B-046) ─────────────────
CF_MILESTONE_ACK_CONTINUITY = (
    "Continuity Front sitting complete — a steady step on your certified arc. "
    "Follow tomorrow's authorised session when you're ready."
)
CF_MILESTONE_ACK_MEMORY = (
    "Memory Front sitting complete — retrieval practice locked in. "
    "Tomorrow's authorised session continues the arc."
)
CF_MILESTONE_ACK_PUBLICATION = (
    "Publication Front sitting complete — another certified day behind you. "
    "Stay with tomorrow's authorised session."
)
CF_MILESTONE_ACK_GENERIC = (
    "Today's certified sitting is complete. "
    "Return tomorrow for the next authorised step — no pass promises, just progress."
)

# ── PX-006 / WS-10 — Diligence without punishment (PX-B-047) ────────────────
DILIGENCE_EMPTY_STREAK = "Study rhythm builds as you show up"
DILIGENCE_STREAK_LABEL = "Recent study rhythm"


@dataclass(frozen=True, slots=True)
class ReturnAfterGapCopy:
    """Calm welcome-back framing (PX-B-044). Authorised next action only."""

    greeting: str
    support_line: str | None = None


def return_after_gap_copy(
    *,
    days_since_last: int | None,
    display_name: str | None = None,
    in_progress: bool = False,
) -> ReturnAfterGapCopy:
    """Welcome-back microcopy without guilt or invented catch-up work."""
    name = (display_name or "").strip()
    hello = f"Welcome back, {name}." if name else "Welcome back."

    if in_progress:
        return ReturnAfterGapCopy(
            greeting=hello,
            support_line="You left a sitting open — continue when you're ready.",
        )
    if days_since_last is None or days_since_last <= 0:
        return ReturnAfterGapCopy(greeting=hello)
    if days_since_last == 1:
        return ReturnAfterGapCopy(
            greeting=hello,
            support_line="Pick up today's authorised session when you're ready.",
        )
    if days_since_last <= 7:
        return ReturnAfterGapCopy(
            greeting=hello,
            support_line=(
                "Good to see you again. Today's session is ready — "
                "no catch-up invented, just the next honest step."
            ),
        )
    return ReturnAfterGapCopy(
        greeting=hello,
        support_line=(
            "Welcome back whenever you are. Follow today's authorised session — "
            "gaps are normal; we do not invent catch-up work."
        ),
    )


@dataclass(frozen=True, slots=True)
class ExamHorizonCopy:
    """Calm near-exam framing (PX-B-045). No panic theatre."""

    tier: str
    support_line: str | None


def exam_horizon_copy(days_to_exam: int | None) -> ExamHorizonCopy | None:
    """Return calm support framing near the exam horizon, or None if distant."""
    if days_to_exam is None:
        return None
    if days_to_exam < 0:
        return ExamHorizonCopy(
            tier="past",
            support_line="Stay with today's authorised session.",
        )
    if days_to_exam == 0:
        return ExamHorizonCopy(
            tier="today",
            support_line=(
                "Exam day — keep today's session calm and focused. "
                "Follow the authorised next step only."
            ),
        )
    if days_to_exam == 1:
        return ExamHorizonCopy(
            tier="imminent",
            support_line=(
                "One day to go. Stay with today's authorised session — "
                "steady beats frantic."
            ),
        )
    if days_to_exam <= 7:
        return ExamHorizonCopy(
            tier="week",
            support_line=(
                "Exam week. Keep to today's authorised session — "
                "calm consistency over last-minute overload."
            ),
        )
    if days_to_exam <= 21:
        return ExamHorizonCopy(
            tier="approach",
            support_line=(
                "Exam approaching. Today's authorised session is enough — "
                "trust the plan."
            ),
        )
    return None


def continuity_front_milestone_ack(mission_title: str | None) -> str | None:
    """Light arc acknowledgement for day-complete Home (PX-B-046).

    Presentation only — never implies until-exam pass. Matches package/title
    chrome already shown; does not invent educational authority.
    """
    text = (mission_title or "").casefold()
    if not text:
        return None
    if "publication front" in text or text.startswith("cr-") or " cr-" in text:
        return CF_MILESTONE_ACK_PUBLICATION
    if "memory front" in text or text.startswith("cp-") or " cp-" in text:
        return CF_MILESTONE_ACK_MEMORY
    if (
        "continuity front" in text
        or text.startswith("co-")
        or " co-" in text
        or "cf-" in text
    ):
        return CF_MILESTONE_ACK_CONTINUITY
    return None


@dataclass(frozen=True, slots=True)
class DiligenceCopy:
    """Calm diligence reinforcement (PX-B-047). Gaps do not destroy narrative."""

    support_line: str | None = None
    streak_empty_label: str = DILIGENCE_EMPTY_STREAK


def diligence_reinforcement_copy(
    *,
    days_since_last: int | None,
    streak_days: int | None = None,
) -> DiligenceCopy:
    """Optional gentle reinforcement — never punishes gaps or invents catch-up."""
    if streak_days is not None and streak_days <= 0:
        return DiligenceCopy(
            support_line=(
                "Showing up for today's authorised session is enough — "
                "rhythm builds without pressure."
            ),
            streak_empty_label=DILIGENCE_EMPTY_STREAK,
        )
    if days_since_last is not None and days_since_last >= 3:
        return DiligenceCopy(
            support_line=(
                "Consistency returns one sitting at a time — "
                "today's authorised session is the next honest step."
            ),
        )
    if days_since_last is not None and 0 < days_since_last <= 2:
        return DiligenceCopy(
            support_line="Steady sittings compound — keep today's session calm.",
        )
    return DiligenceCopy()
