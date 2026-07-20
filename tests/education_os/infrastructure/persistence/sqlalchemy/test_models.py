"""Metadata creation, model integrity, and schema completeness (INF-002)."""

from __future__ import annotations

from dataclasses import fields

import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import DeclarativeBase, Session

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
from infrastructure.persistence.sqlalchemy import (
    NAMING_CONVENTION,
    Base,
    ConceptModel,
    DecisionModel,
    DiagnosisModel,
    DigitalTwinModel,
    EvidenceModel,
    HypothesisModel,
    LearningEpisodeModel,
    OrchestratorModel,
    PriorityModel,
    TeachingIntentionModel,
    TeachingPlanModel,
    TeachingStrategyModel,
    create_session_factory,
    metadata,
)

MODEL_DTO_PAIRS = (
    (DigitalTwinModel, DigitalTwinDTO, "eos_digital_twins"),
    (LearningEpisodeModel, LearningEpisodeDTO, "eos_learning_episodes"),
    (EvidenceModel, EvidenceRecordDTO, "eos_evidence_records"),
    (ConceptModel, ConceptDTO, "eos_concepts"),
    (DiagnosisModel, DiagnosisDTO, "eos_diagnoses"),
    (HypothesisModel, HypothesisDTO, "eos_hypotheses"),
    (PriorityModel, PriorityDTO, "eos_priorities"),
    (TeachingIntentionModel, TeachingIntentionDTO, "eos_teaching_intentions"),
    (TeachingStrategyModel, TeachingStrategyDTO, "eos_teaching_strategies"),
    (DecisionModel, DecisionDTO, "eos_decisions"),
    (OrchestratorModel, OrchestratorDTO, "eos_orchestrators"),
)

STUDENT_SCOPED_MODELS = tuple(
    model for model, _, _ in MODEL_DTO_PAIRS if model is not ConceptModel
)
ALL_MODELS = tuple(pair[0] for pair in MODEL_DTO_PAIRS) + (TeachingPlanModel,)


def test_base_uses_shared_metadata_and_naming_convention() -> None:
    assert issubclass(Base, DeclarativeBase)
    assert Base.metadata is metadata
    assert metadata.naming_convention == NAMING_CONVENTION
    for key in ("ix", "uq", "ck", "fk", "pk"):
        assert key in NAMING_CONVENTION


def test_metadata_create_all_builds_schema() -> None:
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    inspector = inspect(engine)
    table_names = set(inspector.get_table_names())
    expected = {table for _, _, table in MODEL_DTO_PAIRS} | {"eos_teaching_plans"}
    assert expected.issubset(table_names)


@pytest.mark.parametrize(
    ("model_cls", "dto_cls", "table_name"),
    MODEL_DTO_PAIRS,
    ids=[pair[0].__name__ for pair in MODEL_DTO_PAIRS],
)
def test_model_table_and_column_completeness(
    model_cls: type,
    dto_cls: type,
    table_name: str,
) -> None:
    assert model_cls.__tablename__ == table_name
    assert issubclass(model_cls, Base)
    dto_field_names = {field.name for field in fields(dto_cls)}
    column_names = {column.name for column in model_cls.__table__.columns}
    assert column_names == dto_field_names


@pytest.mark.parametrize("model_cls", ALL_MODELS, ids=lambda cls: cls.__name__)
def test_model_has_string_primary_key(model_cls: type) -> None:
    primary = list(model_cls.__table__.primary_key.columns)
    assert len(primary) == 1
    assert primary[0].name.endswith("_id") or primary[0].name in {
        "twin_id",
        "episode_id",
        "evidence_id",
        "concept_id",
        "plan_id",
        "diagnosis_id",
        "hypothesis_id",
        "priority_id",
        "intention_id",
        "strategy_id",
        "decision_id",
        "orchestrator_id",
    }


@pytest.mark.parametrize(
    "model_cls",
    STUDENT_SCOPED_MODELS,
    ids=lambda cls: cls.__name__,
)
def test_model_indexes_student_id(model_cls: type) -> None:
    assert "student_id" in model_cls.__table__.columns
    indexed = {
        column.name
        for index in model_cls.__table__.indexes
        for column in index.columns
    }
    # mapped_column(..., index=True) registers an Index on student_id
    student_col = model_cls.__table__.columns["student_id"]
    assert student_col.index or "student_id" in indexed


def test_teaching_plan_model_schema() -> None:
    assert TeachingPlanModel.__tablename__ == "eos_teaching_plans"
    column_names = {column.name for column in TeachingPlanModel.__table__.columns}
    assert column_names == {"plan_id", "episode_id"}


def test_session_factory_persists_and_loads_row() -> None:
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    session_factory = create_session_factory(engine)

    with session_factory() as session:
        assert isinstance(session, Session)
        row = DigitalTwinModel(
            twin_id="twin-001",
            student_id="student-ada",
            learner_state={"learner_state_id": "ls-1", "student_id": "student-ada"},
            concept_states=[],
            misconception_states=[],
            evidence_history=[],
            intervention_history=[],
            retention={"band": "stable"},
            confidence={"overall": "moderate"},
            trajectory={"points": []},
            status="active",
        )
        session.add(row)
        session.commit()

    with session_factory() as session:
        loaded = session.get(DigitalTwinModel, "twin-001")
        assert loaded is not None
        assert loaded.student_id == "student-ada"
        assert loaded.status == "active"
        assert loaded.retention == {"band": "stable"}


def test_all_models_registered_on_shared_metadata() -> None:
    registered = set(metadata.tables)
    expected = {table for _, _, table in MODEL_DTO_PAIRS} | {"eos_teaching_plans"}
    assert expected.issubset(registered)
