"""Student Digital Twin Engine — public application facade.

Consumes evidence only. Recalculates derived educational state deterministically.
Does NOT teach. Does NOT store curriculum. Does NOT persist. Does NOT use Flask.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from uuid import uuid4

from app.application.student_twin.comparison_service import ComparisonService
from app.application.student_twin.confidence_calculator import ConfidenceCalculator
from app.application.student_twin.diagnostics import TwinDiagnostics
from app.application.student_twin.dto.comparison_snapshot import ComparisonSnapshot
from app.application.student_twin.dto.learner_snapshot import LearnerSnapshot
from app.application.student_twin.dto.recommendation_snapshot import (
    RecommendationExplanation,
)
from app.application.student_twin.dto.twin_snapshot import TwinSnapshotDTO
from app.application.student_twin.evidence_aggregator import EvidenceAggregator
from app.application.student_twin.exceptions import DuplicateEvidence, EvidenceRejected
from app.application.student_twin.explanation_service import ExplanationService
from app.application.student_twin.learning_velocity_service import (
    LearningVelocityService,
)
from app.application.student_twin.mastery_calculator import MasteryCalculator
from app.application.student_twin.policies.confidence_policy import ConfidencePolicy
from app.application.student_twin.policies.evidence_policy import EvidencePolicy
from app.application.student_twin.policies.mastery_policy import MasteryPolicy
from app.application.student_twin.readiness_estimator import ReadinessEstimator
from app.application.student_twin.recommendation_service import RecommendationService
from app.application.student_twin.retention_estimator import RetentionEstimator
from app.application.student_twin.snapshot_service import SnapshotService
from app.application.student_twin.timeline_service import TimelineService
from app.application.student_twin.weakness_analyser import WeaknessAnalyser
from app.domain.student_twin.digital_twin import DigitalTwin
from app.domain.student_twin.evidence_event import EvidenceEvent
from app.domain.student_twin.knowledge_state import KnowledgeState, TopicKnowledgeRecord
from app.domain.student_twin.learner import Learner
from app.domain.student_twin.twin_snapshot import TwinSnapshot


class StudentTwinEngine:
    """Public facade for the Student Digital Twin 2.0.

    Framework-independent. Callers remain responsible for persistence.
    Same evidence → same Twin conclusions (deterministic).
    """

    ENGINE_ID = "student_twin"
    ENGINE_VERSION = "2.0.0"

    def __init__(
        self,
        *,
        clock: Callable[[], datetime] | None = None,
        id_factory: Callable[[], str] | None = None,
    ) -> None:
        self._clock = clock or (lambda: datetime.now(tz=UTC))
        self._id_factory = id_factory or (lambda: uuid4().hex[:12])

    def create_twin(
        self,
        learner: Learner | str,
        *,
        twin_id: str | None = None,
        subject_code: str | None = None,
    ) -> DigitalTwin:
        """Create an empty Twin for a learner."""
        tid = twin_id or f"twin-{self._id_factory()}"
        return DigitalTwin.create(
            tid,
            learner,
            subject_code=subject_code,
            created_at=self._clock(),
        )

    def ingest_evidence(
        self,
        twin: DigitalTwin,
        event: EvidenceEvent,
    ) -> DigitalTwin:
        """Admit one evidence event and recalculate all derived states."""
        try:
            EvidencePolicy.assert_admissible(twin, event)
        except EvidenceRejected:
            raise
        except Exception as exc:
            if "duplicate" in str(exc).lower():
                raise DuplicateEvidence(str(exc)) from exc
            raise

        updated = twin.with_evidence(event)
        return self.recalculate(updated, as_of=event.occurred_at)

    def ingest_many(
        self,
        twin: DigitalTwin,
        events: list[EvidenceEvent] | tuple[EvidenceEvent, ...],
    ) -> DigitalTwin:
        """Admit many evidence events in order; recalculate after each."""
        current = twin
        for event in events:
            current = self.ingest_evidence(current, event)
        return current

    def recalculate(
        self,
        twin: DigitalTwin,
        *,
        as_of: datetime | None = None,
        velocity_window_days: float = 7.0,
    ) -> DigitalTwin:
        """Recalculate all derived Twin states from history."""
        when = as_of if as_of is not None else self._clock()
        if when.tzinfo is None:
            when = when.replace(tzinfo=UTC)

        profile = EvidenceAggregator.from_twin(twin)
        mastery = MasteryCalculator.calculate(twin.history.events)
        knowledge = self._knowledge_from_mastery(mastery, twin.history.events)
        confidence = ConfidenceCalculator.calculate(twin.history.events)
        # Temporarily bind mastery for retention which reads twin.mastery in from_twin;
        # calculate directly with mastery parameter instead.
        retention = RetentionEstimator.calculate(
            twin.history.events,
            mastery,
            as_of=when,
        )
        readiness = ReadinessEstimator.calculate(mastery, retention, confidence)
        velocity = LearningVelocityService.calculate(
            twin.history.events,
            as_of=when,
            window_days=velocity_window_days,
        )
        weaknesses = WeaknessAnalyser.analyse(mastery, retention, confidence)
        recommendations = RecommendationService.recommend(
            mastery,
            retention,
            readiness,
            weaknesses,
            velocity,
        )
        return DigitalTwin(
            identity=twin.identity,
            learner=twin.learner,
            version=twin.version,
            history=twin.history,
            knowledge=knowledge,
            mastery=mastery,
            confidence=confidence,
            retention=retention,
            readiness=readiness,
            velocity=velocity,
            weaknesses=weaknesses,
            recommendations=recommendations,
            evidence_profile=profile,
            created_at=twin.created_at,
            updated_at=when,
        )

    def snapshot(
        self,
        twin: DigitalTwin,
        *,
        as_of: datetime | None = None,
    ) -> TwinSnapshotDTO:
        """Capture and project an immutable Twin snapshot DTO."""
        domain = SnapshotService.capture(twin, as_of=as_of or self._clock())
        return SnapshotService.to_dto(domain)

    def domain_snapshot(
        self,
        twin: DigitalTwin,
        *,
        as_of: datetime | None = None,
    ) -> TwinSnapshot:
        """Capture a domain TwinSnapshot."""
        return SnapshotService.capture(twin, as_of=as_of or self._clock())

    def learner_snapshot(self, twin: DigitalTwin) -> LearnerSnapshot:
        """Project the Twin's learner identity."""
        return LearnerSnapshot.from_domain(twin.learner)

    def explain(
        self,
        twin: DigitalTwin,
        recommendation_id: str,
    ) -> RecommendationExplanation:
        """Explain one recommendation."""
        return ExplanationService.explain_recommendation(twin, recommendation_id)

    def explain_all(self, twin: DigitalTwin) -> tuple[RecommendationExplanation, ...]:
        """Explain all recommendations."""
        return ExplanationService.explain_all(twin)

    def compare(
        self,
        baseline: TwinSnapshot,
        current: TwinSnapshot,
    ) -> ComparisonSnapshot:
        """Compare two domain snapshots."""
        return ComparisonService.compare(baseline, current)

    def timeline(
        self,
        snapshots: list[TwinSnapshot] | tuple[TwinSnapshot, ...],
    ) -> tuple[TwinSnapshot, ...]:
        """Order snapshots chronologically by version."""
        return TimelineService.build(snapshots)

    def diagnose(self, twin: DigitalTwin):
        """Inspect Twin integrity."""
        return TwinDiagnostics.inspect(twin)

    @staticmethod
    def _knowledge_from_mastery(mastery, events) -> KnowledgeState:
        """Derive KnowledgeState from mastery with a deterministic transform.

        Knowledge tracks understanding belief; mastery tracks demonstrated
        capability. Knowledge is slightly lagged relative to mastery.
        """
        by_topic: dict[str, list] = {}
        for event in events:
            if event.topic_id is None:
                continue
            by_topic.setdefault(event.topic_id, []).append(event)

        records: list[TopicKnowledgeRecord] = []
        for record in mastery.topic_records:
            # Understanding lags demonstration slightly (deterministic).
            knowledge_score = max(0.0, min(1.0, record.mastery_score * 0.95 + 0.02))
            topic_events = by_topic.get(record.topic_id, [])
            # Soft boost from positive reflection / self-assessment.
            for event in topic_events:
                delta = MasteryPolicy.delta_for(event) * 0.25
                knowledge_score = max(0.0, min(1.0, knowledge_score + delta * 0.1))
            conf = ConfidencePolicy.score_for(topic_events)
            records.append(
                TopicKnowledgeRecord.create(
                    record.topic_id,
                    knowledge_score,
                    confidence_score=conf,
                    evidence_ids=record.evidence_ids,
                )
            )
        return KnowledgeState.create(
            records,
            evidence_ids=mastery.evidence_ids,
        )
