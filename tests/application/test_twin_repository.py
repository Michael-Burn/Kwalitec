"""Tests for InMemoryTwinRepository (Capability 3.7.4).

Proves Birth / Successor persistence, current resolution, history retrieval,
snapshot immutability, and framework independence. Repository never creates
Twins or performs educational reasoning.
"""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError
from datetime import UTC, date, datetime
from pathlib import Path

import pytest

from app.application.twin_repository import (
    SNAPSHOT_FORMAT_VERSION_1_0,
    CurrentSnapshotRef,
    InMemoryTwinRepository,
    PersistAcknowledgement,
    SnapshotHistory,
    TwinAuthorship,
    TwinPersistenceFailure,
    TwinPersistenceFailureReason,
    TwinScope,
    TwinSnapshotRecord,
)
from app.domain.twin import DigitalTwin, GoalState, IdentityState, KnowledgeState

REPO_ROOT = (
    Path(__file__).resolve().parents[2] / "app" / "application" / "twin_repository"
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
    "app.application.orchestration",
    "app.application.calibration",
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
    "DigitalTwin.create",
    "mastery_belief=",
    "readiness_snapshot=",
)

# Contract / codec / in-memory stay framework-free. twin_repository.py is the
# authorised SQLAlchemy adapter (Capability 3.8.2).
FRAMEWORK_FREE_MODULES = frozenset(
    {
        "__init__.py",
        "types.py",
        "codec.py",
        "in_memory.py",
        "shared.py",
    }
)


def _identity(**overrides: object) -> IdentityState:
    defaults: dict[str, object] = {
        "student_id": "student-42",
        "curriculum_id": "7",
        "current_exam": "CS1",
        "target_sitting": date(2026, 9, 1),
    }
    defaults.update(overrides)
    return IdentityState.create(**defaults)  # type: ignore[arg-type]


def _twin(**overrides: object) -> DigitalTwin:
    identity = overrides.pop("identity", None)
    if identity is None:
        identity = _identity()
    goals = overrides.pop(
        "goals",
        GoalState.create(target_completion_date=date(2026, 9, 1)),
    )
    knowledge = overrides.pop("knowledge", KnowledgeState.create())
    return DigitalTwin.create(
        identity,  # type: ignore[arg-type]
        goals=goals,  # type: ignore[arg-type]
        knowledge=knowledge,  # type: ignore[arg-type]
        **overrides,  # type: ignore[arg-type]
    )


def _scope(**overrides: object) -> TwinScope:
    defaults: dict[str, object] = {
        "student_id": "student-42",
        "sitting_id": "sep-2026",
        "curriculum_id": "7",
    }
    defaults.update(overrides)
    return TwinScope.create(**defaults)  # type: ignore[arg-type]


# ═══════════════════════════════════════════════════════════════════════════════
# Birth persistence
# ═══════════════════════════════════════════════════════════════════════════════


class TestBirthPersistence:
    def test_persist_birth_twin_makes_snapshot_current(self) -> None:
        repo = InMemoryTwinRepository()
        twin = _twin()
        scope = _scope()

        result = repo.persist_birth_twin(
            twin,
            scope=scope,
            snapshot_id="birth-1",
            provenance={"source": "self_declared"},
            persisted_at=datetime(2026, 7, 12, 12, 0, tzinfo=UTC),
        )

        assert isinstance(result, PersistAcknowledgement)
        assert result.snapshot_id == "birth-1"
        assert result.sequence == 1
        assert result.authorship is TwinAuthorship.BIRTH
        assert result.scope == scope

        loaded = repo.retrieve_current_twin(scope)
        assert loaded is twin

    def test_persist_birth_rejects_when_scope_already_has_twin(self) -> None:
        repo = InMemoryTwinRepository()
        scope = _scope()
        first = repo.persist_birth_twin(_twin(), scope=scope, snapshot_id="birth-1")
        assert isinstance(first, PersistAcknowledgement)

        second = repo.persist_birth_twin(
            _twin(), scope=scope, snapshot_id="birth-2"
        )
        assert isinstance(second, TwinPersistenceFailure)
        assert second.reason is TwinPersistenceFailureReason.DUPLICATE
        assert second.snapshot_id == "birth-1"

        # Original birth unchanged
        assert repo.retrieve_current_twin(scope) is not None
        history = repo.retrieve_snapshot_history(scope)
        assert isinstance(history, SnapshotHistory)
        assert len(history.snapshots) == 1
        assert history.snapshots[0].identity.snapshot_id == "birth-1"

    def test_persist_birth_rejects_non_twin_cargo(self) -> None:
        repo = InMemoryTwinRepository()
        result = repo.persist_birth_twin({"not": "a twin"}, scope=_scope())  # type: ignore[arg-type]
        assert isinstance(result, TwinPersistenceFailure)
        assert result.reason is TwinPersistenceFailureReason.REJECTED

    def test_persist_birth_never_invents_twin_from_absence(self) -> None:
        repo = InMemoryTwinRepository()
        assert not hasattr(repo, "create_twin")
        assert not hasattr(repo, "invent")
        assert not hasattr(repo, "fabricate")
        missing = repo.retrieve_current_twin(_scope())
        assert isinstance(missing, TwinPersistenceFailure)
        assert missing.reason is TwinPersistenceFailureReason.MISSING


