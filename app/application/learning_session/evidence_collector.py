"""Coordinates educational evidence generated during a Learning Session.

Integrates with the Learning Evidence Model via ``JourneyEvidence``
attribution. Never estimates mastery. Never persists.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.application.learning_session.dto.evidence_summary import EvidenceSummary
from app.application.learning_session.exceptions import (
    EvidenceCollectionError,
    InvalidSessionState,
    SessionAlreadyArchived,
)
from app.application.learning_session.runtime_phase import RuntimePhase
from app.domain.evidence.evidence_category import EvidenceConfidenceLevel
from app.domain.evidence.evidence_type import EvidenceType
from app.domain.evidence.learning_evidence import LearningEvidence
from app.domain.learning_journey.entities.journey_evidence import JourneyEvidence
from app.domain.learning_journey.entities.learning_session import LearningSession
from app.domain.learning_journey.value_objects.session_state import SessionState


class EvidenceCollector:
    """Attach and summarise session-scoped educational evidence."""

    def __init__(self, *, clock=None, id_factory=None) -> None:
        self._clock = clock or (lambda: datetime.now(tz=UTC))
        self._id_factory = id_factory or (lambda: "ev")

    def collect(
        self,
        session: LearningSession,
        *,
        phase: RuntimePhase,
        evidence_type: EvidenceType | str,
        evidence_id: str | None = None,
        confidence_level: EvidenceConfidenceLevel
        | str = EvidenceConfidenceLevel.UNKNOWN,
        objective_id: str | None = None,
        topic_id: str | None = None,
        learning_evidence: LearningEvidence | None = None,
    ) -> tuple[LearningSession, JourneyEvidence]:
        """Attribute educational evidence to an in-progress or completed session.

        Accepts either catalogue fields or an existing ``LearningEvidence``
        record. Never invents mastery scores.

        Raises:
            SessionAlreadyArchived / InvalidSessionState /
            EvidenceCollectionError.
        """
        self._assert_collectable(session, phase)

        if learning_evidence is not None:
            eid = learning_evidence.evidence_id
            etype = learning_evidence.evidence_type
            conf = learning_evidence.confidence_level
            tid = topic_id or learning_evidence.topic_id
            recorded_at = learning_evidence.timestamp
        else:
            eid = evidence_id or f"ev-{self._id_factory()}"
            etype = (
                evidence_type
                if isinstance(evidence_type, EvidenceType)
                else EvidenceType(evidence_type)
            )
            conf = confidence_level
            tid = topic_id
            recorded_at = self._clock()

        if not eid or not str(eid).strip():
            raise EvidenceCollectionError("evidence_id is required")

        journey_evidence = JourneyEvidence.create(
            f"je-{self._id_factory()}",
            eid,
            session.journey_id,
            etype,
            recorded_at,
            confidence_level=conf,
            session_id=session.session_id,
            objective_id=objective_id or session.objective_id,
            topic_id=tid,
        )
        updated = session.with_evidence(journey_evidence)
        return updated, journey_evidence

    def summarise(self, session: LearningSession) -> EvidenceSummary:
        """Build an immutable evidence summary for ``session``."""
        types: list[str] = []
        confidences: list[str] = []
        seen_types: set[str] = set()
        seen_conf: set[str] = set()
        for item in session.evidence:
            tval = item.evidence_type.value
            if tval not in seen_types:
                seen_types.add(tval)
                types.append(tval)
            cval = item.confidence_level.value
            if cval not in seen_conf:
                seen_conf.add(cval)
                confidences.append(cval)
        count = len(session.evidence)
        return EvidenceSummary(
            evidence_count=count,
            evidence_types=tuple(types),
            confidence_levels=tuple(confidences),
            has_evidence=count > 0,
            session_id=session.session_id,
        )

    @staticmethod
    def _assert_collectable(
        session: LearningSession,
        phase: RuntimePhase,
    ) -> None:
        if phase == RuntimePhase.ARCHIVED:
            raise SessionAlreadyArchived(
                f"Session {session.session_id} is archived"
            )
        if session.state in {
            SessionState.NOT_STARTED,
            SessionState.ABANDONED,
            SessionState.SKIPPED,
        }:
            raise InvalidSessionState(
                f"Cannot collect evidence while session is {session.state.value}"
            )
        if phase in {RuntimePhase.PLANNED, RuntimePhase.READY}:
            raise InvalidSessionState(
                f"Cannot collect evidence while session phase is {phase.value}"
            )
