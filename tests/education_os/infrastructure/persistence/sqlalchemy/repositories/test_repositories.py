"""CRUD and round-trip persistence tests for INF-003 repositories."""

from __future__ import annotations

import pytest

from domain.education.foundation.ids import LearningEpisodeId
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
from infrastructure.persistence.sqlalchemy.repositories import (
    SqlAlchemyDecisionRepository,
    SqlAlchemyDiagnosisRepository,
    SqlAlchemyDigitalTwinRepository,
    SqlAlchemyEvidenceRepository,
    SqlAlchemyHypothesisRepository,
    SqlAlchemyLearningEpisodeRepository,
    SqlAlchemyOrchestratorRepository,
    SqlAlchemyPriorityRepository,
    SqlAlchemySubjectKnowledgeRepository,
    SqlAlchemyTeachingIntentionRepository,
    SqlAlchemyTeachingPlanRepository,
    SqlAlchemyTeachingStrategyRepository,
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

AGGREGATE_CASES = (
    (
        "digital_twin",
        SqlAlchemyDigitalTwinRepository,
        build_digital_twin,
        DigitalTwinMapper,
        "get",
        "twin_id",
        "save",
    ),
    (
        "learning_episode",
        SqlAlchemyLearningEpisodeRepository,
        build_learning_episode,
        LearningEpisodeMapper,
        "get",
        "episode_id",
        "save",
    ),
    (
        "evidence",
        SqlAlchemyEvidenceRepository,
        build_evidence,
        EvidenceMapper,
        "get",
        "evidence_id",
        "save",
    ),
    (
        "diagnosis",
        SqlAlchemyDiagnosisRepository,
        build_diagnosis,
        DiagnosisMapper,
        "get",
        "diagnosis_id",
        "save",
    ),
    (
        "hypothesis",
        SqlAlchemyHypothesisRepository,
        build_hypothesis,
        HypothesisMapper,
        "get",
        "hypothesis_id",
        "save",
    ),
    (
        "priority",
        SqlAlchemyPriorityRepository,
        build_priority,
        PriorityMapper,
        "get",
        "priority_id",
        "save",
    ),
    (
        "teaching_intention",
        SqlAlchemyTeachingIntentionRepository,
        build_intention,
        TeachingIntentionMapper,
        "get",
        "intention_id",
        "save",
    ),
    (
        "teaching_strategy",
        SqlAlchemyTeachingStrategyRepository,
        build_strategy,
        TeachingStrategyMapper,
        "get",
        "strategy_id",
        "save",
    ),
    (
        "decision",
        SqlAlchemyDecisionRepository,
        build_decision,
        DecisionMapper,
        "get",
        "decision_id",
        "save",
    ),
    (
        "orchestrator",
        SqlAlchemyOrchestratorRepository,
        build_orchestrator,
        OrchestratorMapper,
        "get",
        "orchestrator_id",
        "save",
    ),
)


@pytest.mark.parametrize(
    ("label", "repo_cls", "builder", "mapper", "get_name", "id_attr", "save_name"),
    AGGREGATE_CASES,
    ids=[item[0] for item in AGGREGATE_CASES],
)
def test_aggregate_round_trip(
    session,
    label: str,
    repo_cls,
    builder,
    mapper,
    get_name: str,
    id_attr: str,
    save_name: str,
) -> None:
    aggregate = builder()
    if hasattr(aggregate, "pull_events"):
        aggregate.pull_events()

    repo = repo_cls(session)
    getattr(repo, save_name)(aggregate)
    session.commit()

    loaded = getattr(repo, get_name)(getattr(aggregate, id_attr))
    assert loaded is not None
    if hasattr(loaded, "pull_events"):
        assert loaded.pull_events() == []

    assert mapper.to_persistence(loaded) == mapper.to_persistence(aggregate)


def test_digital_twin_get_by_student(session) -> None:
    twin = build_digital_twin()
    twin.pull_events()
    repo = SqlAlchemyDigitalTwinRepository(session)
    repo.save(twin)
    session.commit()

    loaded = repo.get_by_student(twin.student_id)
    assert loaded is not None
    assert loaded.twin_id == twin.twin_id


@pytest.mark.parametrize(
    ("repo_cls", "builder", "id_attr"),
    [
        (SqlAlchemyLearningEpisodeRepository, build_learning_episode, "episode_id"),
        (SqlAlchemyEvidenceRepository, build_evidence, "evidence_id"),
        (SqlAlchemyDiagnosisRepository, build_diagnosis, "diagnosis_id"),
        (SqlAlchemyHypothesisRepository, build_hypothesis, "hypothesis_id"),
        (SqlAlchemyPriorityRepository, build_priority, "priority_id"),
        (SqlAlchemyTeachingIntentionRepository, build_intention, "intention_id"),
        (SqlAlchemyTeachingStrategyRepository, build_strategy, "strategy_id"),
        (SqlAlchemyDecisionRepository, build_decision, "decision_id"),
        (SqlAlchemyOrchestratorRepository, build_orchestrator, "orchestrator_id"),
    ],
    ids=[
        "episode",
        "evidence",
        "diagnosis",
        "hypothesis",
        "priority",
        "intention",
        "strategy",
        "decision",
        "orchestrator",
    ],
)
def test_list_by_student(session, repo_cls, builder, id_attr) -> None:
    aggregate = builder()
    aggregate.pull_events()
    repo = repo_cls(session)
    repo.save(aggregate)
    session.commit()

    listed = repo.list_by_student(aggregate.student_id)
    assert len(listed) == 1
    assert getattr(listed[0], id_attr) == getattr(aggregate, id_attr)


def test_subject_knowledge_round_trip_and_exists(session) -> None:
    concept = build_concept()
    repo = SqlAlchemySubjectKnowledgeRepository(session)

    assert repo.exists(concept.concept_id) is False
    repo.save_concept(concept)
    session.commit()

    assert repo.exists(concept.concept_id) is True
    loaded = repo.get_concept(concept.concept_id)
    assert loaded is not None
    assert SubjectKnowledgeMapper.to_persistence(
        loaded
    ) == SubjectKnowledgeMapper.to_persistence(concept)


def test_aggregate_save_replaces(session) -> None:
    twin = build_digital_twin()
    twin.pull_events()
    repo = SqlAlchemyDigitalTwinRepository(session)
    repo.save(twin)
    session.commit()

    # Re-save identical identity — upsert must not fail.
    repo.save(twin)
    session.commit()
    assert repo.get(twin.twin_id) is not None


def test_teaching_plan_binding_round_trip(session) -> None:
    repo = SqlAlchemyTeachingPlanRepository(session)
    episode_id = LearningEpisodeId("episode-plan-001")

    assert repo.get_episode_id("plan-001") is None
    assert repo.get_plan_id(episode_id) is None

    repo.save("plan-001", episode_id)
    session.commit()

    assert repo.get_episode_id("plan-001") == episode_id
    assert repo.get_plan_id(episode_id) == "plan-001"

    # Rebind episode to a new plan — old plan binding cleared.
    repo.save("plan-002", episode_id)
    session.commit()
    assert repo.get_episode_id("plan-001") is None
    assert repo.get_episode_id("plan-002") == episode_id
    assert repo.get_plan_id(episode_id) == "plan-002"


def test_get_missing_returns_none(session) -> None:
    from domain.education.foundation.ids import DigitalTwinId

    repo = SqlAlchemyDigitalTwinRepository(session)
    assert repo.get(DigitalTwinId("missing-twin")) is None