# ═══════════════════════════════════════════════════════════════════════════════
# Successor persistence
# ═══════════════════════════════════════════════════════════════════════════════


class TestSuccessorPersistence:
    def test_persist_successor_becomes_current_and_retains_birth(self) -> None:
        repo = InMemoryTwinRepository()
        scope = _scope()
        birth = _twin()
        successor = _twin(
            goals=GoalState.create(
                target_completion_date=date(2026, 9, 1),
                planned_study_hours_per_week=10.0,
            )
        )

        birth_ack = repo.persist_birth_twin(
            birth, scope=scope, snapshot_id="birth-1"
        )
        assert isinstance(birth_ack, PersistAcknowledgement)

        succ_ack = repo.persist_successor_twin(
            successor,
            scope=scope,
            snapshot_id="succ-1",
            expected_current_snapshot_id="birth-1",
            provenance={"evidence_ids": ("ev-1",)},
        )
        assert isinstance(succ_ack, PersistAcknowledgement)
        assert succ_ack.snapshot_id == "succ-1"
        assert succ_ack.sequence == 2
        assert succ_ack.authorship is TwinAuthorship.SUCCESSOR

        assert repo.retrieve_current_twin(scope) is successor

        history = repo.retrieve_snapshot_history(scope)
        assert isinstance(history, SnapshotHistory)
        assert len(history.snapshots) == 2
        assert history.snapshots[0].twin is birth
        assert history.snapshots[1].twin is successor
        assert history.current_snapshot_id == "succ-1"

    def test_persist_successor_without_birth_signals_missing(self) -> None:
        repo = InMemoryTwinRepository()
        result = repo.persist_successor_twin(_twin(), scope=_scope())
        assert isinstance(result, TwinPersistenceFailure)
        assert result.reason is TwinPersistenceFailureReason.MISSING

    def test_concurrent_successor_rejected_without_hybrid_merge(self) -> None:
        repo = InMemoryTwinRepository()
        scope = _scope()
        repo.persist_birth_twin(_twin(), scope=scope, snapshot_id="birth-1")
        repo.persist_successor_twin(
            _twin(),
            scope=scope,
            snapshot_id="succ-1",
            expected_current_snapshot_id="birth-1",
        )

        stale = repo.persist_successor_twin(
            _twin(),
            scope=scope,
            snapshot_id="succ-stale",
            expected_current_snapshot_id="birth-1",
        )
        assert isinstance(stale, TwinPersistenceFailure)
        assert stale.reason is TwinPersistenceFailureReason.CONCURRENT

        history = repo.retrieve_snapshot_history(scope)
        assert isinstance(history, SnapshotHistory)
        assert len(history.snapshots) == 2
        assert history.current_snapshot_id == "succ-1"


# ═══════════════════════════════════════════════════════════════════════════════
# Current snapshot resolution
# ═══════════════════════════════════════════════════════════════════════════════


class TestCurrentSnapshotResolution:
    def test_determine_current_snapshot_after_birth(self) -> None:
        repo = InMemoryTwinRepository()
        scope = _scope()
        twin = _twin()
        repo.persist_birth_twin(twin, scope=scope, snapshot_id="birth-1")

        current = repo.determine_current_snapshot(scope)
        assert isinstance(current, CurrentSnapshotRef)
        assert current.snapshot_id == "birth-1"
        assert current.sequence == 1
        assert current.twin is twin

    def test_determine_current_advances_with_successor(self) -> None:
        repo = InMemoryTwinRepository()
        scope = _scope()
        repo.persist_birth_twin(_twin(), scope=scope, snapshot_id="birth-1")
        successor = _twin()
        repo.persist_successor_twin(
            successor, scope=scope, snapshot_id="succ-1"
        )

        current = repo.determine_current_snapshot(scope)
        assert isinstance(current, CurrentSnapshotRef)
        assert current.snapshot_id == "succ-1"
        assert current.sequence == 2
        assert current.twin is successor

    def test_determine_current_missing_when_empty(self) -> None:
        repo = InMemoryTwinRepository()
        result = repo.determine_current_snapshot(_scope())
        assert isinstance(result, TwinPersistenceFailure)
        assert result.reason is TwinPersistenceFailureReason.MISSING

    def test_retrieve_current_matches_determine_current(self) -> None:
        repo = InMemoryTwinRepository()
        scope = _scope()
        twin = _twin()
        repo.persist_birth_twin(twin, scope=scope, snapshot_id="birth-1")

        retrieved = repo.retrieve_current_twin(scope)
        determined = repo.determine_current_snapshot(scope)
        assert retrieved is twin
        assert isinstance(determined, CurrentSnapshotRef)
        assert determined.twin is retrieved


