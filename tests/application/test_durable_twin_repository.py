"""Tests for durable SQLAlchemy TwinRepository (Capability 3.8.2).

Proves restart-safe persistence, Birth / Successor retrieval, snapshot history,
current designation, immutability (no prior-row mutation), and migration.
Contract callers are unchanged — only storage is durable.
"""

from __future__ import annotations

import os
import tempfile
from datetime import UTC, date, datetime
from pathlib import Path

from alembic import command
from alembic.config import Config as AlembicConfig
from sqlalchemy import inspect, text

from app.application.twin_repository import (
    PersistAcknowledgement,
    SnapshotHistory,
    TwinAuthorship,
    TwinPersistenceFailure,
    TwinPersistenceFailureReason,
    TwinRepository,
    TwinScope,
)
from app.application.twin_repository.codec import decode_twin, encode_twin
from app.domain.twin import (
    DigitalTwin,
    GoalState,
    IdentityState,
    KnowledgeState,
    TopicMasteryRecord,
)
from app.extensions import db
from app.models.twin_snapshot import TwinSnapshot

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MIGRATIONS_DIR = PROJECT_ROOT / "migrations"


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
# Birth / current / successor / history
# ═══════════════════════════════════════════════════════════════════════════════


class TestDurableBirthAndCurrent:
    def test_persist_birth_and_retrieve_current(self, ctx) -> None:
        repo = TwinRepository()
        twin = _twin()
        scope = _scope()

        result = repo.persist_birth_twin(
            twin,
            scope=scope,
            snapshot_id="birth-durable-1",
            provenance={"source": "self_declared"},
            persisted_at=datetime(2026, 7, 12, 12, 0, tzinfo=UTC),
        )
        assert isinstance(result, PersistAcknowledgement)
        assert result.snapshot_id == "birth-durable-1"
        assert result.sequence == 1
        assert result.authorship is TwinAuthorship.BIRTH

        loaded = repo.retrieve_current_twin(scope)
        assert isinstance(loaded, DigitalTwin)
        assert loaded == twin
        assert loaded.identity.student_id == "student-42"
        # Empty domains remain empty — no Mid fill.
        assert loaded.knowledge.topic_mastery == ()
        assert loaded.memory.retention == ()

    def test_birth_duplicate_for_scope_rejected(self, ctx) -> None:
        repo = TwinRepository()
        scope = _scope()
        repo.persist_birth_twin(_twin(), scope=scope, snapshot_id="b1")
        dup = repo.persist_birth_twin(_twin(), scope=scope, snapshot_id="b2")
        assert isinstance(dup, TwinPersistenceFailure)
        assert dup.reason is TwinPersistenceFailureReason.DUPLICATE


class TestDurableSuccessorAndHistory:
    def test_successor_becomes_current_prior_retained(self, ctx) -> None:
        repo = TwinRepository()
        scope = _scope()
        birth = _twin()
        successor = _twin(
            knowledge=KnowledgeState.create(
                topic_mastery=[
                    TopicMasteryRecord.create("T1", mastery_belief=None),
                ]
            )
        )

        repo.persist_birth_twin(birth, scope=scope, snapshot_id="birth-1")
        ack = repo.persist_successor_twin(
            successor,
            scope=scope,
            snapshot_id="succ-1",
            provenance={"source": "evidence_update"},
        )
        assert isinstance(ack, PersistAcknowledgement)
        assert ack.sequence == 2
        assert ack.authorship is TwinAuthorship.SUCCESSOR

        current = repo.retrieve_current_twin(scope)
        assert isinstance(current, DigitalTwin)
        assert current == successor
        assert len(current.knowledge.topic_mastery) == 1
        assert current.knowledge.topic_mastery[0].mastery_belief is None

        history = repo.retrieve_snapshot_history(scope)
        assert isinstance(history, SnapshotHistory)
        assert len(history.snapshots) == 2
        assert history.current_snapshot_id == "succ-1"
        assert history.snapshots[0].twin == birth
        assert history.snapshots[0].authorship is TwinAuthorship.BIRTH
        assert history.snapshots[1].twin == successor

    def test_determine_current_snapshot(self, ctx) -> None:
        repo = TwinRepository()
        scope = _scope()
        repo.persist_birth_twin(_twin(), scope=scope, snapshot_id="birth-1")
        repo.persist_successor_twin(_twin(), scope=scope, snapshot_id="succ-1")

        ref = repo.determine_current_snapshot(scope)
        assert not isinstance(ref, TwinPersistenceFailure)
        assert ref.snapshot_id == "succ-1"
        assert ref.sequence == 2

    def test_concurrent_successor_rejected(self, ctx) -> None:
        repo = TwinRepository()
        scope = _scope()
        repo.persist_birth_twin(_twin(), scope=scope, snapshot_id="birth-1")
        conflict = repo.persist_successor_twin(
            _twin(),
            scope=scope,
            snapshot_id="succ-stale",
            expected_current_snapshot_id="not-the-current",
        )
        assert isinstance(conflict, TwinPersistenceFailure)
        assert conflict.reason is TwinPersistenceFailureReason.CONCURRENT


