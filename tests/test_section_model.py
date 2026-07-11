"""Tests for the Section model and its Alembic migration.

Covers:
- Section model creation
- Curriculum <-> Section ORM relationships
- NOT-NULL constraints (title, curriculum_id)
- Optional-field defaults
- Migration success on a fresh database (table, columns, PK, FK, indexes)
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pytest
from sqlalchemy import inspect

# Project root (kwalitec/)
PROJECT_ROOT = Path(__file__).parent.parent
MIGRATIONS_DIR = PROJECT_ROOT / "migrations"


class TestSectionModel:
    """Tests for the Section SQLAlchemy model."""

    def test_create_section(self, db, curriculum):
        """A Section can be created with all fields populated."""
        from app.models.curriculum import Curriculum, Section

        c, _ = curriculum
        section = Section(
            curriculum_id=c.id,
            official_id="SEC-1",
            code="S1",
            title="Probability and Statistics",
            description="Foundational probability concepts.",
            exam_weight=0.25,
            display_order=1,
            estimated_hours=40.0,
            difficulty="Medium",
        )
        db.session.add(section)
        db.session.commit()

        assert section.id is not None
        assert section.curriculum_id == c.id
        assert section.official_id == "SEC-1"
        assert section.code == "S1"
        assert section.title == "Probability and Statistics"
        assert section.exam_weight == 0.25
        assert section.display_order == 1
        assert section.estimated_hours == 40.0
        assert section.difficulty == "Medium"
        assert section.created_at is not None
        assert "Section" in repr(section)

    def test_section_belongs_to_curriculum(self, db, curriculum):
        """A Section belongs to exactly one Curriculum."""
        from app.models.curriculum import Curriculum, Section

        c, _ = curriculum
        section = Section(curriculum_id=c.id, title="Section A", display_order=1)
        db.session.add(section)
        db.session.commit()

        db.session.refresh(section)
        assert section.curriculum is not None
        assert section.curriculum.id == c.id
        assert section in c.sections

    def test_curriculum_has_many_sections(self, db, curriculum):
        """A Curriculum has many Sections accessible via the relationship."""
        from app.models.curriculum import Curriculum, Section

        c, _ = curriculum
        s1 = Section(curriculum_id=c.id, title="S1", display_order=1)
        s2 = Section(curriculum_id=c.id, title="S2", display_order=2)
        db.session.add_all([s1, s2])
        db.session.commit()

        sections = (
            Section.query.filter_by(curriculum_id=c.id)
            .order_by(Section.display_order)
            .all()
        )
        assert len(sections) == 2
        assert c.sections == sections

    def test_section_title_required(self, db, curriculum):
        """A Section without a title must be rejected by the database."""
        from app.models.curriculum import Curriculum, Section

        c, _ = curriculum
        section = Section(curriculum_id=c.id, display_order=1)
        db.session.add(section)
        with pytest.raises(Exception):
            db.session.commit()
        db.session.rollback()

    def test_section_curriculum_id_required(self, db, ctx):
        """A Section without a curriculum_id must be rejected by the database."""
        from app.models.curriculum import Section

        section = Section(title="Orphan Section", display_order=1)
        db.session.add(section)
        with pytest.raises(Exception):
            db.session.commit()
        db.session.rollback()

    def test_section_optional_fields_default(self, db, curriculum):
        """Optional fields default to None and display_order defaults to 0."""
        from app.models.curriculum import Curriculum, Section

        c, _ = curriculum
        section = Section(curriculum_id=c.id, title="Minimal", display_order=0)
        db.session.add(section)
        db.session.commit()

        assert section.official_id is None
        assert section.code is None
        assert section.description is None
        assert section.exam_weight is None
        assert section.estimated_hours is None
        assert section.difficulty is None
        assert section.display_order == 0


class TestSectionMigration:
    """Verify the Alembic migration creates the sections table correctly."""

    def test_migration_creates_sections_table(self):
        """Running the migrations on a fresh DB creates the sections table."""
        from alembic import command
        from alembic.config import Config as AlembicConfig
        from app import config, create_app
        from app.extensions import db as _db

        db_fd, db_path = tempfile.mkstemp(suffix=".sqlite3")
        db_uri = f"sqlite:///{db_path}"

        os.environ["APP_ENV"] = "testing"
        os.environ["SECRET_KEY"] = "test-secret-key-for-testing-only"

        original_uri = config._database_uri
        original_cfg_uri = config.BaseConfig.SQLALCHEMY_DATABASE_URI
        config._database_uri = lambda: db_uri
        # Patch the config class so the app's engine is created against the
        # fresh temp database from the very start (avoids engine redirection
        # races where the default instance DB already has the sections table).
        config.BaseConfig.SQLALCHEMY_DATABASE_URI = db_uri

        try:
            app = create_app()

            with app.app_context():
                cfg = AlembicConfig()
                cfg.set_main_option("script_location", str(MIGRATIONS_DIR))
                cfg.set_main_option("sqlalchemy.url", db_uri)
                command.upgrade(cfg, "head")

                inspector = inspect(_db.engine)
                assert "sections" in inspector.get_table_names(), (
                    "sections table was not created by the migration"
                )

                columns = {col["name"] for col in inspector.get_columns("sections")}
                expected_columns = {
                    "id",
                    "curriculum_id",
                    "official_id",
                    "code",
                    "title",
                    "description",
                    "exam_weight",
                    "display_order",
                    "estimated_hours",
                    "difficulty",
                    "created_at",
                }
                assert expected_columns.issubset(columns), (
                    f"Missing columns: {expected_columns - columns}"
                )

                # Primary key
                pk = inspector.get_pk_constraint("sections")
                assert "id" in pk["constrained_columns"]

                # Foreign key back to curricula
                fks = inspector.get_foreign_keys("sections")
                fk_cols = {fk["constrained_columns"][0] for fk in fks}
                assert "curriculum_id" in fk_cols

                # Indexes created
                indexes = inspector.get_indexes("sections")
                indexed_cols = {
                    col for idx in indexes for col in idx["column_names"]
                }
                assert "curriculum_id" in indexed_cols
                assert "display_order" in indexed_cols
        finally:
            config._database_uri = original_uri
            config.BaseConfig.SQLALCHEMY_DATABASE_URI = original_cfg_uri
            os.close(db_fd)
            if os.path.exists(db_path):
                os.unlink(db_path)