"""Tests for Calibration Birth → InMemoryTwinRepository integration (Capability 3.7.5).

Proves Contract → Builder → Birth Twin → Persist path: snapshot equality,
immutability, history / current resolution, component independence, and
framework independence. No educational reasoning.
"""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError
from datetime import UTC, date, datetime
from pathlib import Path

import pytest

from app.application.calibration import (
    CONTRACT_VERSION_1_0,
    BeginnerOrHistoryPosture,
    CalibrationBirthPersister,
    CalibrationValidationError,
    CoreReadingDeclaration,
    CurriculumExamScope,
    IntendedSitting,
    PersistedCalibrationBirth,
    PreviousAttemptsDeclaration,
    PreviouslyStudied,
    StudentCalibrationBuilder,
    StudentCalibrationContract,
    StudyObjective,
)
from app.application.twin_repository import (
    CurrentSnapshotRef,
    InMemoryTwinRepository,
    PersistAcknowledgement,
    SnapshotHistory,
    TwinAuthorship,
    TwinPersistenceFailure,
    TwinPersistenceFailureReason,
    TwinScope,
)
from app.domain.twin import DigitalTwin

APP_ROOT = Path(__file__).resolve().parents[2] / "app" / "application"
CALIBRATION_ROOT = APP_ROOT / "calibration"
TWIN_REPO_ROOT = APP_ROOT / "twin_repository"
BUILDER_SOURCE = CALIBRATION_ROOT / "student_calibration_builder.py"
REPO_SOURCE = TWIN_REPO_ROOT / "twin_repository.py"
PERSISTER_SOURCE = CALIBRATION_ROOT / "birth_persistence.py"

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
    "app.application.orchestration",
    "app.application.twin",
    "app.application.dashboard",
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
    "EducationalOrchestrator",
    "mastery_belief=",
    "readiness_snapshot=",
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