# ═══════════════════════════════════════════════════════════════════════════════
# Immutability
# ═══════════════════════════════════════════════════════════════════════════════


class TestDurableImmutability:
    def test_successor_does_not_mutate_prior_row_payload(self, ctx) -> None:
        repo = TwinRepository()
        scope = _scope()
        birth = _twin(
            goals=GoalState.create(planned_study_hours_per_week=5.0),
        )
        repo.persist_birth_twin(birth, scope=scope, snapshot_id="birth-1")

        birth_row = TwinSnapshot.query.filter_by(snapshot_id="birth-1").one()
        original_payload = birth_row.twin_payload
        original_updated = birth_row.persisted_at

        repo.persist_successor_twin(
            _twin(goals=GoalState.create(planned_study_hours_per_week=20.0)),
            scope=scope,
            snapshot_id="succ-1",
        )

        birth_row_again = TwinSnapshot.query.filter_by(snapshot_id="birth-1").one()
        assert birth_row_again.twin_payload == original_payload
        assert birth_row_again.persisted_at == original_updated
        assert TwinSnapshot.query.count() == 2

        history = repo.retrieve_snapshot_history(scope)
        assert isinstance(history, SnapshotHistory)
        assert history.snapshots[0].twin.goals.planned_study_hours_per_week == 5.0
        assert history.snapshots[1].twin.goals.planned_study_hours_per_week == 20.0

    def test_no_patch_or_update_api(self, ctx) -> None:
        repo = TwinRepository()
        assert not hasattr(repo, "patch")
        assert not hasattr(repo, "update")
        assert not hasattr(repo, "upsert")
        assert not hasattr(repo, "merge")
        assert not hasattr(repo, "mutate")


# ═══════════════════════════════════════════════════════════════════════════════
# Restart-safe persistence
# ═══════════════════════════════════════════════════════════════════════════════


class TestRestartSafePersistence:
    def test_new_repository_instance_retrieves_persisted_twin(self, ctx) -> None:
        """A fresh TwinRepository handle reads what a prior handle wrote."""
        scope = _scope(student_id="restart-student")
        twin = _twin(identity=_identity(student_id="restart-student"))

        TwinRepository().persist_birth_twin(
            twin,
            scope=scope,
            snapshot_id="restart-birth",
            provenance={"source": "self_declared", "warrant": "declared"},
        )

        # Simulate process restart: new adapter instance, same durable store.
        reloaded = TwinRepository().retrieve_current_twin(scope)
        assert isinstance(reloaded, DigitalTwin)
        assert reloaded == twin

        history = TwinRepository().retrieve_snapshot_history(scope)
        assert isinstance(history, SnapshotHistory)
        assert history.snapshots[0].provenance == {
            "source": "self_declared",
            "warrant": "declared",
        }

    def test_codec_round_trip_preserves_empty_and_none_beliefs(self) -> None:
        twin = _twin(
            knowledge=KnowledgeState.create(
                topic_mastery=[
                    TopicMasteryRecord.create("T-empty", mastery_belief=None),
                ]
            )
        )
        restored = decode_twin(encode_twin(twin))
        assert restored == twin
        assert restored.knowledge.topic_mastery[0].mastery_belief is None


