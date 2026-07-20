"""Round-trip and lossless conversion tests for INF-001 mappers."""

from __future__ import annotations

import pytest

from infrastructure.persistence.mappers import (
    DecisionMapper,
    DiagnosisMapper,
    DigitalTwinMapper,
    EvidenceMapper,
    HypothesisMapper,
    LearningEpisodeMapper,
    OrchestratorMapper,
    PriorityMapper,
    SubjectKnowledgeMapper,
    TeachingIntentionMapper,
    TeachingStrategyMapper,
)
from tests.education_os.infrastructure.persistence.conftest import (
    build_concept,
    build_decision,
    build_diagnosis,
    build_digital_twin,
    build_evidence,
    build_hypothesis,
    build_intention,
    build_learning_episode,
    build_orchestrator,
    build_priority,
    build_strategy,
)

ROUND_TRIPS = (
    ("digital_twin", DigitalTwinMapper, build_digital_twin, "twin_id"),
    ("learning_episode", LearningEpisodeMapper, build_learning_episode, "episode_id"),
    ("evidence", EvidenceMapper, build_evidence, "evidence_id"),
    ("concept", SubjectKnowledgeMapper, build_concept, "concept_id"),
    ("diagnosis", DiagnosisMapper, build_diagnosis, "diagnosis_id"),
    ("hypothesis", HypothesisMapper, build_hypothesis, "hypothesis_id"),
    ("priority", PriorityMapper, build_priority, "priority_id"),
    ("teaching_intention", TeachingIntentionMapper, build_intention, "intention_id"),
    ("teaching_strategy", TeachingStrategyMapper, build_strategy, "strategy_id"),
    ("decision", DecisionMapper, build_decision, "decision_id"),
    ("orchestrator", OrchestratorMapper, build_orchestrator, "orchestrator_id"),
)


@pytest.mark.parametrize(
    ("label", "mapper", "builder", "id_attr"),
    ROUND_TRIPS,
    ids=[item[0] for item in ROUND_TRIPS],
)
def test_round_trip_is_lossless(label: str, mapper, builder, id_attr: str) -> None:
    aggregate = builder()
    if hasattr(aggregate, "pull_events"):
        aggregate.pull_events()

    dto = mapper.to_persistence(aggregate)
    restored = mapper.to_domain(dto)
    if hasattr(restored, "pull_events"):
        assert restored.pull_events() == []

    dto_again = mapper.to_persistence(restored)
    assert dto_again == dto

    original_id = getattr(aggregate, id_attr)
    restored_id = getattr(restored, id_attr)
    assert restored_id == original_id
    if hasattr(aggregate, "student_id"):
        assert restored.student_id == aggregate.student_id
