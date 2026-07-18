"""High-volume matrices to exercise infrastructure integration surface."""

from __future__ import annotations

import pytest

from app.infrastructure.adapters.adaptive_learning import AdaptiveLearningAdapter
from app.infrastructure.adapters.learning_orchestrator import (
    EvidencePortAdapter,
    LearningOrchestratorAdapter,
)
from app.infrastructure.adapters.mission import MissionPortAdapter
from app.infrastructure.adapters.student_twin import StudentTwinAdapter
from app.infrastructure.events.base import IntegrationEvent
from app.infrastructure.events.serialization import EventSerializer
from app.infrastructure.events.types import EVENT_TYPES
from app.infrastructure.persistence.unit_of_work import UnitOfWork
from app.infrastructure.repositories.in_memory import InMemoryAggregateRepository
from tests.infrastructure.helpers import make_request

LEARNERS = tuple(f"vol-L{i}" for i in range(8))
SUBJECTS = tuple(f"vol-S{i}" for i in range(6))
EVENT_SLICE = tuple(EVENT_TYPES)
OPS = ("save", "update", "touch")


@pytest.mark.parametrize("learner_id", LEARNERS)
@pytest.mark.parametrize("subject_id", SUBJECTS)
@pytest.mark.parametrize("event_type", EVENT_SLICE)
def test_event_identity_grid(learner_id, subject_id, event_type):
    event = IntegrationEvent.create(
        event_type,
        {"learner_id": learner_id, "subject_id": subject_id},
        correlation_id=f"{learner_id}:{subject_id}",
        source="volume",
    )
    ser = EventSerializer()
    restored = ser.from_json(ser.to_json(event))
    assert restored.payload["learner_id"] == learner_id
    assert restored.payload["subject_id"] == subject_id
    assert restored.event_type == event_type


@pytest.mark.parametrize("learner_id", LEARNERS)
@pytest.mark.parametrize("subject_id", SUBJECTS)
@pytest.mark.parametrize("op", OPS)
def test_aggregate_repo_op_grid(learner_id, subject_id, op):
    repo = InMemoryAggregateRepository(aggregate_name="DailyMission")
    key = f"{learner_id}:{subject_id}"
    ack = repo.save(key, {"op": op, "subject_id": subject_id})
    assert ack["ok"] is True
    loaded = repo.get(key)
    assert loaded is not None
    assert loaded["op"] == op


@pytest.mark.parametrize("learner_id", LEARNERS[:4])
@pytest.mark.parametrize("subject_id", SUBJECTS[:3])
@pytest.mark.parametrize(
    "event_type",
    (
        "learning_activity_completed",
        "knowledge_check_completed",
        "reflection_submitted",
        "session_completed",
        "mission_completed",
    ),
)
def test_evidence_twin_adaptive_mission_grid(learner_id, subject_id, event_type):
    evidence = EvidencePortAdapter()
    twin = StudentTwinAdapter()
    adaptive = AdaptiveLearningAdapter()
    mission = MissionPortAdapter()
    request = make_request(
        learner_id=learner_id,
        subject_id=subject_id,
        event_type=event_type,
        event_id=f"{learner_id}-{subject_id}-{event_type}",
    )
    ev = evidence.process_evidence(request)
    tw = twin.update_from_evidence(request, evidence_payload=ev)
    dec = adaptive.decide(request, twin_payload=tw, evidence_payload=ev)
    ms = mission.apply_decision(request, decision_payload=dec, twin_payload=tw)
    assert ev["ok"] and tw["ok"] and dec["ok"] and ms["ok"]
    assert dec["next_action_authority"] is True
    assert ms["next_action_authority"] is False


@pytest.mark.parametrize("learner_id", LEARNERS[:3])
@pytest.mark.parametrize("subject_id", SUBJECTS[:3])
def test_orchestrator_uow_grid(learner_id, subject_id):
    orch = LearningOrchestratorAdapter(uow=UnitOfWork())
    response = orch.orchestrate(
        make_request(
            learner_id=learner_id,
            subject_id=subject_id,
            event_id=f"orch-{learner_id}-{subject_id}",
            correlation_id=f"corr-{learner_id}",
        )
    )
    assert response.success is True
    assert response.learner_id == learner_id
