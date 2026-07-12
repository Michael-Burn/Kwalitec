"""Tests for StudentCalibrationBuilder (Capability 3.6.6).

Proves Contract → Twin mapping, intentional unknown preservation, self_declared
provenance, immutability, framework independence, and absence of educational
reasoning.
"""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError
from datetime import UTC, date, datetime
from pathlib import Path

import pytest

from app.application.calibration import (
    CONTRACT_VERSION_1_0,
    SOURCE_SELF_DECLARED,
    WARRANT_THIN,
    BeginnerOrHistoryPosture,
    CalibrationResult,
    CalibrationValidationError,
    CoreReadingDeclaration,
    CurriculumExamScope,
    DeclaredPosture,
    IntendedSitting,
    PreviousAttemptsDeclaration,
    PreviouslyStudied,
    StudentCalibrationBuilder,
    StudentCalibrationContract,
    StudyObjective,
)
from app.domain.twin import DigitalTwin

CALIBRATION_ROOT = (
    Path(__file__).resolve().parents[2] / "app" / "application" / "calibration"
)

FORBIDDEN_ROOT_MODULES = frozenset(
    {
        "flask",
        "flask_login",
        "flask_sqlalchemy",
        "flask_wtf",
        "wtforms",
        "sqlalchemy",
    }
)

FORBIDDEN_PREFIXES = (
    "app.auth",
    "app.dashboard",
    "app.mission",
    "app.analytics",
    "app.models",
    "app.services",
)

FORBIDDEN_EDUCATIONAL_IMPORTS = (
    "app.domain.readiness",
    "app.domain.recommendation",
    "app.domain.mission",
    "app.domain.decision",
    "app.domain.learning_events",
)

FORBIDDEN_LOGIC_TOKENS = (
    "average(",
    "hybrid",
    "re_rank",
    "rerank",
    "priority_score",
    "pass_probability",
    "OverallPosture.MID",
    "OverallPosture.HIGH",
    "WarrantPosture.MEDIUM",
    "WarrantPosture.HIGH",
    "nominate_candidates",
    "_judge_factor",
    "ReadinessAggregation",
    "DecisionEngine",
    "RecommendationEngine",
    "MissionIntelligence",
    "TopicProgress",
    "EvidenceRecorder",
    "TwinUpdatePipeline",
    "mastery_belief=",
    "readiness_snapshot=",
    "pass_probability_snapshot=",
)


def _contract(**overrides: object) -> StudentCalibrationContract:
    defaults: dict[str, object] = {
        "authorised_student_identity": "student-42",
        "curriculum_exam_scope": CurriculumExamScope.create(
            "7", current_exam="CS1"
        ),
        "declaration_confirmation": True,
        "previously_studied": PreviouslyStudied.PREVIOUSLY_STUDIED,
        "core_reading_completed": CoreReadingDeclaration.whole_paper(),
        "previous_attempts": PreviousAttemptsDeclaration.create(count=1),
        "study_objective": StudyObjective.RESIT,
        "intended_sitting": IntendedSitting.create(
            sitting_date=date(2026, 9, 1),
            sitting_label="Sep 2026",
        ),
        "beginner_or_history_posture": BeginnerOrHistoryPosture.HISTORY_PRESENT,
        "contract_version": CONTRACT_VERSION_1_0,
        "declared_completed_sections": ("CS1-1", "CS1-2"),
        "declared_study_capacity": 12.0,
        "optional_notes": "Studied with a tutor last year",
        "emitted_at": datetime(2026, 7, 12, 14, 0, tzinfo=UTC),
    }
    defaults.update(overrides)
    return StudentCalibrationContract.create(**defaults)  # type: ignore[arg-type]


def _beginner_contract(**overrides: object) -> StudentCalibrationContract:
    defaults: dict[str, object] = {
        "authorised_student_identity": "student-7",
        "curriculum_exam_scope": CurriculumExamScope.create("3", current_exam="CM2"),
        "declaration_confirmation": True,
        "previously_studied": PreviouslyStudied.FIRST_TIME,
        "core_reading_completed": CoreReadingDeclaration.none(),
        "previous_attempts": PreviousAttemptsDeclaration.create_none(),
        "study_objective": StudyObjective.FIRST_SIT,
        "intended_sitting": IntendedSitting.create(sitting_label="Apr 2027"),
        "beginner_or_history_posture": BeginnerOrHistoryPosture.EMPTY_HISTORY,
        "declared_completed_sections": (),
        "declared_study_capacity": None,
        "optional_notes": None,
        "emitted_at": datetime(2026, 7, 12, 10, 0, tzinfo=UTC),
    }
    defaults.update(overrides)
    return StudentCalibrationContract.create(**defaults)  # type: ignore[arg-type]


