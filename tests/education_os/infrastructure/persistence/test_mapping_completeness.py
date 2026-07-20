"""Mapping completeness tests for INF-001 persistence DTOs."""

from __future__ import annotations

from dataclasses import fields, is_dataclass

import pytest

from infrastructure.persistence.dto import (
    ConceptDTO,
    DecisionDTO,
    DiagnosisDTO,
    DigitalTwinDTO,
    EvidenceRecordDTO,
    HypothesisDTO,
    LearningEpisodeDTO,
    OrchestratorDTO,
    PriorityDTO,
    TeachingIntentionDTO,
    TeachingStrategyDTO,
)
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

ROOT_DTOS = (
    DigitalTwinDTO,
    LearningEpisodeDTO,
    EvidenceRecordDTO,
    ConceptDTO,
    DiagnosisDTO,
    HypothesisDTO,
    PriorityDTO,
    TeachingIntentionDTO,
    TeachingStrategyDTO,
    DecisionDTO,
    OrchestratorDTO,
)

EXPECTED_FIELDS = {
    DigitalTwinDTO: {
        "twin_id",
        "student_id",
        "learner_state",
        "concept_states",
        "misconception_states",
        "evidence_history",
        "intervention_history",
        "retention",
        "confidence",
        "trajectory",
        "status",
    },
    LearningEpisodeDTO: {
        "episode_id",
        "student_id",
        "teaching_goal",
        "teaching_strategy_id",
        "learning_objectives",
        "steps",
        "concept_references",
        "primary_dimension",
        "duration",
        "selection_rationale",
        "status",
        "reflection",
        "outcome",
        "evidence_ids",
    },
    EvidenceRecordDTO: {
        "evidence_id",
        "student_id",
        "items",
        "source",
        "context",
        "confidence",
        "strength",
        "timestamp",
        "known_concept_ids",
        "known_episode_ids",
        "concept_references",
        "learning_episode_ids",
        "status",
        "invalidation_reason",
    },
    ConceptDTO: {
        "concept_id",
        "canonical_name",
        "core_meaning",
        "boundary",
        "learning_objectives",
        "representations",
        "misconceptions",
        "application_contexts",
        "transfer_contexts",
        "dependencies",
    },
    DiagnosisDTO: {
        "diagnosis_id",
        "student_id",
        "diagnosis_type",
        "scope",
        "confidence",
        "severity",
        "indicators",
        "reasons",
        "known_evidence_ids",
        "known_interpretation_ids",
        "interpretation_references",
        "status",
        "invalidation_reason",
    },
    HypothesisDTO: {
        "hypothesis_id",
        "student_id",
        "hypothesis_kind",
        "explanation",
        "scope",
        "plausibility",
        "explanatory_strength",
        "diagnosis_references",
        "reasons",
        "interpretation_references",
        "evidence_ids",
        "competing_hypotheses",
        "known_evidence_ids",
        "known_interpretation_ids",
        "status",
        "discard_reason",
    },
    PriorityDTO: {
        "priority_id",
        "student_id",
        "scope",
        "diagnosis_references",
        "hypothesis_references",
        "factors",
        "score",
        "urgency",
        "instructional_impact",
        "constraints",
        "status",
        "stabilisation_reason",
    },
    TeachingIntentionDTO: {
        "intention_id",
        "student_id",
        "intention_type",
        "goal",
        "scope",
        "expected_outcome",
        "strength",
        "priority_references",
        "diagnosis_references",
        "hypothesis_references",
        "constraints",
        "status",
        "retire_reason",
    },
    TeachingStrategyDTO: {
        "strategy_id",
        "student_id",
        "primary_strategy",
        "goal",
        "rationale",
        "effectiveness",
        "complexity",
        "intention_references",
        "diagnosis_references",
        "hypothesis_references",
        "secondary_strategies",
        "constraints",
        "composition_pattern",
        "status",
        "retire_reason",
    },
    DecisionDTO: {
        "decision_id",
        "student_id",
        "priority_references",
        "intention_references",
        "strategy_references",
        "indicators",
        "constraints",
        "reasons",
        "confidence",
        "readiness",
        "status",
        "outcome",
        "reconsideration_reason",
    },
    OrchestratorDTO: {
        "orchestrator_id",
        "student_id",
        "decision_reference",
        "strategy_references",
        "plan",
        "episode_references",
        "state",
    },
}


@pytest.mark.parametrize("dto_cls", ROOT_DTOS, ids=lambda cls: cls.__name__)
def test_root_dto_is_frozen_dataclass(dto_cls: type) -> None:
    assert is_dataclass(dto_cls)
    assert dto_cls.__dataclass_params__.frozen is True


@pytest.mark.parametrize("dto_cls", ROOT_DTOS, ids=lambda cls: cls.__name__)
def test_root_dto_field_completeness(dto_cls: type) -> None:
    actual = {field.name for field in fields(dto_cls)}
    assert actual == EXPECTED_FIELDS[dto_cls]


def test_known_allow_lists_remain_sorted_after_round_trip() -> None:
    evidence_dto = EvidenceMapper.to_persistence(build_evidence())
    assert evidence_dto.known_concept_ids == tuple(
        sorted(evidence_dto.known_concept_ids)
    )
    assert evidence_dto.known_episode_ids == tuple(
        sorted(evidence_dto.known_episode_ids)
    )

    diagnosis_dto = DiagnosisMapper.to_persistence(build_diagnosis())
    assert diagnosis_dto.known_evidence_ids == tuple(
        sorted(diagnosis_dto.known_evidence_ids)
    )
    assert diagnosis_dto.known_interpretation_ids == tuple(
        sorted(diagnosis_dto.known_interpretation_ids)
    )

    hypothesis_dto = HypothesisMapper.to_persistence(build_hypothesis())
    assert hypothesis_dto.known_evidence_ids == tuple(
        sorted(hypothesis_dto.known_evidence_ids)
    )
    assert hypothesis_dto.known_interpretation_ids == tuple(
        sorted(hypothesis_dto.known_interpretation_ids)
    )


def test_mappers_cover_all_aggregates() -> None:
    pairs = (
        (DigitalTwinMapper, build_digital_twin),
        (LearningEpisodeMapper, build_learning_episode),
        (EvidenceMapper, build_evidence),
        (SubjectKnowledgeMapper, build_concept),
        (DiagnosisMapper, build_diagnosis),
        (HypothesisMapper, build_hypothesis),
        (PriorityMapper, build_priority),
        (TeachingIntentionMapper, build_intention),
        (TeachingStrategyMapper, build_strategy),
        (DecisionMapper, build_decision),
        (OrchestratorMapper, build_orchestrator),
    )
    for mapper, builder in pairs:
        dto = mapper.to_persistence(builder())
        restored = mapper.to_domain(dto)
        assert mapper.to_persistence(restored) == dto
