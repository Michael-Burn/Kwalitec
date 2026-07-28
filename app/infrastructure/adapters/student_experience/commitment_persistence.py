"""Recommendation Commitment persistence + journal adapters (EP-008.3A).

Binds the process-local ports consumed by
``app.application.student_experience.recommendation_commitment`` to
SQLAlchemy, the existing Decision Journal API (``RecommendationService``),
and the Learning Feedback emitter.
"""

from __future__ import annotations

from app.application.student_experience.ports.commitment_port import (
    CommitmentRecord,
    bind_commitment_persistence_port,
    bind_decision_journal_port,
    bind_learning_feedback_port,
)
from app.extensions import db
from app.models.recommendation_commitment import RecommendationCommitment


class SqlCommitmentPersistenceAdapter:
    """CommitmentPersistencePort backed by ``recommendation_commitments``."""

    def find_active(
        self, user_id: int, recommendation_key: str
    ) -> CommitmentRecord | None:
        if not recommendation_key:
            return None
        row = (
            RecommendationCommitment.query.filter_by(
                user_id=user_id, recommendation_key=recommendation_key
            )
            .order_by(RecommendationCommitment.id.desc())
            .first()
        )
        return _to_record(row)

    def find_by_session(
        self, user_id: int, session_id: str
    ) -> CommitmentRecord | None:
        row = (
            RecommendationCommitment.query.filter_by(
                user_id=user_id, session_id=str(session_id)
            )
            .order_by(RecommendationCommitment.id.desc())
            .first()
        )
        return _to_record(row)

    def find_latest_open(self, user_id: int) -> CommitmentRecord | None:
        row = (
            RecommendationCommitment.query.filter(
                RecommendationCommitment.user_id == user_id,
                RecommendationCommitment.state.in_(["committed", "in_session"]),
            )
            .order_by(RecommendationCommitment.id.desc())
            .first()
        )
        return _to_record(row)

    def find_latest_completed(self, user_id: int) -> CommitmentRecord | None:
        row = (
            RecommendationCommitment.query.filter_by(
                user_id=user_id, state="completed"
            )
            .order_by(RecommendationCommitment.id.desc())
            .first()
        )
        return _to_record(row)

    def find_recent(
        self,
        user_id: int,
        *,
        since,
        states,
        limit: int,
    ) -> tuple[CommitmentRecord, ...]:
        rows = (
            RecommendationCommitment.query.filter(
                RecommendationCommitment.user_id == user_id,
                RecommendationCommitment.created_at >= since,
                RecommendationCommitment.state.in_(list(states)),
            )
            .order_by(RecommendationCommitment.updated_at.desc())
            .limit(max(1, limit))
            .all()
        )
        return tuple(_to_record(r) for r in rows if r is not None)  # type: ignore[misc]

    def save(self, record: CommitmentRecord) -> CommitmentRecord:
        row = None
        if record.id is not None:
            row = db.session.get(RecommendationCommitment, record.id)
        if row is None:
            row = RecommendationCommitment(
                user_id=record.user_id,
                recommendation_key=record.recommendation_key,
            )
            db.session.add(row)
        row.title = record.title
        row.state = record.state
        row.deferred_reason_code = record.deferred_reason_code
        row.deferred_reason_note = record.deferred_reason_note
        row.expected_benefit = record.expected_benefit
        row.review_point = record.review_point
        row.suggested_next_action = record.suggested_next_action
        row.session_id = record.session_id
        row.decision_id = record.decision_id
        row.committed_at = record.committed_at
        row.deferred_at = record.deferred_at
        row.session_started_at = record.session_started_at
        row.completed_at = record.completed_at
        row.reflected_at = record.reflected_at
        db.session.commit()
        # Mutate the caller's record in place so subsequent field reads
        # (e.g. row.title after a fallback assignment) stay consistent.
        record.id = row.id
        record.created_at = row.created_at
        record.updated_at = row.updated_at
        return record


class RecommendationServiceDecisionJournalAdapter:
    """DecisionJournalPort — preference audit + ILE-002 educational journal.

    Writes the legacy ``decisions`` preference row (EP-008.3 contract) and
    mirrors a student-safe narrative entry into the Decision Journal.
    Educational Journal write is fail-open so preference recording never
    breaks commitment flows.
    """

    def record_decision(
        self,
        user_id: int,
        tip: dict,
        *,
        accepted: bool,
        completed: bool,
        outcome_summary: str | None = None,
    ) -> int | None:
        from app.services.recommendation_service import RecommendationService

        decision = RecommendationService.record_decision(
            user_id,
            tip,
            accepted=accepted,
            completed=completed,
            outcome_summary=outcome_summary,
        )
        decision_id = getattr(decision, "id", None)
        try:
            from app.domain.decision_journal import EntryKind
            from app.services.decision_journal_service import (
                DecisionJournalService,
            )

            DecisionJournalService.record_from_recommendation(
                user_id,
                tip,
                accepted=accepted,
                completed=completed,
                outcome_summary=outcome_summary,
                kind=EntryKind.MISSION_RECOMMENDATION,
                catalogue_decision_id="D-L01",
                legacy_decision_id=decision_id,
            )
        except Exception:  # noqa: BLE001 — journal must not break preference
            import logging

            logging.getLogger(__name__).debug(
                "ile002_decision_journal_mirror_failed user_id=%s",
                user_id,
                exc_info=True,
            )
        return decision_id


class LearningFeedbackEmitterAdapter:
    """LearningFeedbackPort — delegates to the Learning Feedback emitter."""

    def emit(
        self,
        *,
        student_id: int,
        event_type: str,
        source_authority: str,
        claim_boundary: str,
        payload: dict,
    ) -> None:
        from app.infrastructure.adapters.learning_feedback import (
            emit_learning_feedback,
        )

        emit_learning_feedback(
            student_id=student_id,
            event_type=event_type,
            source_authority=source_authority,
            claim_boundary=claim_boundary,
            payload=payload,
        )


def _to_record(row: RecommendationCommitment | None) -> CommitmentRecord | None:
    if row is None:
        return None
    return CommitmentRecord(
        id=row.id,
        user_id=row.user_id,
        recommendation_key=row.recommendation_key,
        title=row.title or "",
        state=row.state or "",
        deferred_reason_code=row.deferred_reason_code or "",
        deferred_reason_note=row.deferred_reason_note or "",
        expected_benefit=row.expected_benefit or "",
        review_point=row.review_point or "",
        suggested_next_action=row.suggested_next_action or "",
        session_id=row.session_id or "",
        decision_id=row.decision_id,
        committed_at=row.committed_at,
        deferred_at=row.deferred_at,
        session_started_at=row.session_started_at,
        completed_at=row.completed_at,
        reflected_at=row.reflected_at,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


bind_commitment_persistence_port(SqlCommitmentPersistenceAdapter())
bind_decision_journal_port(RecommendationServiceDecisionJournalAdapter())
bind_learning_feedback_port(LearningFeedbackEmitterAdapter())