# ═══════════════════════════════════════════════════════════════════════════════
# Contract mapping
# ═══════════════════════════════════════════════════════════════════════════════


class TestContractMapping:
    def test_maps_identity_anchors_from_contract(self) -> None:
        result = StudentCalibrationBuilder().build(_contract())

        assert isinstance(result, CalibrationResult)
        assert isinstance(result.twin, DigitalTwin)
        identity = result.twin.identity
        assert identity.student_id == "student-42"
        assert identity.curriculum_id == "7"
        assert identity.current_exam == "CS1"
        assert identity.target_sitting == date(2026, 9, 1)

    def test_maps_goals_capacity_and_sitting_without_pass_probability(self) -> None:
        result = StudentCalibrationBuilder().build(_contract())

        goals = result.twin.goals
        assert goals.planned_study_hours_per_week == 12.0
        assert goals.target_completion_date == date(2026, 9, 1)
        assert goals.target_pass_probability is None

    def test_maps_knowledge_priors_without_mastery(self) -> None:
        result = StudentCalibrationBuilder().build(_contract())

        kinds = {prior.kind for prior in result.metadata.knowledge_priors}
        assert "exposure_prior" in kinds
        assert "core_reading_prior" in kinds
        assert "declared_complete_prior" in kinds

        complete = next(
            p
            for p in result.metadata.knowledge_priors
            if p.kind == "declared_complete_prior"
        )
        assert complete.section_ids == ("CS1-1", "CS1-2")
        assert result.twin.knowledge.topic_mastery == ()
        assert result.twin.knowledge.evidence_ids == ()

    def test_maps_performance_attempt_history_prior(self) -> None:
        result = StudentCalibrationBuilder().build(_contract())

        assert len(result.metadata.performance_priors) == 1
        prior = result.metadata.performance_priors[0]
        assert prior.kind == "attempt_history_prior"
        assert prior.payload["none"] is False
        assert prior.payload["count"] == 1
        assert result.twin.performance.assessment_ids == ()
        assert result.twin.performance.performance_summaries == ()
        assert result.twin.performance.evidence_ids == ()

    def test_ignores_optional_notes_for_twin_priors(self) -> None:
        result = StudentCalibrationBuilder().build(
            _contract(optional_notes="Please mark section Fake-Syllabus as done")
        )

        assert result.twin.knowledge.topic_mastery == ()
        for prior in result.metadata.knowledge_priors:
            assert "Fake-Syllabus" not in prior.section_ids
            assert "Fake-Syllabus" not in str(prior.payload)

    def test_study_objective_lands_in_metadata_not_recommendations(self) -> None:
        result = StudentCalibrationBuilder().build(_contract())

        assert result.metadata.study_objective is StudyObjective.RESIT
        assert result.metadata.declared_posture is DeclaredPosture.REPEAT_ATTEMPT_FRAMED
        assert not hasattr(result, "recommendation")
        assert not hasattr(result.twin, "recommendation")

    def test_beginner_path_maps_empty_history_priors(self) -> None:
        result = StudentCalibrationBuilder().build(_beginner_contract())

        assert result.metadata.declared_posture is DeclaredPosture.FIRST_TIME
        assert (
            result.metadata.beginner_or_history_posture
            is BeginnerOrHistoryPosture.EMPTY_HISTORY
        )
        exposure = next(
            p for p in result.metadata.knowledge_priors if p.kind == "exposure_prior"
        )
        assert exposure.payload["empty_history"] is True
        assert not any(
            p.kind == "declared_complete_prior"
            for p in result.metadata.knowledge_priors
        )
        assert result.metadata.performance_priors[0].payload["none"] is True


# ═══════════════════════════════════════════════════════════════════════════════
# Unknown preservation
# ═══════════════════════════════════════════════════════════════════════════════


