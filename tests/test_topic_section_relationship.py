"""Tests for the Topic -> Section relationship (Milestone 1.6).

Covers:
- Topic creation with no Section (section_id remains NULL)
- Topic creation with a Section (section_id populated)
- ORM relationships (Section.topics, Topic.section)
- Migration success (column, FK, index added; no data migration)
- Existing Topics continue to function unchanged
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


class TestTopicSectionRelationship:
    """Tests for the Topic <-> Section ORM relationship."""

    def test_topic_without_section(self, db, curriculum):
        """A Topic can be created without a Section (section_id is None)."""
        from app.models.curriculum import Curriculum, Topic

        c, _ = curriculum
        topic = Topic(
            name="Probability",
            curriculum_id=c.id,
            order=1,
            recommended_minutes=60,
            active=True,
        )
        db.session.add(topic)
        db.session.commit()

        assert topic.id is not None
        assert topic.section_id is None
        assert topic.section is None

    def test_topic_with_section(self, db, curriculum):
        """A Topic can reference a Section via section_id."""
        from app.models.curriculum import Curriculum, Section, Topic

        c, _ = curriculum
        section = Section(curriculum_id=c.id, title="Section A", display_order=1)
        db.session.add(section)
        db.session.flush()

        topic = Topic(
            name="Probability",
            curriculum_id=c.id,
            order=1,
            recommended_minutes=60,
            active=True,
            section_id=section.id,
        )
        db.session.add(topic)
        db.session.commit()

        assert topic.section_id == section.id
        assert topic.section is not None
        assert topic.section.id == section.id

    def test_section_has_many_topics(self, db, curriculum):
        """A Section exposes its Topics via the relationship."""
        from app.models.curriculum import Curriculum, Section, Topic

        c, _ = curriculum
        section = Section(curriculum_id=c.id, title="Section A", display_order=1)
        db.session.add(section)
        db.session.flush()

        t1 = Topic(
            name="T1", curriculum_id=c.id, order=1,
            recommended_minutes=30, active=True, section_id=section.id,
        )
        t2 = Topic(
            name="T2", curriculum_id=c.id, order=2,
            recommended_minutes=30, active=True, section_id=section.id,
        )
        db.session.add_all([t1, t2])
        db.session.commit()

        db.session.refresh(section)
        assert len(section.topics) == 2
        assert t1 in section.topics
        assert t2 in section.topics

    def test_topic_belongs_to_section(self, db, curriculum):
        """A Topic's section attribute resolves to the owning Section."""
        from app.models.curriculum import Curriculum, Section, Topic

        c, _ = curriculum
        section = Section(curriculum_id=c.id, title="Section A", display_order=1)
        db.session.add(section)
        db.session.flush()

        topic = Topic(
            name="T1", curriculum_id=c.id, order=1,
            recommended_minutes=30, active=True, section_id=section.id,
        )
        db.session.add(topic)
        db.session.commit()

        db.session.refresh(topic)
        assert topic.section.id == section.id
        assert topic in section.topics

    def test_existing_topic_still_functions(self, db, curriculum):
        """Topics created the existing way (no section) keep working.

        The new nullable ``section_id`` column must not affect pre-existing
        topics: they remain queryable, their curriculum aggregation methods
        still work, and they carry no section reference.
        """
        from app.models.curriculum import Curriculum, Topic

        c, topics = curriculum
        assert len(topics) == 3

        # No topic references a section yet (backwards compatible)
        for topic in topics:
            assert topic.section_id is None
            assert topic.section is None

        # Existing behaviour: curriculum still aggregates topics
        assert c.get_root_topics()
        assert c.get_all_topics_ordered()

        # A topic created the old way (no section) persists correctly
        legacy = Topic(
            name="Legacy Topic",
            curriculum_id=c.id,
            order=99,
            recommended_minutes=45,
            active=True,
        )
        db.session.add(legacy)
        db.session.commit()

        reloaded = db.session.get(Topic, legacy.id)
        assert reloaded is not None
        assert reloaded.section_id is None
        assert reloaded.section is None
        assert reloaded.curriculum_id == c.id


class TestTopicSectionMigration:
    """Verify the Alembic migration adds section_id correctly."""

    def test_migration_adds_section_id(self):
        """Running the migrations on a fresh DB adds section_id to topics."""
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
        config.BaseConfig.SQLALCHEMY_DATABASE_URI = db_uri

        try:
            app = create_app()

            with app.app_context():
                cfg = AlembicConfig()
                cfg.set_main_option("script_location", str(MIGRATIONS_DIR))
                cfg.set_main_option("sqlalchemy.url", db_uri)
                command.upgrade(cfg, "head")

                inspector = inspect(_db.engine)

                # topics table exists with the new column
                assert "topics" in inspector.get_table_names()
                columns = {col["name"] for col in inspector.get_columns("topics")}
                assert "section_id" in columns

                # column is nullable (no data migration, backwards compatible)
                section_col = next(
                    col for col in inspector.get_columns("topics")
                    if col["name"] == "section_id"
                )
                assert section_col["nullable"] is True

                # foreign key to sections
                fks = inspector.get_foreign_keys("topics")
                fk_cols = {fk["constrained_columns"][0] for fk in fks}
                assert "section_id" in fk_cols

                # index created
                indexes = inspector.get_indexes("topics")
                indexed_cols = {
                    col for idx in indexes for col in idx["column_names"]
                }
                assert "section_id" in indexed_cols
        finally:
            config._database_uri = original_uri
            config.BaseConfig.SQLALCHEMY_DATABASE_URI = original_cfg_uri
            os.close(db_fd)
            if os.path.exists(db_path):
                os.unlink(db_path)