# ═══════════════════════════════════════════════════════════════════════════════
# History retrieval
# ═══════════════════════════════════════════════════════════════════════════════


class TestHistoryRetrieval:
    def test_history_ordered_birth_to_successors(self) -> None:
        repo = InMemoryTwinRepository()
        scope = _scope()
        t0 = _twin()
        t1 = _twin(
            goals=GoalState.create(planned_study_hours_per_week=8.0),
        )
        t2 = _twin(
            goals=GoalState.create(planned_study_hours_per_week=12.0),
        )

        repo.persist_birth_twin(t0, scope=scope, snapshot_id="s0")
        repo.persist_successor_twin(t1, scope=scope, snapshot_id="s1")
        repo.persist_successor_twin(t2, scope=scope, snapshot_id="s2")

        history = repo.retrieve_snapshot_history(scope)
        assert isinstance(history, SnapshotHistory)
        assert not history.is_empty
        assert [r.identity.snapshot_id for r in history.snapshots] == [
            "s0",
            "s1",
            "s2",
        ]
        assert [r.identity.sequence for r in history.snapshots] == [1, 2, 3]
        assert [r.authorship for r in history.snapshots] == [
            TwinAuthorship.BIRTH,
            TwinAuthorship.SUCCESSOR,
            TwinAuthorship.SUCCESSOR,
        ]
        assert history.current_snapshot_id == "s2"
        assert all(
            r.identity.format_version == SNAPSHOT_FORMAT_VERSION_1_0
            for r in history.snapshots
        )

    def test_empty_scope_history_is_honest_emptiness(self) -> None:
        repo = InMemoryTwinRepository()
        history = repo.retrieve_snapshot_history(_scope())
        assert isinstance(history, SnapshotHistory)
        assert history.is_empty
        assert history.snapshots == ()
        assert history.current_snapshot_id is None

    def test_provenance_survives_persist_and_history(self) -> None:
        repo = InMemoryTwinRepository()
        scope = _scope()
        provenance = {"source": "self_declared", "warrant": "thin"}
        repo.persist_birth_twin(
            _twin(),
            scope=scope,
            snapshot_id="birth-1",
            provenance=provenance,
        )

        history = repo.retrieve_snapshot_history(scope)
        assert isinstance(history, SnapshotHistory)
        record = history.snapshots[0]
        assert isinstance(record, TwinSnapshotRecord)
        assert record.provenance == provenance
        # Caller mutation of input dict must not alter stored provenance
        provenance["source"] = "tampered"
        assert record.provenance == {
            "source": "self_declared",
            "warrant": "thin",
        }


# ═══════════════════════════════════════════════════════════════════════════════
# Snapshot immutability
# ═══════════════════════════════════════════════════════════════════════════════


class TestSnapshotImmutability:
    def test_stored_records_are_frozen(self) -> None:
        repo = InMemoryTwinRepository()
        scope = _scope()
        repo.persist_birth_twin(_twin(), scope=scope, snapshot_id="birth-1")
        history = repo.retrieve_snapshot_history(scope)
        assert isinstance(history, SnapshotHistory)
        record = history.snapshots[0]

        with pytest.raises(FrozenInstanceError):
            record.twin = _twin()  # type: ignore[misc]
        with pytest.raises(FrozenInstanceError):
            record.identity.snapshot_id = "hacked"  # type: ignore[misc]
        with pytest.raises(FrozenInstanceError):
            record.authorship = TwinAuthorship.SUCCESSOR  # type: ignore[misc]

    def test_successor_does_not_mutate_prior_snapshot_content(self) -> None:
        repo = InMemoryTwinRepository()
        scope = _scope()
        birth = _twin()
        birth_goals = birth.goals

        repo.persist_birth_twin(birth, scope=scope, snapshot_id="birth-1")
        repo.persist_successor_twin(
            _twin(
                goals=GoalState.create(planned_study_hours_per_week=20.0),
            ),
            scope=scope,
            snapshot_id="succ-1",
        )

        history = repo.retrieve_snapshot_history(scope)
        assert isinstance(history, SnapshotHistory)
        prior = history.snapshots[0]
        assert prior.twin is birth
        assert prior.twin.goals is birth_goals
        assert prior.twin.goals.planned_study_hours_per_week is None
        assert prior.identity.snapshot_id == "birth-1"
        assert prior.authorship is TwinAuthorship.BIRTH

    def test_no_patch_or_update_api(self) -> None:
        repo = InMemoryTwinRepository()
        assert not hasattr(repo, "patch")
        assert not hasattr(repo, "update")
        assert not hasattr(repo, "upsert")
        assert not hasattr(repo, "merge")
        assert not hasattr(repo, "mutate")
        assert not hasattr(repo, "edit_field")

    def test_acknowledgement_and_failure_are_frozen(self) -> None:
        repo = InMemoryTwinRepository()
        ack = repo.persist_birth_twin(_twin(), scope=_scope(), snapshot_id="b1")
        assert isinstance(ack, PersistAcknowledgement)
        with pytest.raises(FrozenInstanceError):
            ack.snapshot_id = "other"  # type: ignore[misc]

        fail = repo.retrieve_current_twin(_scope(student_id="nobody"))
        assert isinstance(fail, TwinPersistenceFailure)
        with pytest.raises(FrozenInstanceError):
            fail.reason = TwinPersistenceFailureReason.CORRUPT  # type: ignore[misc]