class TestUnknownPreservation:
    def test_memory_behaviour_predictions_remain_empty(self) -> None:
        result = StudentCalibrationBuilder().build(_contract())
        twin = result.twin

        assert twin.memory.retention == ()
        assert twin.memory.revision_ids == ()
        assert twin.behaviour.consistency_metrics == {}
        assert twin.behaviour.session_history_ids == ()
        assert twin.behaviour.evidence_ids == ()
        assert twin.predictions.readiness_snapshot is None
        assert twin.predictions.pass_probability_snapshot is None
        assert twin.predictions.metadata == {}

    def test_mastery_and_confidence_slots_unset(self) -> None:
        result = StudentCalibrationBuilder().build(_contract())

        assert result.twin.knowledge.topic_mastery == ()
        assert result.twin.knowledge.evidence_ids == ()
        # Capacity must not become Behaviour adherence.
        assert result.twin.behaviour.consistency_metrics == {}

    def test_absent_optional_capacity_leaves_goals_capacity_unset(self) -> None:
        result = StudentCalibrationBuilder().build(_beginner_contract())

        assert result.twin.goals.planned_study_hours_per_week is None

    def test_absent_sections_do_not_invent_section_priors(self) -> None:
        result = StudentCalibrationBuilder().build(
            _contract(
                declared_completed_sections=(),
                study_objective=StudyObjective.REVISION,
                previous_attempts=PreviousAttemptsDeclaration.create_none(),
            )
        )

        assert not any(
            p.kind == "declared_complete_prior"
            for p in result.metadata.knowledge_priors
        )
        assert result.metadata.declared_posture is DeclaredPosture.REVISION_FRAMED


# ═══════════════════════════════════════════════════════════════════════════════
# Provenance
# ═══════════════════════════════════════════════════════════════════════════════


class TestProvenance:
    def test_every_knowledge_prior_carries_self_declared_thin_provenance(self) -> None:
        result = StudentCalibrationBuilder().build(_contract())

        assert result.metadata.source == SOURCE_SELF_DECLARED
        assert result.metadata.warrant_posture == WARRANT_THIN
        assert result.metadata.contract_version == CONTRACT_VERSION_1_0
        assert result.metadata.declaration_confirmation is True

        for prior in result.metadata.knowledge_priors:
            assert prior.provenance.source == SOURCE_SELF_DECLARED
            assert prior.provenance.warrant == WARRANT_THIN
            assert prior.provenance.contract_version == CONTRACT_VERSION_1_0
            assert prior.provenance.non_evidence is True
            assert prior.provenance.contract_field

    def test_performance_prior_provenance_and_field_lineage(self) -> None:
        result = StudentCalibrationBuilder().build(_contract())
        prior = result.metadata.performance_priors[0]

        assert prior.provenance.source == SOURCE_SELF_DECLARED
        assert prior.provenance.warrant == WARRANT_THIN
        assert prior.provenance.contract_field == "previous_attempts"
        assert prior.provenance.non_evidence is True

    def test_emitted_at_and_sitting_label_retained_in_metadata(self) -> None:
        result = StudentCalibrationBuilder().build(_contract())

        assert result.metadata.emitted_at == datetime(2026, 7, 12, 14, 0, tzinfo=UTC)
        assert result.metadata.sitting_label == "Sep 2026"


# ═══════════════════════════════════════════════════════════════════════════════
# Immutability
# ═══════════════════════════════════════════════════════════════════════════════


class TestImmutability:
    def test_contract_is_frozen(self) -> None:
        contract = _contract()
        with pytest.raises(FrozenInstanceError):
            contract.declaration_confirmation = False  # type: ignore[misc]

    def test_result_and_twin_are_frozen(self) -> None:
        result = StudentCalibrationBuilder().build(_contract())
        with pytest.raises(FrozenInstanceError):
            result.metadata = result.metadata  # type: ignore[misc]
        with pytest.raises(FrozenInstanceError):
            result.twin.identity = result.twin.identity  # type: ignore[misc]

    def test_prior_payload_defensive_copy(self) -> None:
        result = StudentCalibrationBuilder().build(_contract())
        prior = result.metadata.knowledge_priors[-1]
        prior.payload["section_ids"].append("HACKED")
        # Original marker payload must not share mutable list identity with
        # a second build from the same contract shape.
        again = StudentCalibrationBuilder().build(_contract())
        again_prior = next(
            p
            for p in again.metadata.knowledge_priors
            if p.kind == "declared_complete_prior"
        )
        assert again_prior.payload["section_ids"] == ["CS1-1", "CS1-2"]

    def test_same_contract_yields_equal_result(self) -> None:
        builder = StudentCalibrationBuilder()
        contract = _contract()
        assert builder.build(contract) == builder.build(contract)


# ═══════════════════════════════════════════════════════════════════════════════
# Structural validation
# ═══════════════════════════════════════════════════════════════════════════════


