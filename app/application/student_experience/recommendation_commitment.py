"""Recommendation Commitment & Follow-through (EP-008.3A).

Preference / intent commitment layer only. Does not change Runtime A ranking,
PlanningService, ReadinessService, or educational reasoning.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any

from app.application.student_experience.dto.commitment_reflection_snapshot import (
    CommitmentReflectionSnapshot,
)
from app.application.student_experience.dto.recommendation_commitment_snapshot import (
    RecommendationCommitmentSnapshot,
)
from app.application.student_experience.dto.recommendation_narrative_entry_snapshot import (  # noqa: E501
    RecommendationNarrativeEntrySnapshot,
)
from app.application.student_experience.ports.commitment_port import (
    CommitmentPersistencePort,
    CommitmentRecord,
    DecisionJournalPort,
    LearningFeedbackPort,
    get_commitment_persistence_port,
    get_decision_journal_port,
    get_learning_feedback_port,
)
from app.domain.student_experience.recommendation_explanation import (
    translate_to_student_language,
)

logger = logging.getLogger(__name__)

# Learning-feedback claim boundaries / source authority (mirrors the
# infrastructure contract constants without importing infrastructure here).
_CLAIM_PREFERENCE_JOURNAL = "preference_journal"
_CLAIM_OBSERVED_BEHAVIOUR = "observed_behaviour"
_SOURCE_RECOMMENDATION = "recommendation_service"

# Commitment states (ENGINEERING_DESIGN §6.1).
STATE_OFFERED = "offered"
STATE_COMMITTED = "committed"
STATE_IN_SESSION = "in_session"
STATE_COMPLETED = "completed"
STATE_REFLECTED = "reflected"
STATE_DEFERRED = "deferred"
STATE_REFUSAL = "refusal"

ACTIVE_COMMIT_STATES = frozenset(
    {STATE_COMMITTED, STATE_IN_SESSION, STATE_COMPLETED}
)
NARRATIVE_CAP = 10
NARRATIVE_DAYS = 14

# Plan continuity copy bank (UI_SPEC §9).
CONTINUITY_COMMIT = "This is part of your continuous study plan."
CONTINUITY_DEFER = (
    "Your study plan continues — we'll meet you when you're ready."
)
CONTINUITY_REFLECTION = (
    "Tomorrow's Mission will reflect tonight's work as part of the same plan."
)
CONTINUITY_HISTORY_HEADER = "Choices you've made inside one study plan."

# Humble static frame — never personal-model theatre (Design §6.4).
WHAT_WAS_LEARNED_HUMBLE = (
    "Tonight's practice updates the educational state that shapes "
    "tomorrow's Mission."
)

# Defer catalogue (Design §6.3) — student-safe labels only.
DEFER_CATALOGUE: tuple[tuple[str, str], ...] = (
    ("not_enough_time", "Not enough time"),
    ("need_prerequisite", "Need a prerequisite first"),
    ("studying_elsewhere", "Already studying elsewhere"),
    ("not_today", "Not today"),
    ("other", "Something else"),
)
DEFER_LABELS: dict[str, str] = dict(DEFER_CATALOGUE)
DEFER_CODES: frozenset[str] = frozenset(DEFER_LABELS)

# Forbidden shame / streak / gamification strings (CF-A04).
FORBIDDEN_SHAME_SUBSTRINGS: tuple[str, ...] = (
    "hurt your readiness",
    "top students never",
    "broke your streak",
    "streak",
    "you fell behind",
    "points",
    "badge",
    "accept ai",
    "the ai learned",
)


def continuity_line_for(moment: str) -> str:
    """Return canonical continuity copy for a commitment moment."""
    key = (moment or "").strip().lower()
    if key == "commit":
        return CONTINUITY_COMMIT
    if key == "defer":
        return CONTINUITY_DEFER
    if key == "reflection":
        return CONTINUITY_REFLECTION
    if key == "history":
        return CONTINUITY_HISTORY_HEADER
    return CONTINUITY_COMMIT


def defer_reason_label(code: str) -> str:
    """Map defer catalogue code to student-safe label (never raw enum in UI)."""
    return DEFER_LABELS.get((code or "").strip().lower(), "")


def recommendation_key_from_tip(tip: dict[str, Any] | None) -> str:
    """Stable preference key from authored tip — not a new ranking id."""
    if not tip:
        return ""
    title = str(tip.get("title") or tip.get("topic_title") or "").strip()
    generated = tip.get("generated_at") or tip.get("decision_id") or ""
    if hasattr(generated, "isoformat"):
        generated = generated.isoformat()
    generated_s = str(generated).strip()
    if title and generated_s:
        return f"{title}|{generated_s}"[:255]
    if title:
        return title[:255]
    return ""


def compose_reflection(
    *,
    title: str = "",
    review_point: str = "",
    expected_benefit: str = "",
    suggested_next_action: str = "",
    session_topic: str = "",
) -> CommitmentReflectionSnapshot:
    """Compose reflection from authored MES + session facts — no LLM / Twin."""
    did = translate_to_student_language(title or session_topic or "today's session")
    changed = translate_to_student_language(review_point) or (
        "Your completed practice is now part of tonight's study record."
    )
    mattered = translate_to_student_language(expected_benefit) or (
        "Focused practice on tonight's priority."
    )
    next_line = translate_to_student_language(suggested_next_action) or (
        "Return Home for the next Mission in your continuous study plan."
    )
    return CommitmentReflectionSnapshot(
        what_you_did=f"Completed: {did}" if did else "Completed today's session.",
        what_changed=changed,
        why_it_mattered=mattered,
        what_was_learned=WHAT_WAS_LEARNED_HUMBLE,
        what_happens_next=next_line,
    )


def empty_commitment_snapshot(
    *,
    trust_state: str = "",
    has_schema_complete_tip: bool = False,
    title: str = "",
    recommendation_key: str = "",
) -> RecommendationCommitmentSnapshot:
    """C0 offered (or refusal) when no persisted commitment exists."""
    refusal = (trust_state or "").strip().lower() == "refusal"
    if refusal:
        return RecommendationCommitmentSnapshot(
            state=STATE_REFUSAL,
            recommendation_key=recommendation_key,
            title=title,
            continuity_line="",
            show_commit_affordance=False,
            show_defer_affordance=False,
        )
    show = bool(has_schema_complete_tip and title)
    return RecommendationCommitmentSnapshot(
        state=STATE_OFFERED,
        recommendation_key=recommendation_key,
        title=title,
        continuity_line=CONTINUITY_COMMIT if show else "",
        show_commit_affordance=show,
        show_defer_affordance=show,
    )


def _emit_observational(
    *,
    user_id: int,
    event_type: str,
    payload: dict[str, Any],
    feedback_port: LearningFeedbackPort | None = None,
) -> None:
    """Research-only learning-feedback emit (fail-open). Never raises."""
    try:
        port = feedback_port or get_learning_feedback_port()
        if port is None:
            return
        claim = (
            _CLAIM_PREFERENCE_JOURNAL
            if event_type
            in {
                "commitment_confirmed",
                "commitment_deferred",
                "commitment_completed",
            }
            else _CLAIM_OBSERVED_BEHAVIOUR
        )
        port.emit(
            student_id=user_id,
            event_type=event_type,
            source_authority=_SOURCE_RECOMMENDATION,
            claim_boundary=claim,
            payload=payload,
        )
    except Exception:  # noqa: BLE001 — observational path must not break UX
        logger.warning(
            "commitment_observational_emit_failed user_id=%s event=%s",
            user_id,
            event_type,
            exc_info=True,
        )


def _tip_for_decision(tip: dict[str, Any]) -> dict[str, Any]:
    """Build the minimal dict ``record_decision`` requires."""
    generated = tip.get("generated_at") or datetime.utcnow()
    if isinstance(generated, str):
        try:
            generated = datetime.fromisoformat(generated.replace("Z", "+00:00"))
        except ValueError:
            generated = datetime.utcnow()
    return {
        "title": str(tip.get("title") or tip.get("topic_title") or "Recommendation"),
        "category": str(tip.get("category") or "Study"),
        "priority": str(tip.get("priority") or "Medium"),
        "reason": str(
            tip.get("reason")
            or tip.get("why_recommended")
            or tip.get("summary")
            or ""
        ),
        "expected_benefit": str(tip.get("expected_benefit") or ""),
        "generated_at": generated,
    }


class RecommendationCommitmentService:
    """Commit / defer / complete / reflect — preference journal only."""

    @staticmethod
    def snapshot_for_home(
        user_id: int,
        *,
        tip: dict[str, Any] | None = None,
        trust_state: str = "",
        schema_complete: bool = False,
    ) -> RecommendationCommitmentSnapshot:
        """Load current commitment chrome for Home."""
        tip = tip or {}
        title = translate_to_student_language(
            str(tip.get("title") or tip.get("topic_title") or "")
        )
        key = recommendation_key_from_tip(tip)
        refusal = (trust_state or "").strip().lower() == "refusal"
        if refusal:
            return empty_commitment_snapshot(
                trust_state="refusal",
                title=title,
                recommendation_key=key,
            )

        row = RecommendationCommitmentService._active_row(user_id, key)
        if row is None:
            return empty_commitment_snapshot(
                has_schema_complete_tip=schema_complete,
                title=title,
                recommendation_key=key,
            )

        reflection = None
        continuity = CONTINUITY_COMMIT
        if row.state == STATE_DEFERRED:
            continuity = CONTINUITY_DEFER
        elif row.state in {STATE_COMPLETED, STATE_REFLECTED}:
            continuity = CONTINUITY_REFLECTION
            reflection = compose_reflection(
                title=row.title,
                review_point=row.review_point,
                expected_benefit=row.expected_benefit,
                suggested_next_action=row.suggested_next_action,
            )

        show_commit = False
        show_defer = row.state in {
            STATE_OFFERED,
            STATE_COMMITTED,
            STATE_IN_SESSION,
        }
        if row.state == STATE_DEFERRED:
            show_commit = schema_complete  # optional restore
            show_defer = False
        elif row.state == STATE_OFFERED:
            show_commit = schema_complete
            show_defer = schema_complete

        return RecommendationCommitmentSnapshot(
            state=row.state,
            recommendation_key=row.recommendation_key,
            title=row.title or title,
            committed_at=(
                row.committed_at.isoformat() if row.committed_at else ""
            ),
            deferred_reason_code=row.deferred_reason_code or "",
            deferred_reason_label=defer_reason_label(row.deferred_reason_code),
            continuity_line=continuity,
            reflection=reflection,
            show_commit_affordance=show_commit,
            show_defer_affordance=show_defer,
        )

    @staticmethod
    def confirm_commitment(
        user_id: int,
        tip: dict[str, Any],
        *,
        session_id: str | None = None,
    ) -> RecommendationCommitmentSnapshot:
        """Record C1 (or C2 if session already starting). Preference only."""
        tip = dict(tip or {})
        key = recommendation_key_from_tip(tip)
        title = translate_to_student_language(
            str(tip.get("title") or tip.get("topic_title") or "")
        )
        if not key or not title:
            return empty_commitment_snapshot()

        now = datetime.utcnow()
        row = RecommendationCommitmentService._active_row(user_id, key)
        if row is None:
            row = RecommendationCommitmentService._new_record(
                user_id=user_id,
                tip=tip,
                key=key,
                title=title,
            )

        if row.state in {STATE_COMPLETED, STATE_REFLECTED}:
            return RecommendationCommitmentService.snapshot_for_home(
                user_id, tip=tip, schema_complete=True
            )

        row.state = STATE_IN_SESSION if session_id else STATE_COMMITTED
        row.committed_at = row.committed_at or now
        row.title = title
        row.expected_benefit = str(tip.get("expected_benefit") or "")
        row.review_point = str(tip.get("review_point") or "")
        row.suggested_next_action = str(
            tip.get("suggested_next_action") or tip.get("next_action") or ""
        )
        if session_id:
            row.session_id = str(session_id)
            row.session_started_at = row.session_started_at or now
        row.deferred_reason_code = ""
        row.deferred_reason_note = ""

        decision_id = RecommendationCommitmentService._record_decision(
            user_id, tip, accepted=True, completed=False
        )
        if decision_id is not None:
            row.decision_id = decision_id

        RecommendationCommitmentService._persistence().save(row)
        _emit_observational(
            user_id=user_id,
            event_type="commitment_confirmed",
            payload={
                "recommendation_title": title[:255],
                "recommendation_key": key[:255],
                "state": row.state,
            },
        )
        return RecommendationCommitmentService.snapshot_for_home(
            user_id, tip=tip, schema_complete=True
        )

    @staticmethod
    def defer_commitment(
        user_id: int,
        tip: dict[str, Any],
        *,
        reason_code: str,
        reason_note: str = "",
    ) -> RecommendationCommitmentSnapshot:
        """Record D1 honest deferral — never punishment, never re-rank."""
        tip = dict(tip or {})
        code = (reason_code or "").strip().lower()
        if code not in DEFER_CODES:
            code = "not_today"
        note = (reason_note or "").strip()[:140] if code == "other" else ""
        key = recommendation_key_from_tip(tip)
        title = translate_to_student_language(
            str(tip.get("title") or tip.get("topic_title") or "")
        )
        if not key:
            return empty_commitment_snapshot(
                has_schema_complete_tip=False, title=title
            )

        now = datetime.utcnow()
        row = RecommendationCommitmentService._active_row(user_id, key)
        if row is None:
            row = RecommendationCommitmentService._new_record(
                user_id=user_id,
                tip=tip,
                key=key,
                title=title,
            )

        row.state = STATE_DEFERRED
        row.deferred_at = now
        row.deferred_reason_code = code
        row.deferred_reason_note = note
        row.title = title or row.title

        outcome = f"deferred:{code}"
        if note:
            outcome = f"{outcome}:{note}"
        decision_id = RecommendationCommitmentService._record_decision(
            user_id,
            tip,
            accepted=False,
            completed=False,
            outcome_summary=outcome[:500],
        )
        if decision_id is not None:
            row.decision_id = decision_id

        RecommendationCommitmentService._persistence().save(row)
        _emit_observational(
            user_id=user_id,
            event_type="commitment_deferred",
            payload={
                "recommendation_title": (title or row.title)[:255],
                "recommendation_key": key[:255],
                "deferred_reason_code": code,
            },
        )
        return RecommendationCommitmentService.snapshot_for_home(
            user_id, tip=tip, schema_complete=True
        )

    @staticmethod
    def mark_session_started(
        user_id: int,
        *,
        tip: dict[str, Any] | None = None,
        session_id: str | None = None,
    ) -> None:
        """Advance C1 → C2 when a session starts from a committed tip."""
        tip = tip or {}
        key = recommendation_key_from_tip(tip)
        row = RecommendationCommitmentService._active_row(user_id, key)
        if row is None:
            return
        if row.state not in {STATE_COMMITTED, STATE_IN_SESSION}:
            return
        row.state = STATE_IN_SESSION
        if session_id:
            row.session_id = str(session_id)
        row.session_started_at = row.session_started_at or datetime.utcnow()
        RecommendationCommitmentService._persistence().save(row)

    @staticmethod
    def mark_completed(
        user_id: int,
        *,
        tip: dict[str, Any] | None = None,
        session_id: str | None = None,
        session_topic: str = "",
    ) -> RecommendationCommitmentSnapshot | None:
        """Advance to C3 and compose reflection. Preference + observation only."""
        tip = tip or {}
        key = recommendation_key_from_tip(tip)
        row = None
        if key:
            row = RecommendationCommitmentService._active_row(user_id, key)
        persistence = RecommendationCommitmentService._persistence()

        if row is None and session_id:
            row = persistence.find_by_session(user_id, str(session_id))
        if row is None:
            # Complete the most recent open commitment for the user.
            row = persistence.find_latest_open(user_id)
        if row is None:
            return None

        now = datetime.utcnow()
        row.state = STATE_COMPLETED
        row.completed_at = now
        if session_id:
            row.session_id = str(session_id)
        if session_topic and not row.title:
            row.title = translate_to_student_language(session_topic)

        tip_payload = tip or {
            "title": row.title,
            "category": "Study",
            "priority": "Medium",
            "reason": "",
            "expected_benefit": row.expected_benefit,
            "generated_at": row.committed_at or now,
        }
        RecommendationCommitmentService._record_decision(
            user_id,
            tip_payload,
            accepted=True,
            completed=True,
            outcome_summary="commitment_completed",
        )
        RecommendationCommitmentService._persistence().save(row)
        _emit_observational(
            user_id=user_id,
            event_type="commitment_completed",
            payload={
                "recommendation_title": (row.title or "")[:255],
                "recommendation_key": (row.recommendation_key or "")[:255],
            },
        )
        return RecommendationCommitmentService.snapshot_for_home(
            user_id,
            tip=tip_payload,
            schema_complete=True,
        )

    @staticmethod
    def acknowledge_reflection(
        user_id: int,
        *,
        recommendation_key: str = "",
    ) -> RecommendationCommitmentSnapshot | None:
        """Advance C3 → C4 (observational reflection_viewed)."""
        row = None
        if recommendation_key:
            row = RecommendationCommitmentService._active_row(
                user_id, recommendation_key
            )
        if row is None:
            row = RecommendationCommitmentService._persistence().find_latest_completed(
                user_id
            )
        if row is None:
            return None
        row.state = STATE_REFLECTED
        row.reflected_at = datetime.utcnow()
        RecommendationCommitmentService._persistence().save(row)
        _emit_observational(
            user_id=user_id,
            event_type="reflection_viewed",
            payload={
                "recommendation_title": (row.title or "")[:255],
                "recommendation_key": (row.recommendation_key or "")[:255],
            },
        )
        return RecommendationCommitmentSnapshot(
            state=STATE_REFLECTED,
            recommendation_key=row.recommendation_key,
            title=row.title,
            committed_at=(
                row.committed_at.isoformat() if row.committed_at else ""
            ),
            continuity_line=CONTINUITY_REFLECTION,
            reflection=compose_reflection(
                title=row.title,
                review_point=row.review_point,
                expected_benefit=row.expected_benefit,
                suggested_next_action=row.suggested_next_action,
            ),
            show_commit_affordance=False,
            show_defer_affordance=False,
        )

    @staticmethod
    def narrative_entries(
        user_id: int,
        *,
        limit: int = NARRATIVE_CAP,
        within_days: int = NARRATIVE_DAYS,
    ) -> tuple[RecommendationNarrativeEntrySnapshot, ...]:
        """Lightweight educational narrative (≤10 / ~14 days)."""
        since = datetime.utcnow() - timedelta(days=max(1, within_days))
        rows = RecommendationCommitmentService._persistence().find_recent(
            user_id,
            since=since,
            states=(
                STATE_COMPLETED,
                STATE_REFLECTED,
                STATE_DEFERRED,
                STATE_COMMITTED,
                STATE_IN_SESSION,
            ),
            limit=max(1, limit),
        )
        entries: list[RecommendationNarrativeEntrySnapshot] = []
        for row in rows:
            kind, summary, occurred, reason = (
                RecommendationCommitmentService._narrative_bits(row)
            )
            if not kind:
                continue
            entries.append(
                RecommendationNarrativeEntrySnapshot(
                    kind=kind,
                    title=row.title or "Study choice",
                    occurred_at=occurred,
                    summary_line=summary,
                    reason_label=reason,
                )
            )
            if len(entries) >= limit:
                break
        return tuple(entries)

    @staticmethod
    def _narrative_bits(
        row: Any,
    ) -> tuple[str, str, str, str]:
        title = row.title or "Study choice"
        if row.state in {STATE_COMPLETED, STATE_REFLECTED}:
            benefit = translate_to_student_language(row.expected_benefit)
            short = benefit[:120] if benefit else "Completed as part of your plan"
            when = row.completed_at or row.updated_at
            return (
                "completed",
                f"Completed · {title} · {short}",
                when.isoformat() if when else "",
                "",
            )
        if row.state == STATE_DEFERRED:
            label = defer_reason_label(row.deferred_reason_code) or "Not today"
            when = row.deferred_at or row.updated_at
            return (
                "deferred",
                f"Deferred · {title} · {label} · plan continues",
                when.isoformat() if when else "",
                label,
            )
        if row.state in {STATE_COMMITTED, STATE_IN_SESSION}:
            # Optional restorative incomplete entry.
            age = row.committed_at or row.created_at
            if age and age < datetime.utcnow() - timedelta(days=1):
                return (
                    "committed_incomplete",
                    f"Committed · not finished · {title}",
                    age.isoformat(),
                    "",
                )
        return ("", "", "", "")

    @staticmethod
    def _active_row(user_id: int, key: str) -> CommitmentRecord | None:
        if not key:
            return None
        return RecommendationCommitmentService._persistence().find_active(
            user_id, key
        )

    @staticmethod
    def _new_record(
        *,
        user_id: int,
        tip: dict[str, Any],
        key: str,
        title: str,
    ) -> CommitmentRecord:
        return CommitmentRecord(
            user_id=user_id,
            recommendation_key=key,
            title=title,
            state=STATE_OFFERED,
            expected_benefit=str(tip.get("expected_benefit") or ""),
            review_point=str(tip.get("review_point") or ""),
            suggested_next_action=str(
                tip.get("suggested_next_action") or tip.get("next_action") or ""
            ),
        )

    @staticmethod
    def _persistence(
        port: CommitmentPersistencePort | None = None,
    ) -> CommitmentPersistencePort:
        active = port or get_commitment_persistence_port()
        if active is None:
            raise RuntimeError(
                "RecommendationCommitmentService requires a "
                "CommitmentPersistencePort bound via infrastructure composition"
            )
        return active

    @staticmethod
    def _record_decision(
        user_id: int,
        tip: dict[str, Any],
        *,
        accepted: bool,
        completed: bool,
        outcome_summary: str | None = None,
        journal: DecisionJournalPort | None = None,
    ) -> int | None:
        """Call existing Decision Journal API — never edit ranking."""
        try:
            port = journal or get_decision_journal_port()
            if port is None:
                return None
            return port.record_decision(
                user_id,
                _tip_for_decision(tip),
                accepted=accepted,
                completed=completed,
                outcome_summary=outcome_summary,
            )
        except Exception:  # noqa: BLE001 — preference journal fail-open
            logger.warning(
                "commitment_record_decision_failed user_id=%s",
                user_id,
                exc_info=True,
            )
            return None
