"""Decision Journal service — learner educational memory (ILE-002).

Records significant educational guidance, evidence at the time, learner
choices, and later outcomes. Preference / narrative only — never mastery,
Twin mutation, or recommendation ranking changes.
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime
from typing import Any

from app.domain.decision_journal import (
    EntryKind,
    JournalLifecycleStatus,
    QualitativeConfidence,
    ReflectionStatus,
    StudentAction,
    assert_student_safe_text,
    can_transition,
)
from app.extensions import db
from app.models.decision_journal import (
    DecisionJournalEntry,
    DecisionJournalEvidenceEvent,
)

logger = logging.getLogger(__name__)

# Student-visible labels (ILE-001C0 / ILE-011 vocabulary).
LIFECYCLE_LABELS: dict[str, str] = {
    JournalLifecycleStatus.RECOMMENDED: "Recommended",
    JournalLifecycleStatus.ACCEPTED: "Accepted",
    JournalLifecycleStatus.DEFERRED: "Deferred",
    JournalLifecycleStatus.EVIDENCE_EVOLVING: "Evidence updated",
    JournalLifecycleStatus.REFLECTED: "Reflected",
    JournalLifecycleStatus.OUTCOME_RECORDED: "Outcome recorded",
    JournalLifecycleStatus.ARCHIVED: "Archived",
}

KIND_LABELS: dict[str, str] = {
    EntryKind.MISSION_RECOMMENDATION: "Mission recommendation",
    EntryKind.QUICK_CHECK_RECOMMENDATION: "Quick Check recommendation",
    EntryKind.REVISION_RECOMMENDATION: "Revision recommendation",
    EntryKind.RECOVERY_RECOMMENDATION: "Recovery recommendation",
    EntryKind.LEARNING_MILESTONE: "Learning milestone",
    EntryKind.EDUCATIONAL_REFLECTION: "Educational reflection",
}

CONFIDENCE_LABELS: dict[str, str] = {
    QualitativeConfidence.INSUFFICIENT: "Not enough evidence yet",
    QualitativeConfidence.OBSERVATION_ONLY: "Still gathering evidence",
    QualitativeConfidence.EMERGING: "Emerging confidence",
    QualitativeConfidence.RELIABLE: "Reliable guidance",
    QualitativeConfidence.HIGH: "High confidence",
}

ACTION_LABELS: dict[str, str] = {
    StudentAction.NONE_YET: "No choice recorded yet",
    StudentAction.ACCEPTED: "You accepted this guidance",
    StudentAction.DEFERRED: "You deferred this guidance",
    StudentAction.DISMISSED: "You set this aside",
}

REFLECTION_LABELS: dict[str, str] = {
    ReflectionStatus.PENDING: "Reflection pending",
    ReflectionStatus.REFLECTED: "Reflected",
    ReflectionStatus.NOT_APPLICABLE: "Reflection not needed",
}


class DecisionJournalError(Exception):
    """Base error for Decision Journal operations."""


class DecisionJournalNotFoundError(DecisionJournalError):
    """Requested journal entry does not exist for this learner."""


class DecisionJournalTransitionError(DecisionJournalError):
    """Illegal lifecycle transition."""


class DecisionJournalService:
    """Persistent educational memory for significant learner decisions."""

    @staticmethod
    def record_entry(
        user_id: int,
        *,
        kind: EntryKind | str,
        educational_context: str,
        observation: str,
        meaning: str,
        recommendation: str,
        supporting_evidence_summary: str = "",
        qualitative_confidence: QualitativeConfidence | str = (
            QualitativeConfidence.EMERGING
        ),
        expected_benefit: str = "",
        uncertainty: str = "",
        catalogue_decision_id: str = "",
        student_action: StudentAction | str = StudentAction.NONE_YET,
        lifecycle_status: JournalLifecycleStatus | str | None = None,
        reflection_status: ReflectionStatus | str = ReflectionStatus.PENDING,
        legacy_decision_id: int | None = None,
        commitment_id: int | None = None,
        recorded_at: datetime | None = None,
    ) -> DecisionJournalEntry:
        """Create one journal entry (immutable guidance snapshot).

        Args:
            user_id: Owning learner.
            kind: Significant interaction kind.
            educational_context: Plain-language study context.
            observation: What we saw (P-001.2 / ILE-001C0).
            meaning: Educational meaning of the observation.
            recommendation: Suggested action at the time.
            supporting_evidence_summary: Evidence available then.
            qualitative_confidence: ILE-011 confidence band.
            expected_benefit: Why the action helps learning.
            uncertainty: What remains uncertain.
            catalogue_decision_id: Optional ILE-011 Decision ID.
            student_action: Initial learner choice if known.
            lifecycle_status: Override; default derived from action.
            reflection_status: Reflection posture.
            legacy_decision_id: Optional link to ``decisions`` row.
            commitment_id: Optional link to recommendation commitment.
            recorded_at: Optional timestamp (defaults to now).

        Returns:
            Persisted ``DecisionJournalEntry``.

        Raises:
            ValueError: Unsafe learner-facing text or invalid enums.
        """
        kind_v = EntryKind(str(kind))
        conf_v = QualitativeConfidence(str(qualitative_confidence))
        action_v = StudentAction(str(student_action))
        reflection_v = ReflectionStatus(str(reflection_status))

        texts = {
            "educational_context": educational_context or "",
            "observation": observation or "",
            "meaning": meaning or "",
            "recommendation": recommendation or "",
            "supporting_evidence_summary": supporting_evidence_summary or "",
            "expected_benefit": expected_benefit or "",
            "uncertainty": uncertainty or "",
        }
        for field, value in texts.items():
            assert_student_safe_text(value, field=field)

        if lifecycle_status is None:
            status_v = _status_from_action(action_v)
        else:
            status_v = JournalLifecycleStatus(str(lifecycle_status))

        now = recorded_at or datetime.utcnow()
        entry = DecisionJournalEntry(
            entry_id=_new_entry_id(),
            user_id=user_id,
            catalogue_decision_id=(catalogue_decision_id or "").strip()[:32],
            kind=kind_v.value,
            lifecycle_status=status_v.value,
            educational_context=texts["educational_context"].strip(),
            observation=texts["observation"].strip(),
            meaning=texts["meaning"].strip(),
            recommendation=texts["recommendation"].strip(),
            supporting_evidence_summary=texts[
                "supporting_evidence_summary"
            ].strip(),
            qualitative_confidence=conf_v.value,
            expected_benefit=texts["expected_benefit"].strip(),
            uncertainty=texts["uncertainty"].strip(),
            student_action=action_v.value,
            reflection_status=reflection_v.value,
            legacy_decision_id=legacy_decision_id,
            commitment_id=commitment_id,
            recorded_at=now,
            accepted_at=now if action_v == StudentAction.ACCEPTED else None,
            deferred_at=now if action_v == StudentAction.DEFERRED else None,
        )
        db.session.add(entry)
        db.session.commit()
        logger.info(
            "decision_journal_recorded user_id=%s entry_id=%s kind=%s",
            user_id,
            entry.entry_id,
            entry.kind,
        )
        return entry

    @staticmethod
    def record_from_recommendation(
        user_id: int,
        tip: dict[str, Any],
        *,
        accepted: bool,
        completed: bool = False,
        outcome_summary: str | None = None,
        kind: EntryKind | str = EntryKind.MISSION_RECOMMENDATION,
        catalogue_decision_id: str = "",
        legacy_decision_id: int | None = None,
        commitment_id: int | None = None,
    ) -> DecisionJournalEntry:
        """Record journal entry from a recommendation tip payload.

        Used by commitment / preference paths. Maps tip fields onto the
        explainability arc without exposing internals.
        """
        title = str(tip.get("title") or tip.get("topic_title") or "Study tip")
        reason = str(
            tip.get("reason")
            or tip.get("why_recommended")
            or tip.get("summary")
            or ""
        )
        benefit = str(tip.get("expected_benefit") or "")
        evidence = str(
            tip.get("supporting_evidence")
            or tip.get("review_point")
            or tip.get("summary")
            or ""
        )
        uncertainty = str(tip.get("uncertainty") or "")
        context = str(tip.get("educational_context") or tip.get("category") or "")
        observation = str(tip.get("observation") or reason or title)
        meaning = str(tip.get("meaning") or reason)
        recommendation = str(
            tip.get("suggested_next_action") or tip.get("recommendation") or title
        )

        if accepted and completed:
            action = StudentAction.ACCEPTED
            status = JournalLifecycleStatus.OUTCOME_RECORDED
            reflection = ReflectionStatus.PENDING
        elif accepted:
            action = StudentAction.ACCEPTED
            status = JournalLifecycleStatus.ACCEPTED
            reflection = ReflectionStatus.PENDING
        else:
            action = StudentAction.DEFERRED
            status = JournalLifecycleStatus.DEFERRED
            reflection = ReflectionStatus.PENDING

        entry = DecisionJournalService.record_entry(
            user_id,
            kind=kind,
            educational_context=context or "Today's study guidance",
            observation=observation,
            meaning=meaning,
            recommendation=recommendation,
            supporting_evidence_summary=evidence,
            qualitative_confidence=QualitativeConfidence.EMERGING,
            expected_benefit=benefit,
            uncertainty=uncertainty,
            catalogue_decision_id=catalogue_decision_id,
            student_action=action,
            lifecycle_status=status,
            reflection_status=reflection,
            legacy_decision_id=legacy_decision_id,
            commitment_id=commitment_id,
        )
        if outcome_summary:
            DecisionJournalService.record_outcome(
                user_id,
                entry.entry_id,
                outcome_summary=outcome_summary,
            )
            entry = DecisionJournalService.get_entry(user_id, entry.entry_id)
        return entry

    @staticmethod
    def accept_entry(user_id: int, entry_id: str) -> DecisionJournalEntry:
        """Mark guidance as accepted by the learner."""
        entry = DecisionJournalService._owned(user_id, entry_id)
        DecisionJournalService._transition(
            entry, JournalLifecycleStatus.ACCEPTED
        )
        entry.student_action = StudentAction.ACCEPTED.value
        entry.accepted_at = datetime.utcnow()
        db.session.commit()
        return entry

    @staticmethod
    def defer_entry(user_id: int, entry_id: str) -> DecisionJournalEntry:
        """Mark guidance as deferred by the learner."""
        entry = DecisionJournalService._owned(user_id, entry_id)
        DecisionJournalService._transition(
            entry, JournalLifecycleStatus.DEFERRED
        )
        entry.student_action = StudentAction.DEFERRED.value
        entry.deferred_at = datetime.utcnow()
        db.session.commit()
        return entry

    @staticmethod
    def append_evidence(
        user_id: int,
        entry_id: str,
        *,
        summary: str,
        move_status: bool = True,
    ) -> DecisionJournalEvidenceEvent:
        """Append evidence evolution without rewriting the original guidance.

        Args:
            user_id: Owning learner.
            entry_id: Public Decision ID.
            summary: Student-safe description of new evidence.
            move_status: When True, move lifecycle to ``evidence_evolving``
                if lawful.
        """
        assert_student_safe_text(summary or "", field="evidence_summary")
        entry = DecisionJournalService._owned(user_id, entry_id)
        if entry.lifecycle_status == JournalLifecycleStatus.ARCHIVED.value:
            raise DecisionJournalTransitionError(
                "Cannot append evidence to an archived journal entry"
            )
        event = DecisionJournalEvidenceEvent(
            entry_pk=entry.id,
            summary=(summary or "").strip(),
            recorded_at=datetime.utcnow(),
        )
        db.session.add(event)
        if move_status and can_transition(
            entry.lifecycle_status,
            JournalLifecycleStatus.EVIDENCE_EVOLVING,
        ):
            entry.lifecycle_status = (
                JournalLifecycleStatus.EVIDENCE_EVOLVING.value
            )
        db.session.commit()
        logger.info(
            "decision_journal_evidence_appended user_id=%s entry_id=%s",
            user_id,
            entry_id,
        )
        return event

    @staticmethod
    def record_reflection(
        user_id: int,
        entry_id: str,
        *,
        note: str = "",
    ) -> DecisionJournalEntry:
        """Close the reflection loop for a journal entry.

        When the entry is already ``outcome_recorded``, reflection fields are
        appended without requiring a lifecycle rewrite of the outcome itself
        when transition to ``reflected`` is lawful (ILE-005 feedback loop).
        """
        assert_student_safe_text(note or "", field="reflection_note")
        entry = DecisionJournalService._owned(user_id, entry_id)
        target = JournalLifecycleStatus.REFLECTED
        if can_transition(entry.lifecycle_status, target):
            DecisionJournalService._transition(entry, target)
        elif entry.lifecycle_status != JournalLifecycleStatus.REFLECTED.value:
            raise DecisionJournalTransitionError(
                f"Cannot record reflection from {entry.lifecycle_status}"
            )
        entry.reflection_status = ReflectionStatus.REFLECTED.value
        entry.reflection_note = (note or "").strip()
        entry.reflected_at = datetime.utcnow()
        db.session.commit()
        return entry

    @staticmethod
    def record_outcome(
        user_id: int,
        entry_id: str,
        *,
        outcome_summary: str,
    ) -> DecisionJournalEntry:
        """Record what happened afterwards (never shames the learner)."""
        assert_student_safe_text(outcome_summary or "", field="outcome_summary")
        entry = DecisionJournalService._owned(user_id, entry_id)
        # Outcome may follow reflection or earlier accepted/deferred states.
        target = JournalLifecycleStatus.OUTCOME_RECORDED
        if not can_transition(entry.lifecycle_status, target):
            # Allow outcome after reflection path by stepping if needed.
            if can_transition(
                entry.lifecycle_status, JournalLifecycleStatus.REFLECTED
            ):
                DecisionJournalService._transition(
                    entry, JournalLifecycleStatus.REFLECTED
                )
                entry.reflection_status = ReflectionStatus.REFLECTED.value
                if entry.reflected_at is None:
                    entry.reflected_at = datetime.utcnow()
        DecisionJournalService._transition(entry, target)
        entry.outcome_summary = (outcome_summary or "").strip()
        entry.outcome_at = datetime.utcnow()
        db.session.commit()
        return entry

    @staticmethod
    def archive_entry(user_id: int, entry_id: str) -> DecisionJournalEntry:
        """Archive an entry. Never deletes; history remains readable."""
        entry = DecisionJournalService._owned(user_id, entry_id)
        DecisionJournalService._transition(
            entry, JournalLifecycleStatus.ARCHIVED
        )
        entry.archived_at = datetime.utcnow()
        db.session.commit()
        return entry

    @staticmethod
    def get_entry(user_id: int, entry_id: str) -> DecisionJournalEntry:
        """Return one owned entry or raise ``DecisionJournalNotFound``."""
        return DecisionJournalService._owned(user_id, entry_id)

    @staticmethod
    def get_timeline(
        user_id: int,
        *,
        limit: int = 50,
        include_archived: bool = True,
    ) -> list[DecisionJournalEntry]:
        """Return newest-first chronology for the learner."""
        query = DecisionJournalEntry.query.filter_by(user_id=user_id)
        if not include_archived:
            query = query.filter(
                DecisionJournalEntry.lifecycle_status
                != JournalLifecycleStatus.ARCHIVED.value
            )
        return (
            query.order_by(DecisionJournalEntry.recorded_at.desc())
            .limit(max(1, min(limit, 200)))
            .all()
        )

    @staticmethod
    def to_student_dict(
        entry: DecisionJournalEntry,
        *,
        evidence_events: list[DecisionJournalEvidenceEvent] | None = None,
    ) -> dict[str, Any]:
        """Present one entry for student UI / JSON — no internals."""
        events = evidence_events
        if events is None:
            events = list(entry.evidence_events or [])
        return {
            "decision_id": entry.entry_id,
            "timestamp": (
                entry.recorded_at.isoformat() if entry.recorded_at else None
            ),
            "kind": entry.kind,
            "kind_label": KIND_LABELS.get(entry.kind, "Educational guidance"),
            "lifecycle_status": entry.lifecycle_status,
            "lifecycle_label": LIFECYCLE_LABELS.get(
                entry.lifecycle_status, entry.lifecycle_status
            ),
            "educational_context": entry.educational_context,
            "observation": entry.observation,
            "meaning": entry.meaning,
            "recommendation": entry.recommendation,
            "supporting_evidence_summary": entry.supporting_evidence_summary,
            "qualitative_confidence": entry.qualitative_confidence,
            "confidence_label": CONFIDENCE_LABELS.get(
                entry.qualitative_confidence, "Emerging confidence"
            ),
            "expected_benefit": entry.expected_benefit,
            "uncertainty": entry.uncertainty,
            "student_action": entry.student_action,
            "student_action_label": ACTION_LABELS.get(
                entry.student_action, "No choice recorded yet"
            ),
            "outcome_summary": entry.outcome_summary or "",
            "reflection_status": entry.reflection_status,
            "reflection_label": REFLECTION_LABELS.get(
                entry.reflection_status, "Reflection pending"
            ),
            "reflection_note": entry.reflection_note or "",
            "catalogue_decision_id": entry.catalogue_decision_id or "",
            "evidence_updates": [
                {
                    "summary": ev.summary,
                    "recorded_at": (
                        ev.recorded_at.isoformat() if ev.recorded_at else None
                    ),
                }
                for ev in events
            ],
            # Narrative questions for the timeline.
            "what_happened": entry.observation,
            "why": entry.meaning,
            "what_i_chose": ACTION_LABELS.get(
                entry.student_action, "No choice recorded yet"
            ),
            "what_happened_afterwards": entry.outcome_summary or "",
            "what_to_learn": entry.reflection_note
            or entry.expected_benefit
            or "",
        }

    # ── internals ─────────────────────────────────────────────────────────

    @staticmethod
    def _owned(user_id: int, entry_id: str) -> DecisionJournalEntry:
        entry = DecisionJournalEntry.query.filter_by(
            user_id=user_id, entry_id=entry_id
        ).first()
        if entry is None:
            raise DecisionJournalNotFoundError(
                f"Decision Journal entry not found: {entry_id}"
            )
        return entry

    @staticmethod
    def _transition(
        entry: DecisionJournalEntry,
        target: JournalLifecycleStatus,
    ) -> None:
        if not can_transition(entry.lifecycle_status, target):
            raise DecisionJournalTransitionError(
                f"Cannot move journal entry from "
                f"{entry.lifecycle_status} to {target.value}"
            )
        entry.lifecycle_status = target.value


def _new_entry_id() -> str:
    return f"dj_{uuid.uuid4().hex[:20]}"


def _status_from_action(action: StudentAction) -> JournalLifecycleStatus:
    if action == StudentAction.ACCEPTED:
        return JournalLifecycleStatus.ACCEPTED
    if action == StudentAction.DEFERRED:
        return JournalLifecycleStatus.DEFERRED
    if action == StudentAction.DISMISSED:
        return JournalLifecycleStatus.DEFERRED
    return JournalLifecycleStatus.RECOMMENDED