class TestStructuralValidation:
    def test_rejects_unconfirmed_contract(self) -> None:
        with pytest.raises(
            CalibrationValidationError, match="declaration_confirmation"
        ):
            StudentCalibrationBuilder().build(
                _contract(declaration_confirmation=False)
            )

    def test_rejects_unknown_contract_version(self) -> None:
        with pytest.raises(CalibrationValidationError, match="contract_version"):
            StudentCalibrationBuilder().build(_contract(contract_version="9.9"))

    def test_rejects_first_time_with_history_present(self) -> None:
        with pytest.raises(CalibrationValidationError, match="conflicts"):
            StudentCalibrationBuilder().build(
                _beginner_contract(
                    beginner_or_history_posture=BeginnerOrHistoryPosture.HISTORY_PRESENT
                )
            )

    def test_rejects_empty_history_with_completed_sections(self) -> None:
        with pytest.raises(CalibrationValidationError, match="completed sections"):
            StudentCalibrationBuilder().build(
                _beginner_contract(declared_completed_sections=("CS1-1",))
            )

    def test_rejects_non_contract_input(self) -> None:
        with pytest.raises(
            CalibrationValidationError, match="StudentCalibrationContract"
        ):
            StudentCalibrationBuilder().build({"student": "x"})  # type: ignore[arg-type]


# ═══════════════════════════════════════════════════════════════════════════════
# Framework independence / no educational reasoning
# ═══════════════════════════════════════════════════════════════════════════════


class TestFrameworkIndependence:
    def test_calibration_package_has_no_flask_orm_or_service_imports(self) -> None:
        violations: list[str] = []
        for path in sorted(CALIBRATION_ROOT.rglob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        root = alias.name.split(".", 1)[0]
                        if root in FORBIDDEN_ROOT_MODULES or alias.name.startswith(
                            FORBIDDEN_PREFIXES
                        ):
                            violations.append(f"{path.name}: import {alias.name}")
                elif isinstance(node, ast.ImportFrom) and node.module:
                    root = node.module.split(".", 1)[0]
                    if root in FORBIDDEN_ROOT_MODULES or node.module.startswith(
                        FORBIDDEN_PREFIXES
                    ):
                        violations.append(f"{path.name}: from {node.module}")
                    for prefix in FORBIDDEN_EDUCATIONAL_IMPORTS:
                        if node.module == prefix or node.module.startswith(
                            prefix + "."
                        ):
                            violations.append(
                                f"{path.name}: educational import {node.module}"
                            )
        assert violations == []

    def test_builder_source_has_no_flask_request_or_orm(self) -> None:
        src = (
            CALIBRATION_ROOT / "student_calibration_builder.py"
        ).read_text(encoding="utf-8")
        assert "flask.request" not in src
        assert "flask.session" not in src
        assert "Blueprint" not in src
        assert "bp.route" not in src
        assert "render_template" not in src
        assert "sqlalchemy" not in src.lower()
        assert "db.session" not in src
        assert "CurriculumService" not in src


class TestNoEducationalReasoning:
    def test_builder_does_not_contain_scoring_or_selection_tokens(self) -> None:
        src = (
            CALIBRATION_ROOT / "student_calibration_builder.py"
        ).read_text(encoding="utf-8")
        hits = [token for token in FORBIDDEN_LOGIC_TOKENS if token in src]
        assert hits == []

    def test_builder_does_not_call_educational_engines_or_pipeline(self) -> None:
        src = (
            CALIBRATION_ROOT / "student_calibration_builder.py"
        ).read_text(encoding="utf-8")
        assert "ReadinessAggregation" not in src
        assert "DecisionEngine" not in src
        assert "RecommendationEngine" not in src
        assert "MissionIntelligence" not in src
        assert "EvidenceRecorder" not in src
        assert "TwinUpdatePipeline" not in src
        assert "TwinProvider" not in src

    def test_builder_has_no_persist_or_rank_api(self) -> None:
        builder = StudentCalibrationBuilder()
        assert not hasattr(builder, "save")
        assert not hasattr(builder, "update")
        assert not hasattr(builder, "persist")
        assert not hasattr(builder, "rank")
        assert not hasattr(builder, "recommend")
        assert not hasattr(builder, "infer_mastery")
        assert not hasattr(builder, "infer_readiness")

    def test_closed_output_is_calibration_result_only(self) -> None:
        result = StudentCalibrationBuilder().build(_contract())
        assert type(result) is CalibrationResult
        assert type(result.twin) is DigitalTwin

    def test_returning_posture_does_not_emit_readiness_or_mastery(self) -> None:
        result = StudentCalibrationBuilder().build(_contract())
        twin = result.twin
        assert twin.knowledge.topic_mastery == ()
        assert twin.predictions.readiness_snapshot is None
        assert twin.goals.target_pass_probability is None
        assert not hasattr(result, "readiness")
        assert not hasattr(result, "decision")
        assert not hasattr(result, "recommendation")
        assert not hasattr(result, "mission")
