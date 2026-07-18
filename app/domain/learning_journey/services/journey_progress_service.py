"""Deterministic educational progress calculation for Learning Journeys.

Derives JourneyProgress from sessions, evidence, objectives, and reflections.
Does not estimate mastery, invent competence scores, or write Twin beliefs.
"""

from __future__ import annotations

from app.domain.evidence.evidence_category import EvidenceConfidenceLevel
from app.domain.learning_journey.entities.journey_evidence import JourneyEvidence
from app.domain.learning_journey.entities.journey_progress import (
    ConsistencyPosture,
    EvidenceConfidencePosture,
    JourneyProgress,
)
from app.domain.learning_journey.entities.journey_reflection import ReflectionPosture
from app.domain.learning_journey.entities.learning_journey import LearningJourney
from app.domain.learning_journey.entities.learning_session import LearningSession
from app.domain.learning_journey.value_objects.completion_status import CompletionStatus
from app.domain.learning_journey.value_objects.session_state import SessionState


class JourneyProgressService:
    """Calculate educational progress from available journey artefacts.

    All calculations are deterministic: same inputs → same JourneyProgress.
    """

    # Default structural thresholds for READY_FOR_COMPLETION (domain foundation).
    # Exact product thresholds remain V2-003 concerns; these are honest floors.
    DEFAULT_MIN_COMPLETED_SESSIONS = 2
    DEFAULT_REQUIRE_REFLECTIONS_FOR_COMPLETED = True

    @staticmethod
    def calculate(
        journey: LearningJourney,
        *,
        min_completed_sessions: int = DEFAULT_MIN_COMPLETED_SESSIONS,
        require_reflections: bool = DEFAULT_REQUIRE_REFLECTIONS_FOR_COMPLETED,
    ) -> JourneyProgress:
        """Derive JourneyProgress from the journey aggregate.

        Args:
            journey: Learning Journey aggregate to evaluate.
            min_completed_sessions: Structural session-sufficiency floor.
            require_reflections: When True, every completed session must have
                a CAPTURED reflection before completion criteria can be met.

        Returns:
            A deterministic JourneyProgress posture (no mastery claims).
        """
        objectives_total = len(journey.objectives)
        addressed = JourneyProgressService._objectives_addressed(journey)
        completed_sessions = [
            s for s in journey.sessions if s.state == SessionState.COMPLETED
        ]
        sessions_completed = len(completed_sessions)
        sessions_planned = sum(
            1
            for s in journey.sessions
            if s.state != SessionState.SKIPPED
        )
        evidence_count = len(journey.evidence)
        reflections_captured = sum(
            1
            for r in journey.reflections
            if r.posture == ReflectionPosture.CAPTURED
        )
        consistency = JourneyProgressService._consistency(sessions_completed)
        evidence_confidence = JourneyProgressService._evidence_confidence(
            journey.evidence
        )
        meets = JourneyProgressService._meets_completion_criteria(
            journey,
            objectives_total=objectives_total,
            objectives_addressed=addressed,
            sessions_completed=sessions_completed,
            completed_sessions=completed_sessions,
            min_completed_sessions=min_completed_sessions,
            require_reflections=require_reflections,
        )
        completion_status = JourneyProgressService._completion_status(
            journey,
            sessions_completed=sessions_completed,
            objectives_addressed=addressed,
            objectives_total=objectives_total,
            meets_completion_criteria=meets,
        )
        return JourneyProgress.create(
            objectives_total=objectives_total,
            objectives_addressed=addressed,
            sessions_completed=sessions_completed,
            sessions_planned=sessions_planned,
            evidence_count=evidence_count,
            reflections_captured=reflections_captured,
            consistency=consistency,
            evidence_confidence=evidence_confidence,
            completion_status=completion_status,
            meets_completion_criteria=meets,
        )

    @staticmethod
    def _objectives_addressed(journey: LearningJourney) -> int:
        if not journey.objectives:
            return 0
        addressed_ids: set[str] = set()
        objective_ids = {o.objective_id for o in journey.objectives}
        for session in journey.sessions:
            if (
                session.objective_id
                and session.objective_id in objective_ids
                and session.state
                in {
                    SessionState.COMPLETED,
                    SessionState.ACTIVE,
                    SessionState.PAUSED,
                }
            ):
                addressed_ids.add(session.objective_id)
        for item in journey.evidence:
            if item.objective_id and item.objective_id in objective_ids:
                addressed_ids.add(item.objective_id)
        return len(addressed_ids)

    @staticmethod
    def _consistency(sessions_completed: int) -> ConsistencyPosture:
        if sessions_completed <= 0:
            return ConsistencyPosture.NONE
        if sessions_completed == 1:
            return ConsistencyPosture.SPARSE
        if sessions_completed >= 2:
            return ConsistencyPosture.REGULAR
        return ConsistencyPosture.UNKNOWN

    @staticmethod
    def _evidence_confidence(
        evidence: tuple[JourneyEvidence, ...],
    ) -> EvidenceConfidencePosture:
        if not evidence:
            return EvidenceConfidencePosture.UNKNOWN
        levels = [e.confidence_level for e in evidence]
        if all(level == EvidenceConfidenceLevel.UNKNOWN for level in levels):
            return EvidenceConfidencePosture.UNKNOWN
        known = [level for level in levels if level != EvidenceConfidenceLevel.UNKNOWN]
        if not known:
            return EvidenceConfidencePosture.UNKNOWN
        if len(known) < 2:
            return EvidenceConfidencePosture.THIN
        high = sum(1 for level in known if level == EvidenceConfidenceLevel.HIGH)
        medium = sum(1 for level in known if level == EvidenceConfidenceLevel.MEDIUM)
        low = sum(1 for level in known if level == EvidenceConfidenceLevel.LOW)
        if high >= medium and high >= low and high > 0:
            return EvidenceConfidencePosture.HIGH
        if medium >= low:
            return EvidenceConfidencePosture.MEDIUM
        return EvidenceConfidencePosture.LOW

    @staticmethod
    def _meets_completion_criteria(
        journey: LearningJourney,
        *,
        objectives_total: int,
        objectives_addressed: int,
        sessions_completed: int,
        completed_sessions: list[LearningSession],
        min_completed_sessions: int,
        require_reflections: bool,
    ) -> bool:
        if sessions_completed < min_completed_sessions:
            return False
        if objectives_total > 0 and objectives_addressed < objectives_total:
            return False
        if require_reflections:
            captured_session_ids = {
                r.session_id
                for r in journey.reflections
                if r.posture == ReflectionPosture.CAPTURED
            }
            for session in completed_sessions:
                if session.session_id not in captured_session_ids:
                    if not (
                        session.reflection is not None
                        and session.reflection.posture == ReflectionPosture.CAPTURED
                    ):
                        return False
        return True

    @staticmethod
    def _completion_status(
        journey: LearningJourney,
        *,
        sessions_completed: int,
        objectives_addressed: int,
        objectives_total: int,
        meets_completion_criteria: bool,
    ) -> CompletionStatus:
        if journey.state.value == "completed":
            return CompletionStatus.COMPLETED
        if journey.state.value in {"abandoned", "archived"}:
            return CompletionStatus.INCOMPLETE
        if meets_completion_criteria:
            return CompletionStatus.READY_FOR_COMPLETION
        if sessions_completed == 0 and objectives_addressed == 0:
            return CompletionStatus.NOT_STARTED
        if objectives_total > 0 and 0 < objectives_addressed < objectives_total:
            return CompletionStatus.PARTIALLY_ADDRESSED
        return CompletionStatus.IN_PROGRESS