# ═══════════════════════════════════════════════════════════════════════════════
# Corruption / missing honesty
# ═══════════════════════════════════════════════════════════════════════════════


class TestDurableHonesty:
    def test_missing_twin(self, ctx) -> None:
        result = TwinRepository().retrieve_current_twin(
            _scope(student_id="nobody")
        )
        assert isinstance(result, TwinPersistenceFailure)
        assert result.reason is TwinPersistenceFailureReason.MISSING

    def test_corrupt_payload_signals_corrupt(self, ctx) -> None:
        scope = _scope(student_id="corrupt-student")
        TwinRepository().persist_birth_twin(
            _twin(identity=_identity(student_id="corrupt-student")),
            scope=scope,
            snapshot_id="corrupt-1",
        )
        row = TwinSnapshot.query.filter_by(snapshot_id="corrupt-1").one()
        row.twin_payload = "{not-json"
        db.session.commit()

        result = TwinRepository().retrieve_current_twin(scope)
        assert isinstance(result, TwinPersistenceFailure)
        assert result.reason is TwinPersistenceFailureReason.CORRUPT


# ═══════════════════════════════════════════════════════════════════════════════
# Migration
# ═══════════════════════════════════════════════════════════════════════════════


class TestTwinSnapshotMigration:
    def test_migration_creates_twin_snapshots_table(self) -> None:
        from app import config, create_app
        from app.extensions import db as _db

        db_fd, db_path = tempfile.mkstemp(suffix=".sqlite3")
        db_uri = f"sqlite:///{db_path}"

        os.environ["APP_ENV"] = "testing"
        os.environ["SECRET_KEY"] = "test-secret-key-for-testing-only"

        original_uri = config._database_uri
        original_cfg_uri = config.BaseConfig.SQLALCHEMY_DATABASE_URI
        config._database_uri = lambda: db_uri
        config.BaseConfig.SQLALCHEMY_DATABASE_URI = db_uri

        try:
            app = create_app()
            with app.app_context():
                cfg = AlembicConfig()
                cfg.set_main_option("script_location", str(MIGRATIONS_DIR))
                cfg.set_main_option("sqlalchemy.url", db_uri)
                command.upgrade(cfg, "head")

                inspector = inspect(_db.engine)
                assert "twin_snapshots" in inspector.get_table_names()

                columns = {
                    col["name"] for col in inspector.get_columns("twin_snapshots")
                }
                expected = {
                    "id",
                    "snapshot_id",
                    "student_id",
                    "sitting_id",
                    "curriculum_id",
                    "sequence",
                    "format_version",
                    "authorship",
                    "twin_payload",
                    "provenance_payload",
                    "persisted_at",
                    "created_at",
                }
                assert expected.issubset(columns)

                pk = inspector.get_pk_constraint("twin_snapshots")
                assert "id" in pk["constrained_columns"]

                # Durable write/read through migrated schema.
                repo = TwinRepository()
                scope = TwinScope.create("mig-student", curriculum_id="7")
                twin = DigitalTwin.create(
                    IdentityState.create("mig-student", curriculum_id="7")
                )
                ack = repo.persist_birth_twin(
                    twin, scope=scope, snapshot_id="mig-birth"
                )
                assert isinstance(ack, PersistAcknowledgement)
                loaded = repo.retrieve_current_twin(scope)
                assert loaded == twin

                count = _db.session.execute(
                    text("SELECT COUNT(*) FROM twin_snapshots")
                ).scalar()
                assert count == 1
        finally:
            os.close(db_fd)
            os.unlink(db_path)
            config._database_uri = original_uri
            config.BaseConfig.SQLALCHEMY_DATABASE_URI = original_cfg_uri
