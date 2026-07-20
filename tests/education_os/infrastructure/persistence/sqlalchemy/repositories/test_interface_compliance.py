"""Repository interface compliance tests for INF-003 adapters."""

from __future__ import annotations

import inspect

import pytest

from application.ports.repositories import (
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

ADAPTER_PORT_PAIRS = (
    (SqlAlchemyDigitalTwinRepository, DigitalTwinRepository),
    (SqlAlchemyLearningEpisodeRepository, LearningEpisodeRepository),
    (SqlAlchemyEvidenceRepository, EvidenceRepository),
    (SqlAlchemySubjectKnowledgeRepository, SubjectKnowledgeRepository),
    (SqlAlchemyTeachingPlanRepository, TeachingPlanRepository),
    (SqlAlchemyDiagnosisRepository, DiagnosisRepository),
    (SqlAlchemyHypothesisRepository, HypothesisRepository),
    (SqlAlchemyPriorityRepository, PriorityRepository),
    (SqlAlchemyTeachingIntentionRepository, TeachingIntentionRepository),
    (SqlAlchemyTeachingStrategyRepository, TeachingStrategyRepository),
    (SqlAlchemyDecisionRepository, DecisionRepository),
    (SqlAlchemyOrchestratorRepository, OrchestratorRepository),
)


@pytest.mark.parametrize(
    ("adapter", "port"),
    ADAPTER_PORT_PAIRS,
    ids=[pair[0].__name__ for pair in ADAPTER_PORT_PAIRS],
)
def test_adapter_implements_port(adapter: type, port: type) -> None:
    assert issubclass(adapter, port)
    abstract_methods = getattr(port, "__abstractmethods__", frozenset())
    for name in abstract_methods:
        assert hasattr(adapter, name)
        assert not getattr(getattr(adapter, name), "__isabstractmethod__", False)


@pytest.mark.parametrize(
    ("adapter", "port"),
    ADAPTER_PORT_PAIRS,
    ids=[pair[0].__name__ for pair in ADAPTER_PORT_PAIRS],
)
def test_adapter_method_signatures_match_port(adapter: type, port: type) -> None:
    for name in getattr(port, "__abstractmethods__", frozenset()):
        port_params = list(inspect.signature(getattr(port, name)).parameters)
        adapter_params = list(inspect.signature(getattr(adapter, name)).parameters)
        assert adapter_params == port_params