def _persister(
    *,
    builder: StudentCalibrationBuilder | None = None,
    repository: InMemoryTwinRepository | None = None,
) -> CalibrationBirthPersister:
    return CalibrationBirthPersister(
        builder=builder,
        repository=repository if repository is not None else InMemoryTwinRepository(),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# Birth Twin persisted
# ═══════════════════════════════════════════════════════════════════════════════


class TestBirthTwinPersisted:
    def test_persist_birth_stores_builder_twin_as_current(self) -> None:
        repo = InMemoryTwinRepository()
        result = _persister(repository=repo).persist_birth(
            _contract(),
            snapshot_id="birth-cal-1",
            persisted_at=datetime(2026, 7, 12, 15, 0, tzinfo=UTC),
        )

        assert isinstance(result, PersistedCalibrationBirth)
        assert isinstance(result.acknowledgement, PersistAcknowledgement)
        assert result.snapshot_id == "birth-cal-1"
        assert result.acknowledgement.sequence == 1
        assert result.acknowledgement.authorship is TwinAuthorship.BIRTH
        assert result.scope.student_id == "student-42"
        assert result.scope.curriculum_id == "7"
        assert result.scope.sitting_id == "Sep 2026"

        current = repo.retrieve_current_twin(result.scope)
        assert isinstance(current, DigitalTwin)
        assert current is result.twin

    def test_persist_birth_propagates_repository_honesty(self) -> None:
        repo = InMemoryTwinRepository()
        repo.mark_unavailable()
        result = _persister(repository=repo).persist_birth(_contract())

        assert isinstance(result, TwinPersistenceFailure)
        assert result.reason is TwinPersistenceFailureReason.UNAVAILABLE


# ═══════════════════════════════════════════════════════════════════════════════
# Persisted snapshot equals Builder output
# ═══════════════════════════════════════════════════════════════════════════════


class TestPersistedEqualsBuilderOutput:
    def test_persisted_snapshot_equals_builder_output(self) -> None:
        builder = StudentCalibrationBuilder()
        repo = InMemoryTwinRepository()
        contract = _contract()

        built = builder.build(contract)
        persisted = _persister(builder=builder, repository=repo).persist_birth(
            contract,
            snapshot_id="eq-1",
        )

        assert isinstance(persisted, PersistedCalibrationBirth)
        assert persisted.twin == built.twin
        assert persisted.metadata == built.metadata
        assert persisted.calibration == built
        assert persisted.twin is persisted.calibration.twin

        loaded = repo.retrieve_current_twin(persisted.scope)
        assert isinstance(loaded, DigitalTwin)
        assert loaded == built.twin
        assert loaded is persisted.twin


# ═══════════════════════════════════════════════════════════════════════════════
# Immutability preserved
# ═══════════════════════════════════════════════════════════════════════════════


class TestImmutabilityPreserved:
    def test_persisted_result_and_cargo_are_frozen(self) -> None:
        result = _persister().persist_birth(_contract(), snapshot_id="imm-1")
        assert isinstance(result, PersistedCalibrationBirth)

        with pytest.raises(FrozenInstanceError):
            result.twin = result.twin  # type: ignore[misc]
        with pytest.raises(FrozenInstanceError):
            result.acknowledgement.snapshot_id = "other"  # type: ignore[misc]
        with pytest.raises(FrozenInstanceError):
            result.metadata.source = "evidence"  # type: ignore[misc]
        with pytest.raises(FrozenInstanceError):
            result.twin.identity.student_id = "mutated"  # type: ignore[misc]


# ═══════════════════════════════════════════════════════════════════════════════
# History contains one snapshot / current resolves
# ═══════════════════════════════════════════════════════════════════════════════


class TestHistoryAndCurrent:
    def test_history_contains_exactly_one_birth_snapshot(self) -> None:
        repo = InMemoryTwinRepository()
        result = _persister(repository=repo).persist_birth(
            _contract(),
            snapshot_id="hist-1",
        )
        assert isinstance(result, PersistedCalibrationBirth)

        history = repo.retrieve_snapshot_history(result.scope)
        assert isinstance(history, SnapshotHistory)
        assert len(history.snapshots) == 1
        assert history.current_snapshot_id == "hist-1"
        assert history.snapshots[0].authorship is TwinAuthorship.BIRTH
        assert history.snapshots[0].twin is result.twin

    def test_current_snapshot_resolves_correctly(self) -> None:
        repo = InMemoryTwinRepository()
        result = _persister(repository=repo).persist_birth(
            _contract(),
            snapshot_id="cur-1",
        )
        assert isinstance(result, PersistedCalibrationBirth)

        current = repo.determine_current_snapshot(result.scope)
        assert isinstance(current, CurrentSnapshotRef)
        assert current.snapshot_id == "cur-1"
        assert current.sequence == 1
        assert current.twin is result.twin
        assert current.scope == result.scope


# ═══════════════════════════════════════════════════════════════════════════════
# Builder and Repository remain independent
# ═══════════════════════════════════════════════════════════════════════════════


class TestComponentIndependence:
    def test_builder_remains_independent_of_repository(self) -> None:
        src = BUILDER_SOURCE.read_text(encoding="utf-8")
        assert "twin_repository" not in src
        assert "InMemoryTwinRepository" not in src
        assert "persist_birth" not in src
        assert "CalibrationBirthPersister" not in src

        # Builder still works without any repository.
        alone = StudentCalibrationBuilder().build(_contract())
        assert isinstance(alone.twin, DigitalTwin)
        assert alone.metadata.source == "self_declared"

    def test_repository_remains_independent_of_calibration(self) -> None:
        from app.domain.twin import GoalState, IdentityState

        src = REPO_SOURCE.read_text(encoding="utf-8")
        assert "calibration" not in src
        assert "StudentCalibrationBuilder" not in src
        assert "StudentCalibrationContract" not in src
        assert "CalibrationBirthPersister" not in src

        # Repository still works without Calibration authorship.
        repo = InMemoryTwinRepository()
        twin = DigitalTwin.create(
            IdentityState.create("student-99", curriculum_id="7"),
            goals=GoalState.create(target_completion_date=date(2026, 9, 1)),
        )
        ack = repo.persist_birth_twin(
            twin,
            scope=TwinScope.create("student-99", curriculum_id="7"),
            snapshot_id="solo-1",
        )
        assert isinstance(ack, PersistAcknowledgement)

    def test_persister_composes_without_merging_components(self) -> None:
        builder = StudentCalibrationBuilder()
        repo = InMemoryTwinRepository()
        persister = _persister(builder=builder, repository=repo)

        assert persister.builder is builder
        assert persister.repository is repo
        assert not hasattr(builder, "persist_birth")
        assert not hasattr(repo, "build")
        assert not hasattr(repo, "calibrate")


# ═══════════════════════════════════════════════════════════════════════════════
# Structural validation still fail-closed before persist
# ═══════════════════════════════════════════════════════════════════════════════


class TestFailClosedBeforePersist:
    def test_unlawful_contract_never_reaches_repository(self) -> None:
        repo = InMemoryTwinRepository()
        with pytest.raises(
            CalibrationValidationError, match="declaration_confirmation"
        ):
            _persister(repository=repo).persist_birth(
                _contract(declaration_confirmation=False)
            )

        history = repo.retrieve_snapshot_history(
            TwinScope.create("student-42", sitting_id="Sep 2026", curriculum_id="7")
        )
        assert isinstance(history, SnapshotHistory)
        assert history.is_empty


# ═══════════════════════════════════════════════════════════════════════════════
# Framework independence / no educational reasoning
# ═══════════════════════════════════════════════════════════════════════════════


class TestFrameworkIndependence:
    def test_persister_has_no_flask_orm_or_service_imports(self) -> None:
        violations: list[str] = []
        tree = ast.parse(
            PERSISTER_SOURCE.read_text(encoding="utf-8"),
            filename=str(PERSISTER_SOURCE),
        )
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root = alias.name.split(".", 1)[0]
                    if root in FORBIDDEN_ROOT_MODULES or alias.name.startswith(
                        FORBIDDEN_PREFIXES
                    ):
                        violations.append(f"import {alias.name}")
            elif isinstance(node, ast.ImportFrom) and node.module:
                root = node.module.split(".", 1)[0]
                if root in FORBIDDEN_ROOT_MODULES or node.module.startswith(
                    FORBIDDEN_PREFIXES
                ):
                    violations.append(f"from {node.module}")
                for prefix in FORBIDDEN_EDUCATIONAL_IMPORTS:
                    if node.module == prefix or node.module.startswith(prefix + "."):
                        violations.append(f"educational import {node.module}")
        assert violations == []

    def test_persister_source_has_no_flask_request_orm_or_sql(self) -> None:
        src = PERSISTER_SOURCE.read_text(encoding="utf-8")
        assert "flask.request" not in src
        assert "flask.session" not in src
        assert "Blueprint" not in src
        assert "bp.route" not in src
        assert "render_template" not in src
        assert "sqlalchemy" not in src.lower()
        assert "db.session" not in src
        assert "SELECT " not in src
        assert "INSERT " not in src
        assert "CurriculumService" not in src


class TestNoEducationalReasoning:
    def test_persister_does_not_contain_scoring_or_selection_tokens(self) -> None:
        src = PERSISTER_SOURCE.read_text(encoding="utf-8")
        hits = [token for token in FORBIDDEN_LOGIC_TOKENS if token in src]
        assert hits == []

    def test_persister_does_not_call_educational_engines_or_provider(self) -> None:
        src = PERSISTER_SOURCE.read_text(encoding="utf-8")
        assert "ReadinessAggregation" not in src
        assert "DecisionEngine" not in src
        assert "RecommendationEngine" not in src
        assert "MissionIntelligence" not in src
        assert "EducationalOrchestrator" not in src
        assert "TwinUpdatePipeline" not in src
        assert "EvidenceRecorder" not in src
        assert "from app.domain.readiness" not in src
        assert "from app.domain.decision" not in src
        assert "from app.application.orchestration" not in src
        assert "from app.application.twin." not in src
        assert "from app.application.twin import" not in src
        assert "import TwinProvider" not in src
        assert "application.twin.twin_provider" not in src
