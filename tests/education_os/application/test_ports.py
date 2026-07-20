"""Port contract tests — interfaces only, no implementations in application."""

from __future__ import annotations

import inspect
from abc import ABC

import pytest

from application.ports import (
    ApplicationEventPublisher,
    Clock,
    DecisionRepository,
    DiagnosisRepository,
    DigitalTwinRepository,
    EvidenceRepository,
    HypothesisRepository,
    LearningEpisodeRepository,
    OrchestratorRepository,
    PriorityRepository,
    SubjectKnowledgeRepository,
    TeachingIntentionRepository,
    TeachingPlanRepository,
    TeachingStrategyRepository,
    TransactionManager,
    UnitOfWork,
    UUIDGenerator,
)
from domain.education.foundation.ids import (
    ConceptId,
    DecisionId,
    DiagnosisId,
    DigitalTwinId,
    EvidenceId,
    HypothesisId,
    LearningEpisodeId,
    OrchestratorId,
    PriorityId,
    TeachingIntentionId,
    TeachingStrategyId,
)

REPOSITORY_PORTS = [
    DigitalTwinRepository,
    LearningEpisodeRepository,
    EvidenceRepository,
    SubjectKnowledgeRepository,
    TeachingPlanRepository,
    DiagnosisRepository,
    HypothesisRepository,
    PriorityRepository,
    TeachingIntentionRepository,
    TeachingStrategyRepository,
    DecisionRepository,
    OrchestratorRepository,
]

INFRASTRUCTURE_PORTS = [
    ApplicationEventPublisher,
    Clock,
    UUIDGenerator,
    TransactionManager,
    UnitOfWork,
]


@pytest.mark.parametrize("port", REPOSITORY_PORTS + INFRASTRUCTURE_PORTS)
def test_ports_are_abstract(port: type) -> None:
    assert issubclass(port, ABC)
    assert inspect.isabstract(port)


@pytest.mark.parametrize("port", REPOSITORY_PORTS + INFRASTRUCTURE_PORTS)
def test_ports_cannot_be_instantiated(port: type) -> None:
    with pytest.raises(TypeError):
        port()  # type: ignore[misc]


def test_digital_twin_repository_contract() -> None:
    assert hasattr(DigitalTwinRepository, "get")
    assert hasattr(DigitalTwinRepository, "get_by_student")
    assert hasattr(DigitalTwinRepository, "save")
    sig = inspect.signature(DigitalTwinRepository.get)
    assert "twin_id" in sig.parameters


def test_learning_episode_repository_contract() -> None:
    assert hasattr(LearningEpisodeRepository, "get")
    assert hasattr(LearningEpisodeRepository, "list_by_student")
    assert hasattr(LearningEpisodeRepository, "save")


def test_evidence_repository_contract() -> None:
    assert hasattr(EvidenceRepository, "get")
    assert hasattr(EvidenceRepository, "list_by_student")
    assert hasattr(EvidenceRepository, "save")


def test_subject_knowledge_repository_contract() -> None:
    assert hasattr(SubjectKnowledgeRepository, "get_concept")
    assert hasattr(SubjectKnowledgeRepository, "save_concept")
    assert hasattr(SubjectKnowledgeRepository, "exists")


def test_teaching_plan_repository_contract() -> None:
    assert hasattr(TeachingPlanRepository, "get_episode_id")
    assert hasattr(TeachingPlanRepository, "get_plan_id")
    assert hasattr(TeachingPlanRepository, "save")


@pytest.mark.parametrize(
    ("port", "methods"),
    [
        (DiagnosisRepository, ("get", "list_by_student", "save")),
        (HypothesisRepository, ("get", "list_by_student", "save")),
        (PriorityRepository, ("get", "list_by_student", "save")),
        (TeachingIntentionRepository, ("get", "list_by_student", "save")),
        (TeachingStrategyRepository, ("get", "list_by_student", "save")),
        (DecisionRepository, ("get", "list_by_student", "save")),
        (OrchestratorRepository, ("get", "list_by_student", "save")),
    ],
)
def test_aggregate_repository_contracts(port: type, methods: tuple[str, ...]) -> None:
    for method in methods:
        assert hasattr(port, method)


def test_clock_contract() -> None:
    assert hasattr(Clock, "now")
    sig = inspect.signature(Clock.now)
    assert list(sig.parameters) == ["self"]


def test_uuid_generator_contract() -> None:
    assert hasattr(UUIDGenerator, "new_id")


def test_transaction_manager_contract() -> None:
    for method in ("begin", "commit", "rollback"):
        assert hasattr(TransactionManager, method)


def test_unit_of_work_contract() -> None:
    for method in ("begin", "commit", "rollback"):
        assert hasattr(UnitOfWork, method)
    for repo in (
        "digital_twins",
        "episodes",
        "evidence",
        "subject_knowledge",
        "diagnosis",
        "hypothesis",
        "priority",
        "teaching_intention",
        "teaching_strategy",
        "decision",
        "orchestrator",
        "teaching_plan",
    ):
        assert hasattr(UnitOfWork, repo)
    assert hasattr(UnitOfWork, "is_active")
    assert hasattr(UnitOfWork, "__enter__")
    assert hasattr(UnitOfWork, "__exit__")


def test_identity_types_used_by_ports() -> None:
    assert DigitalTwinId("twin-001").value == "twin-001"
    assert LearningEpisodeId("episode-001").value == "episode-001"
    assert EvidenceId("evidence-001").value == "evidence-001"
    assert ConceptId("concept-001").value == "concept-001"
    assert DiagnosisId("diagnosis-001").value == "diagnosis-001"
    assert HypothesisId("hypothesis-001").value == "hypothesis-001"
    assert PriorityId("priority-001").value == "priority-001"
    assert TeachingIntentionId("intention-001").value == "intention-001"
    assert TeachingStrategyId("strategy-001").value == "strategy-001"
    assert DecisionId("decision-001").value == "decision-001"
    assert OrchestratorId("orchestrator-001").value == "orchestrator-001"
