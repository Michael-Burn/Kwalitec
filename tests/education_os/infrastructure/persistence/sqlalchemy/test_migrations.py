"""Migration upgrade, downgrade, and schema-metadata consistency tests (INF-009)."""

from __future__ import annotations

from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config as AlembicConfig
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, inspect

from infrastructure.persistence.sqlalchemy import metadata
from infrastructure.persistence.sqlalchemy.models import (  # noqa: F401
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
)

SRC_ROOT = Path(__file__).resolve().parents[5] / "src"
PERSISTENCE_ROOT = SRC_ROOT / "infrastructure" / "persistence"
MIGRATIONS_DIR = PERSISTENCE_ROOT / "migrations"
ALEMBIC_INI = PERSISTENCE_ROOT / "alembic.ini"


def _alembic_cfg(db_url: str) -> AlembicConfig:
    cfg = AlembicConfig(str(ALEMBIC_INI))
    cfg.set_main_option("script_location", str(MIGRATIONS_DIR))
    cfg.set_main_option("sqlalchemy.url", db_url)
    return cfg


class TestMigrationUpgrade:
    def test_upgrade_head_creates_all_eos_tables(self) -> None:
        engine = create_engine("sqlite:///:memory:")
        url = str(engine.url)

        # Alembic cannot use in-memory SQLite (separate connection), so use
        # a file-based approach via the engine directly for the connection.
        # Instead, use a temp file.
        import tempfile

        fd, path = tempfile.mkstemp(suffix=".sqlite3")
        import os

        os.close(fd)
        try:
            db_url = f"sqlite:///{path}"
            cfg = _alembic_cfg(db_url)
            command.upgrade(cfg, "head")

            eng = create_engine(db_url)
            inspector = inspect(eng)
            tables = set(inspector.get_table_names())

            expected = {
                "eos_concepts",
                "eos_decisions",
                "eos_diagnoses",
                "eos_digital_twins",
                "eos_evidence_records",
                "eos_hypotheses",
                "eos_learning_episodes",
                "eos_orchestrators",
                "eos_priorities",
                "eos_teaching_intentions",
                "eos_teaching_plans",
                "eos_teaching_strategies",
            }
            assert expected.issubset(tables)
            eng.dispose()
        finally:
            os.unlink(path)


class TestMigrationDowngrade:
    def test_downgrade_base_removes_all_eos_tables(self) -> None:
        import os
        import tempfile

        fd, path = tempfile.mkstemp(suffix=".sqlite3")
        os.close(fd)
        try:
            db_url = f"sqlite:///{path}"
            cfg = _alembic_cfg(db_url)
            command.upgrade(cfg, "head")
            command.downgrade(cfg, "base")

            eng = create_engine(db_url)
            inspector = inspect(eng)
            tables = set(inspector.get_table_names())
            eos_tables = {t for t in tables if t.startswith("eos_")}
            assert eos_tables == set(), f"Tables remain after downgrade: {eos_tables}"
            eng.dispose()
        finally:
            os.unlink(path)


class TestSchemaMatchesMetadata:
    def test_migrated_schema_matches_metadata_tables(self) -> None:
        import os
        import tempfile

        fd, path = tempfile.mkstemp(suffix=".sqlite3")
        os.close(fd)
        try:
            db_url = f"sqlite:///{path}"
            cfg = _alembic_cfg(db_url)
            command.upgrade(cfg, "head")

            eng = create_engine(db_url)
            inspector = inspect(eng)
            migrated_tables = {
                t for t in inspector.get_table_names() if t.startswith("eos_")
            }
            metadata_tables = set(metadata.tables.keys())
            assert migrated_tables == metadata_tables

            # Verify columns match for each table.
            for table_name in metadata_tables:
                migrated_cols = {
                    col["name"] for col in inspector.get_columns(table_name)
                }
                metadata_cols = {
                    col.name for col in metadata.tables[table_name].columns
                }
                assert migrated_cols == metadata_cols, (
                    f"{table_name} column mismatch: "
                    f"migrated={migrated_cols}, metadata={metadata_cols}"
                )

            eng.dispose()
        finally:
            os.unlink(path)


class TestMigrationFileIntegrity:
    def test_script_directory_has_single_head(self) -> None:
        sd = ScriptDirectory(str(MIGRATIONS_DIR))
        heads = sd.get_heads()
        assert len(heads) == 1, f"Expected single head, got {heads}"

    def test_initial_revision_exists(self) -> None:
        sd = ScriptDirectory(str(MIGRATIONS_DIR))
        assert sd.get_current_head() == "202607200001"

    def test_no_domain_imports_in_migration(self) -> None:
        """Migration files must not import domain or application modules."""
        import ast

        versions_dir = MIGRATIONS_DIR / "versions"
        for py_file in sorted(versions_dir.glob("*.py")):
            tree = ast.parse(py_file.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module:
                    assert not node.module.startswith("domain"), (
                        f"{py_file.name} imports domain module {node.module}"
                    )
                    assert not node.module.startswith("application"), (
                        f"{py_file.name} imports application module {node.module}"
                    )
