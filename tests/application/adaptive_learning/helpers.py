"""Shared helpers for Adaptive Decision Engine application tests."""

from __future__ import annotations

from datetime import UTC, datetime

from app.application.adaptive_learning.decision_engine import (
    AdaptiveDecisionEngine,
    CurriculumContextInput,
    JourneyPositionInput,
)
from app.domain.student_twin.confidence_band import ConfidenceBand
from app.domain.student_twin.confidence_state import (
    ConfidenceState,
    TopicConfidenceRecord,
)
from app.domain.student_twin.knowledge_state import KnowledgeState, TopicKnowledgeRecord
from app.domain.student_twin.learning_velocity import LearningVelocity
from app.domain.student_twin.mastery_state import MasteryState, TopicMasteryRecord
from app.domain.student_twin.readiness_state import ReadinessState
from app.domain.student_twin.retention_state import RetentionState, TopicRetentionRecord
from app.domain.student_twin.twin_identity import TwinIdentity
from app.domain.student_twin.twin_snapshot import TwinSnapshot
from app.domain.student_twin.twin_version import TwinVersion
from app.domain.student_twin.weakness_profile import (
    WeaknessItem,
    WeaknessKind,
    WeaknessProfile,
)

FIXED_TIME = datetime(2026, 7, 18, 12, 0, tzinfo=UTC)


def make_engine(*, seed: str = "fixed") -> AdaptiveDecisionEngine:
    counter = {"n": 0}

    def _ids() -> str:
        counter["n"] += 1
        return f"{seed}{counter['n']:04d}"

    return AdaptiveDecisionEngine(clock=lambda: FIXED_TIME, id_factory=_ids)


def make_snapshot(
    *,
    topics: list[dict] | None = None,
    learner_id: str = "learner-1",
    twin_id: str = "twin-1",
    readiness: float = 0.4,
    events_per_day: float = 2.0,
    mastery_delta: float = 0.0,
    history_event_ids: list[str] | None = None,
) -> TwinSnapshot:
    """Build a TwinSnapshot from compact topic dicts.

    Each topic dict may include: id, mastery, retention, knowledge,
    confidence, severity, weakness_kind.
    """
    specs = topics or [
        {
            "id": "topic-1",
            "mastery": 0.3,
            "retention": 0.25,
            "knowledge": 0.35,
            "confidence": 0.4,
            "severity": 0.7,
        }
    ]
    mastery_records = []
    retention_records = []
    knowledge_records = []
    confidence_records = []
    weakness_items = []
    evidence: list[str] = []
    for index, spec in enumerate(specs):
        tid = spec["id"]
        eid = f"e-{tid}"
        evidence.append(eid)
        mastery_records.append(
            TopicMasteryRecord.create(
                tid,
                float(spec.get("mastery", 0.3)),
                confidence="medium",
                evidence_ids=[eid],
            )
        )
        retention_records.append(
            TopicRetentionRecord.create(
                tid,
                float(spec.get("retention", 0.3)),
                confidence="medium",
                evidence_ids=[eid],
            )
        )
        knowledge_records.append(
            TopicKnowledgeRecord.create(
                tid,
                float(spec.get("knowledge", 0.3)),
                confidence="medium",
                evidence_ids=[eid],
            )
        )
        confidence_records.append(
            TopicConfidenceRecord.create(
                tid,
                float(spec.get("confidence", 0.4)),
                evidence_ids=[eid],
            )
        )
        severity = float(spec.get("severity", 0.5))
        if severity > 0.0:
            kind = spec.get("weakness_kind", WeaknessKind.LOW_RETENTION)
            weakness_items.append(
                WeaknessItem.create(
                    tid,
                    kind,
                    severity,
                    confidence=ConfidenceBand.MEDIUM,
                    evidence_ids=[eid],
                    rationale=f"weakness_{index}",
                )
            )

    identity = TwinIdentity.create(twin_id, learner_id, subject_code="CS1")
    version = TwinVersion.create(1, 0, index_safe(topics))
    return TwinSnapshot.create(
        identity,
        version,
        FIXED_TIME,
        knowledge=KnowledgeState.create(knowledge_records, evidence_ids=evidence),
        mastery=MasteryState.create(mastery_records, evidence_ids=evidence),
        retention=RetentionState.create(retention_records, evidence_ids=evidence),
        confidence=ConfidenceState.create(
            topic_records=confidence_records,
            evidence_ids=evidence,
        ),
        readiness=ReadinessState.create(
            readiness,
            confidence=ConfidenceBand.MEDIUM,
            evidence_ids=evidence,
            limiting_topic_ids=[s["id"] for s in specs[:2]],
        ),
        velocity=LearningVelocity.create(
            events_per_day=events_per_day,
            mastery_delta=mastery_delta,
            window_days=7.0,
            confidence=ConfidenceBand.MEDIUM,
            evidence_ids=evidence,
        ),
        weaknesses=WeaknessProfile.create(weakness_items, evidence_ids=evidence),
        history_event_ids=history_event_ids or evidence,
    )


def index_safe(topics: list[dict] | None) -> int:
    return min(len(topics or []), 9)


def make_journey(topic_id: str | None = "topic-1") -> JourneyPositionInput:
    return JourneyPositionInput.create(
        journey_id="journey-1",
        current_topic_id=topic_id,
        progress_ratio=0.4,
    )


def make_curriculum(
    *,
    importance: dict[str, float] | None = None,
    prereq: dict[str, float] | None = None,
    struggle: dict[str, float] | None = None,
    exam_proximity: float = 0.0,
) -> CurriculumContextInput:
    return CurriculumContextInput.create(
        subject_code="CS1",
        topic_importance=importance or {"topic-1": 0.7},
        prerequisite_criticality=prereq or {},
        historical_struggle=struggle or {},
        exam_proximity=exam_proximity,
    )