# ═══════════════════════════════════════════════════════════════════════════════
# Honesty / unavailable
# ═══════════════════════════════════════════════════════════════════════════════


class TestHonestySignals:
    def test_storage_unavailable_on_persist_and_retrieve(self) -> None:
        repo = InMemoryTwinRepository()
        repo.mark_unavailable()
        scope = _scope()

        persist = repo.persist_birth_twin(_twin(), scope=scope)
        assert isinstance(persist, TwinPersistenceFailure)
        assert persist.reason is TwinPersistenceFailureReason.UNAVAILABLE

        retrieve = repo.retrieve_current_twin(scope)
        assert isinstance(retrieve, TwinPersistenceFailure)
        assert retrieve.reason is TwinPersistenceFailureReason.UNAVAILABLE

    def test_duplicate_snapshot_identity_rejected(self) -> None:
        repo = InMemoryTwinRepository()
        scope_a = _scope(student_id="a", sitting_id="s1")
        scope_b = _scope(student_id="b", sitting_id="s1")
        repo.persist_birth_twin(
            _twin(identity=_identity(student_id="a")),
            scope=scope_a,
            snapshot_id="shared-id",
        )
        dup = repo.persist_birth_twin(
            _twin(identity=_identity(student_id="b")),
            scope=scope_b,
            snapshot_id="shared-id",
        )
        assert isinstance(dup, TwinPersistenceFailure)
        assert dup.reason is TwinPersistenceFailureReason.DUPLICATE


# ═══════════════════════════════════════════════════════════════════════════════
# Framework independence / no educational reasoning
# ═══════════════════════════════════════════════════════════════════════════════


class TestFrameworkIndependence:
    def test_framework_free_modules_have_no_flask_orm_or_service_imports(self) -> None:
        violations: list[str] = []
        for name in sorted(FRAMEWORK_FREE_MODULES):
            path = REPO_ROOT / name
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

    def test_durable_adapter_has_no_flask_request_or_routes(self) -> None:
        """SQLAlchemy adapter may use ORM; must not use request/session/routes."""
        src = (REPO_ROOT / "twin_repository.py").read_text(encoding="utf-8")
        assert "flask.request" not in src
        assert "flask.session" not in src
        assert "Blueprint" not in src
        assert "bp.route" not in src
        assert "render_template" not in src
        assert "CurriculumService" not in src
        assert "from flask" not in src


class TestNoEducationalReasoning:
    def test_repository_does_not_contain_scoring_or_selection_tokens(self) -> None:
        src = (REPO_ROOT / "twin_repository.py").read_text(encoding="utf-8")
        hits = [token for token in FORBIDDEN_LOGIC_TOKENS if token in src]
        assert hits == []

    def test_repository_does_not_call_educational_engines_or_orchestrator(self) -> None:
        src = (REPO_ROOT / "twin_repository.py").read_text(encoding="utf-8")
        assert "ReadinessAggregation" not in src
        assert "DecisionEngine" not in src
        assert "RecommendationEngine" not in src
        assert "MissionIntelligence" not in src
        assert "EducationalOrchestrator" not in src
        assert "TwinProvider" not in src
        assert "TwinUpdatePipeline" not in src
        assert "StudentCalibrationBuilder" not in src
        assert "from app.application.orchestration" not in src
        assert "from app.domain.readiness" not in src
        assert "from app.domain.decision" not in src

    def test_repository_never_creates_twins(self) -> None:
        src = (REPO_ROOT / "twin_repository.py").read_text(encoding="utf-8")
        assert "DigitalTwin.create" not in src
        assert "IdentityState.create" not in src
        repo = InMemoryTwinRepository()
        assert not hasattr(repo, "create")
        assert not hasattr(repo, "build")
        assert not hasattr(repo, "calibrate")
