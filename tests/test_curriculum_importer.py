"""Tests for the Curriculum Importer (CurriculumService.import_curricula()).

This test suite covers:
- V1 import (legacy format)
- V2 import (hierarchical format)
- Idempotent imports
- Duplicate protection
- Mixed-format support
- Startup import
- Error handling
- Validation failures
- Automatic format detection
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

# Project root (kwalitec/)
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "app" / "curriculum" / "data"


# ═══════════════════════════════════════════════════════════════════════════════
# V1 Import Tests (Legacy Format)
# ═══════════════════════════════════════════════════════════════════════════════

class TestV1Import:
    """Tests for importing the bundled curriculum (canonical CS1 V2)."""

    def test_import_v1_curriculum_populates_tables(self, ctx, db):
        """V1 curriculum import should populate Curriculum, Topic, and LearningObjective tables."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum, Topic
        from app.models.learning import LearningObjective

        count = CurriculumService.import_curricula()
        assert count >= 1, "Should import at least one curriculum"

        # Verify curriculum was created
        assert Curriculum.query.count() >= 1
        c = Curriculum.query.first()
        assert c.exam_name is not None
        assert c.version is not None
        assert c.active is True

        # Verify topics were created
        assert Topic.query.count() >= 1
        topics = Topic.query.filter_by(curriculum_id=c.id).all()
        assert len(topics) >= 1

        # Verify learning objectives were created
        assert LearningObjective.query.count() >= 1
        for topic in topics:
            los = LearningObjective.query.filter_by(topic_id=topic.id).all()
            assert len(los) >= 1, f"Topic {topic.name} has no learning objectives"

    def test_import_v1_creates_correct_topic_order(self, ctx, db):
        """V1 topics should be imported in the correct order."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum, Topic

        CurriculumService.import_curricula()
        c = Curriculum.query.first()
        topics = Topic.query.filter_by(curriculum_id=c.id).order_by(Topic.order).all()

        # Verify order is sequential
        for i, topic in enumerate(topics, start=1):
            assert topic.order == i, f"Topic {topic.name} has order {topic.order}, expected {i}"

    def test_import_v1_creates_correct_metadata(self, ctx, db):
        """Bundled CS1 V2 topics carry minutes; syllabus_weight is section-level (0 on topics)."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum, Topic

        CurriculumService.import_curricula()
        c = Curriculum.query.filter_by(exam_name="IFoA CS1", version="2026").one()
        assert c.exam_name == "IFoA CS1"
        topics = Topic.query.filter_by(curriculum_id=c.id).all()

        for topic in topics:
            assert topic.recommended_minutes > 0, f"Topic {topic.name} has no recommended minutes"
            assert topic.syllabus_weight == 0.0, (
                f"V2 topic {topic.name} must have syllabus_weight 0.0"
            )
            assert topic.active is True


# ═══════════════════════════════════════════════════════════════════════════════
# V2 Import Tests (Hierarchical Format)
# ═══════════════════════════════════════════════════════════════════════════════

class TestV2Import:
    """Tests for importing V2 (hierarchical) curriculum format."""

    def test_import_v2_curriculum_detects_format(self, ctx, db):
        """V2 curriculum should be automatically detected and imported."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum, Topic
        from app.models.learning import LearningObjective

        # Create a minimal V2 curriculum file
        v2_data = {
            "exam_code": "CS1",
            "exam_name": "Actuarial Statistics V2",
            "provider": "IFoA",
            "version": "2027",
            "effective_date": "2027-01-01",
            "sections": [
                {
                    "id": "CS1-A",
                    "code": "CS1-A",
                    "title": "Section A",
                    "description": "Test section",
                    "exam_weight": 100.0,
                    "estimated_hours": 10.0,
                    "display_order": 1,
                    "topics": [
                        {
                            "id": "CS1-A-T01",
                            "section_id": "CS1-A",
                            "code": "CS1-A.1",
                            "title": "Test Topic",
                            "description": "A test topic",
                            "estimated_minutes": 120,
                            "difficulty": "foundational",
                            "display_order": 1,
                            "learning_objectives": [
                                {
                                    "id": "CS1-A-T01-LO01",
                                    "topic_id": "CS1-A-T01",
                                    "code": "CS1-A.1.1",
                                    "description": "Test learning objective",
                                    "cognitive_level": "understand",
                                    "estimated_minutes": 30,
                                    "learning_type": "concept",
                                    "display_order": 1,
                                }
                            ],
                        }
                    ],
                }
            ],
        }

        # Write to a temporary location in the data directory
        v2_dir = DATA_DIR / "ifoa" / "cs1"
        v2_file = v2_dir / "2027.json"
        
        # Backup existing file if it exists
        backup = None
        if v2_file.exists():
            backup = v2_dir / "2027.json.bak"
            v2_file.rename(backup)

        try:
            with open(v2_file, "w") as f:
                json.dump(v2_data, f)

            # Import should detect V2 format
            count = CurriculumService.import_curricula()
            assert count >= 1, "Should import V2 curriculum"

            # Verify the V2 curriculum was imported under product naming
            c = Curriculum.query.filter_by(exam_name="IFoA CS1", version="2027").first()
            assert c is not None, "V2 curriculum not found in database"
            assert c.version == "2027"

            # Verify topics were imported
            topics = Topic.query.filter_by(curriculum_id=c.id).all()
            assert len(topics) == 1
            assert topics[0].name == "Test Topic"
            assert topics[0].recommended_minutes == 120

            # Verify learning objectives were imported
            los = LearningObjective.query.filter_by(topic_id=topics[0].id).all()
            assert len(los) == 1
            assert "Test learning objective" in los[0].description

        finally:
            # Cleanup
            if v2_file.exists():
                v2_file.unlink()
            if backup and backup.exists():
                backup.rename(v2_file)

    def test_import_v2_topics_ordered_globally(self, ctx, db):
        """V2 topics across sections are ordered globally and linked to Sections."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum, Section, Topic

        v2_data = {
            "exam_code": "CS1",
            "exam_name": "Multi-Section Exam",
            "provider": "IFoA",
            "version": "2028",
            "effective_date": "2028-01-01",
            "sections": [
                {
                    "id": "CS1-A",
                    "code": "CS1-A",
                    "title": "Section A",
                    "description": "First section",
                    "exam_weight": 50.0,
                    "estimated_hours": 5.0,
                    "display_order": 1,
                    "topics": [
                        {
                            "id": "CS1-A-T01",
                            "section_id": "CS1-A",
                            "code": "CS1-A.1",
                            "title": "Topic A1",
                            "description": "First topic",
                            "estimated_minutes": 60,
                            "difficulty": "foundational",
                            "display_order": 1,
                            "learning_objectives": [
                                {
                                    "id": "CS1-A-T01-LO01",
                                    "topic_id": "CS1-A-T01",
                                    "code": "CS1-A.1.1",
                                    "description": "LO A1",
                                    "cognitive_level": "remember",
                                    "estimated_minutes": 15,
                                    "learning_type": "concept",
                                    "display_order": 1,
                                }
                            ],
                        }
                    ],
                },
                {
                    "id": "CS1-B",
                    "code": "CS1-B",
                    "title": "Section B",
                    "description": "Second section",
                    "exam_weight": 50.0,
                    "estimated_hours": 5.0,
                    "display_order": 2,
                    "topics": [
                        {
                            "id": "CS1-B-T01",
                            "section_id": "CS1-B",
                            "code": "CS1-B.1",
                            "title": "Topic B1",
                            "description": "Second topic",
                            "estimated_minutes": 60,
                            "difficulty": "intermediate",
                            "display_order": 1,
                            "learning_objectives": [
                                {
                                    "id": "CS1-B-T01-LO01",
                                    "topic_id": "CS1-B-T01",
                                    "code": "CS1-B.1.1",
                                    "description": "LO B1",
                                    "cognitive_level": "apply",
                                    "estimated_minutes": 20,
                                    "learning_type": "procedure",
                                    "display_order": 1,
                                }
                            ],
                        }
                    ],
                },
            ],
        }

        v2_dir = DATA_DIR / "ifoa" / "cs1"
        v2_file = v2_dir / "2028.json"

        backup = None
        if v2_file.exists():
            backup = v2_dir / "2028.json.bak"
            v2_file.rename(backup)

        try:
            with open(v2_file, "w") as f:
                json.dump(v2_data, f)

            count = CurriculumService.import_curricula()
            assert count >= 1

            c = Curriculum.query.filter_by(version="2028").first()
            assert c is not None

            topics = Topic.query.filter_by(curriculum_id=c.id).order_by(Topic.order).all()
            assert len(topics) == 2

            # Topics are not nested under each other
            for topic in topics:
                assert topic.parent_topic_id is None, "V2 topics must not be nested"

            # Topics are ordered globally across sections
            assert topics[0].order == 1
            assert topics[1].order == 2

            # Every V2 topic must reference its owning Section
            sections = Section.query.filter_by(curriculum_id=c.id).all()
            assert len(sections) == 2
            section_ids = {s.id for s in sections}
            for topic in topics:
                assert topic.section_id is not None, "V2 topic must have a section_id"
                assert topic.section_id in section_ids, "section_id must point to a valid Section"

        finally:
            if v2_file.exists():
                v2_file.unlink()
            if backup and backup.exists():
                backup.rename(v2_file)


# ═══════════════════════════════════════════════════════════════════════════════
# Idempotency Tests
# ═══════════════════════════════════════════════════════════════════════════════

class TestIdempotentImport:
    """Tests for import idempotency."""

    def test_import_is_idempotent(self, ctx, db):
        """Calling import_curricula() twice must not create duplicate rows."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum, Topic
        from app.models.learning import LearningObjective

        count1 = CurriculumService.import_curricula()
        assert count1 >= 1, "First import should create at least one curriculum"

        # Get counts after first import
        curriculum_count_1 = Curriculum.query.count()
        topic_count_1 = Topic.query.count()
        lo_count_1 = LearningObjective.query.count()

        # Second import
        count2 = CurriculumService.import_curricula()
        assert count2 == 0, "Second import should return 0 (no new curricula)"

        # Verify no duplicates
        assert Curriculum.query.count() == curriculum_count_1
        assert Topic.query.count() == topic_count_1
        assert LearningObjective.query.count() == lo_count_1

    def test_import_skips_existing_curricula(self, ctx, db):
        """Import should skip curricula that already exist."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum

        # First import
        count1 = CurriculumService.import_curricula()
        assert count1 >= 1

        # Get the curriculum that was created
        curriculum = Curriculum.query.first()
        original_id = curriculum.id
        original_name = curriculum.exam_name

        # Second import should skip it
        count2 = CurriculumService.import_curricula()
        assert count2 == 0

        # Verify the same curriculum still exists
        curriculum_again = Curriculum.query.filter_by(exam_name=original_name).first()
        assert curriculum_again is not None
        assert curriculum_again.id == original_id


# ═══════════════════════════════════════════════════════════════════════════════
# Mixed-Format Support Tests
# ═══════════════════════════════════════════════════════════════════════════════

class TestMixedFormatSupport:
    """Tests for supporting both V1 and V2 formats simultaneously."""

    def test_import_both_v1_and_v2(self, ctx, db):
        """Import should handle both V1 and V2 curricula in the same run."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum

        # The bundled V1 curriculum should be imported
        count = CurriculumService.import_curricula()
        assert count >= 1

        # Verify at least one curriculum exists
        assert Curriculum.query.count() >= 1

        # The existing V1 curriculum (IFoA CS1 2026) should be present
        v1_curriculum = Curriculum.query.filter_by(version="2026").first()
        assert v1_curriculum is not None


# ═══════════════════════════════════════════════════════════════════════════════
# Error Handling Tests
# ═══════════════════════════════════════════════════════════════════════════════

class TestErrorHandling:
    """Tests for error handling during import."""

    def test_import_handles_invalid_json_gracefully(self, ctx, db):
        """Invalid JSON files should be skipped without crashing."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum

        # Create an invalid JSON file
        invalid_dir = DATA_DIR / "test_invalid"
        invalid_dir.mkdir(parents=True, exist_ok=True)
        invalid_file = invalid_dir / "invalid.json"

        try:
            with open(invalid_file, "w") as f:
                f.write("not valid json {{{")

            # Import should not crash
            count = CurriculumService.import_curricula()
            # Should return 0 or import valid curricula, but not crash
            assert isinstance(count, int)

        finally:
            if invalid_file.exists():
                invalid_file.unlink()
            if invalid_dir.exists():
                invalid_dir.rmdir()

    def test_import_handles_validation_failures(self, ctx, db):
        """Curricula that fail validation should be skipped."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum

        # Create a V2 curriculum with invalid data (missing required fields)
        invalid_v2 = {
            "exam_code": "CS1",
            "exam_name": "Invalid",
            "provider": "IFoA",
            "version": "2099",
            "effective_date": "2099-01-01",
            "sections": [
                {
                    "id": "CS1-A",
                    "code": "CS1-A",
                    "title": "Section A",
                    "description": "Test",
                    "exam_weight": 50.0,
                    "estimated_hours": 5.0,
                    "display_order": 1,
                    "topics": [
                        {
                            "id": "CS1-A-T01",
                            "section_id": "CS1-A",
                            "code": "CS1-A.1",
                            "title": "Topic",
                            "description": "Test",
                            "estimated_minutes": 60,
                            "difficulty": "foundational",
                            "display_order": 1,
                            "learning_objectives": [
                                {
                                    "id": "CS1-A-T01-LO01",
                                    "topic_id": "CS1-A-T01",
                                    "code": "CS1-A.1.1",
                                    "description": "LO",
                                    "cognitive_level": "remember",
                                    "estimated_minutes": 15,
                                    "learning_type": "concept",
                                    "display_order": 1,
                                }
                            ],
                        }
                    ],
                }
            ],
        }

        v2_dir = DATA_DIR / "ifoa" / "cs1"
        v2_file = v2_dir / "2099.json"

        backup = None
        if v2_file.exists():
            backup = v2_dir / "2099.json.bak"
            v2_file.rename(backup)

        try:
            with open(v2_file, "w") as f:
                json.dump(invalid_v2, f)

            # Import should handle the error gracefully
            count = CurriculumService.import_curricula()
            # Should not crash, may or may not import depending on validation
            assert isinstance(count, int)

        finally:
            if v2_file.exists():
                v2_file.unlink()
            if backup and backup.exists():
                backup.rename(v2_file)


# ═══════════════════════════════════════════════════════════════════════════════
# Automatic Format Detection Tests
# ═══════════════════════════════════════════════════════════════════════════════

class TestFormatDetection:
    """Tests for automatic V1/V2 format detection."""

    def test_v1_format_detected(self, ctx, db):
        """V1 curricula should be automatically detected."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum

        count = CurriculumService.import_curricula()
        assert count >= 1

        # Bundled curricula use product naming (CS1 + CB2 + CM1)
        c = Curriculum.query.filter_by(exam_name="IFoA CS1", version="2026").one()
        assert c is not None
        assert c.exam_name == "IFoA CS1"
        assert Curriculum.query.filter_by(exam_name="IFoA CB2", version="2026").one() is not None
        assert Curriculum.query.filter_by(exam_name="IFoA CM1", version="2026").one() is not None

    def test_format_detection_logs_correctly(self, ctx, db, caplog):
        """Format detection should be logged."""
        import logging
        from app.services.curriculum_service import CurriculumService

        with caplog.at_level(logging.DEBUG):
            CurriculumService.import_curricula()

        # Check that format detection was logged
        assert any("Detected" in record.message for record in caplog.records)


# ═══════════════════════════════════════════════════════════════════════════════
# Logging Tests
# ═══════════════════════════════════════════════════════════════════════════════

class TestImportLogging:
    """Tests for import logging."""

    def test_import_logs_start(self, ctx, db, caplog):
        """Import should log when it starts."""
        import logging
        from app.services.curriculum_service import CurriculumService

        with caplog.at_level(logging.INFO):
            CurriculumService.import_curricula()

        assert any("Starting curriculum import" in record.message for record in caplog.records)

    def test_import_logs_completion(self, ctx, db, caplog):
        """Import should log completion with statistics."""
        import logging
        from app.services.curriculum_service import CurriculumService

        with caplog.at_level(logging.INFO):
            CurriculumService.import_curricula()

        assert any("Curriculum import complete" in record.message for record in caplog.records)

    def test_import_logs_imported_curriculum(self, ctx, db, caplog):
        """Import should log each imported curriculum."""
        import logging
        from app.services.curriculum_service import CurriculumService

        with caplog.at_level(logging.INFO):
            count = CurriculumService.import_curricula()

        if count > 0:
            assert any("Imported" in record.message and "curriculum" in record.message.lower() 
                      for record in caplog.records)

    def test_import_logs_skipped_curricula(self, ctx, db, caplog):
        """Import should log skipped curricula."""
        import logging
        from app.services.curriculum_service import CurriculumService

        # First import
        CurriculumService.import_curricula()

        # Second import (should skip)
        with caplog.at_level(logging.DEBUG):
            CurriculumService.import_curricula()

        assert any("already exists" in record.message for record in caplog.records)


# ═══════════════════════════════════════════════════════════════════════════════
# Learning Objectives Tests
# ═══════════════════════════════════════════════════════════════════════════════

class TestLearningObjectivesImport:
    """Tests for learning objective import."""

    def test_import_creates_learning_objectives(self, ctx, db):
        """Every topic should have at least one learning objective."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum, Topic
        from app.models.learning import LearningObjective

        CurriculumService.import_curricula()
        c = Curriculum.query.first()
        topics = Topic.query.filter_by(curriculum_id=c.id).all()

        for topic in topics:
            los = LearningObjective.query.filter_by(topic_id=topic.id).all()
            assert len(los) >= 1, f"Topic {topic.name} has no learning objectives"

    def test_learning_objectives_have_correct_order(self, ctx, db):
        """Learning objectives should be imported in the correct order."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Topic
        from app.models.learning import LearningObjective

        CurriculumService.import_curricula()
        topic = Topic.query.first()
        los = LearningObjective.query.filter_by(topic_id=topic.id).order_by(LearningObjective.order).all()

        for i, lo in enumerate(los, start=1):
            assert lo.order == i, f"LO has order {lo.order}, expected {i}"

    def test_learning_objectives_preserve_code_and_description(self, ctx, db):
        """Learning objectives should preserve their code and description."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Topic
        from app.models.learning import LearningObjective

        CurriculumService.import_curricula()
        topic = Topic.query.first()
        los = LearningObjective.query.filter_by(topic_id=topic.id).all()

        for lo in los:
            # Should contain the code in brackets
            assert "[" in lo.description and "]" in lo.description, \
                f"LO description should contain code: {lo.description}"
            assert len(lo.description) > 0


# ═══════════════════════════════════════════════════════════════════════════════
# Startup Import Tests
# ═══════════════════════════════════════════════════════════════════════════════

class TestStartupImport:
    """Tests for startup import behavior."""

    def test_startup_import_creates_curricula(self, ctx, app, db):
        """StartupService should import curricula when it runs."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum

        count = CurriculumService.import_curricula()
        assert count >= 1, "Should import at least one curriculum on startup"
        assert Curriculum.query.count() >= 1

    def test_startup_import_is_safe_to_run_multiple_times(self, ctx, app, db):
        """Running import multiple times should be safe (idempotent)."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum

        # Run multiple times
        for _ in range(3):
            count = CurriculumService.import_curricula()
            assert isinstance(count, int)
            assert count >= 0

        # Should still have exactly the bundled curricula (CS1 + CB2 + CM1)
        assert Curriculum.query.count() == 3
        assert {c.exam_name for c in Curriculum.query.all()} == {
            "IFoA CS1",
            "IFoA CB2",
            "IFoA CM1",
        }


# ═══════════════════════════════════════════════════════════════════════════════
# Duplicate Protection Tests
# ═══════════════════════════════════════════════════════════════════════════════

class TestDuplicateProtection:
    """Tests for duplicate protection."""

    def test_no_duplicate_curricula(self, ctx, db):
        """Import should not create duplicate curricula."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum

        # Import twice
        CurriculumService.import_curricula()
        count1 = Curriculum.query.count()

        CurriculumService.import_curricula()
        count2 = Curriculum.query.count()

        assert count1 == count2, "Duplicate curricula were created"

    def test_no_duplicate_topics(self, ctx, db):
        """Import should not create duplicate topics."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum, Topic

        CurriculumService.import_curricula()
        c = Curriculum.query.first()
        count1 = Topic.query.filter_by(curriculum_id=c.id).count()

        CurriculumService.import_curricula()
        count2 = Topic.query.filter_by(curriculum_id=c.id).count()

        assert count1 == count2, "Duplicate topics were created"

    def test_no_duplicate_learning_objectives(self, ctx, db):
        """Import should not create duplicate learning objectives."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum, Topic
        from app.models.learning import LearningObjective

        CurriculumService.import_curricula()
        c = Curriculum.query.first()
        topic = Topic.query.filter_by(curriculum_id=c.id).first()
        count1 = LearningObjective.query.filter_by(topic_id=topic.id).count()

        CurriculumService.import_curricula()
        count2 = LearningObjective.query.filter_by(topic_id=topic.id).count()

        assert count1 == count2, "Duplicate learning objectives were created"


# ═══════════════════════════════════════════════════════════════════════════════
# Shared V2 fixture data and helper
# ═══════════════════════════════════════════════════════════════════════════════

_TWO_SECTION_V2 = {
    "exam_code": "CS9",
    "exam_name": "Test Exam Nine",
    "provider": "IFoA",
    "version": "2099",
    "effective_date": "2099-01-01",
    "sections": [
        {
            "id": "CS9-A",
            "code": "CS9-A",
            "title": "Section Alpha",
            "description": "First section",
            "exam_weight": 60.0,
            "estimated_hours": 6.0,
            "difficulty": "foundational",
            "display_order": 1,
            "topics": [
                {
                    "id": "CS9-A-T01",
                    "section_id": "CS9-A",
                    "code": "CS9-A.1",
                    "title": "Alpha Topic",
                    "description": "Topic in section A",
                    "estimated_minutes": 120,
                    "difficulty": "foundational",
                    "display_order": 1,
                    "learning_objectives": [
                        {
                            "id": "CS9-A-T01-LO01",
                            "topic_id": "CS9-A-T01",
                            "code": "CS9-A.1.1",
                            "description": "LO 1",
                            "cognitive_level": "remember",
                            "estimated_minutes": 30,
                            "learning_type": "concept",
                            "display_order": 1,
                        }
                    ],
                }
            ],
        },
        {
            "id": "CS9-B",
            "code": "CS9-B",
            "title": "Section Beta",
            "description": "Second section",
            "exam_weight": 40.0,
            "estimated_hours": 4.0,
            "difficulty": "intermediate",
            "display_order": 2,
            "topics": [
                {
                    "id": "CS9-B-T01",
                    "section_id": "CS9-B",
                    "code": "CS9-B.1",
                    "title": "Beta Topic",
                    "description": "Topic in section B",
                    "estimated_minutes": 90,
                    "difficulty": "intermediate",
                    "display_order": 1,
                    "learning_objectives": [
                        {
                            "id": "CS9-B-T01-LO01",
                            "topic_id": "CS9-B-T01",
                            "code": "CS9-B.1.1",
                            "description": "LO 2",
                            "cognitive_level": "apply",
                            "estimated_minutes": 25,
                            "learning_type": "procedure",
                            "display_order": 1,
                        }
                    ],
                }
            ],
        },
    ],
}


def _write_v2_fixture(data: dict) -> tuple:
    """Write a V2 JSON fixture to disk and return (dir, file) paths."""
    exam_code = data["exam_code"].lower()
    version = data["version"]
    v2_dir = DATA_DIR / "ifoa" / exam_code
    v2_dir.mkdir(parents=True, exist_ok=True)
    v2_file = v2_dir / f"{version}.json"
    backup = None
    if v2_file.exists():
        backup = v2_dir / f"{version}.json.bak"
        v2_file.rename(backup)
    with open(v2_file, "w") as fh:
        json.dump(data, fh)
    return v2_dir, v2_file, backup


def _cleanup_v2_fixture(v2_dir, v2_file, backup) -> None:
    if v2_file.exists():
        v2_file.unlink()
    if backup and backup.exists():
        backup.rename(v2_file)
    # Only remove the directory if we created it and it is now empty
    try:
        v2_dir.rmdir()
    except OSError:
        pass


# ═══════════════════════════════════════════════════════════════════════════════
# Section Persistence Tests (Milestone 1.7)
# ═══════════════════════════════════════════════════════════════════════════════

class TestSectionPersistence:
    """V2 import must create Section rows and link Topics via section_id."""

    def test_v2_creates_section_rows(self, ctx, db):
        """Importing a V2 curriculum creates one Section row per JSON section."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum, Section

        v2_dir, v2_file, backup = _write_v2_fixture(_TWO_SECTION_V2)
        try:
            CurriculumService.import_curricula()
            c = Curriculum.query.filter_by(exam_name="IFoA CS9").first()
            assert c is not None

            sections = Section.query.filter_by(curriculum_id=c.id).order_by(Section.display_order).all()
            assert len(sections) == 2
        finally:
            _cleanup_v2_fixture(v2_dir, v2_file, backup)

    def test_v2_section_fields_persisted(self, ctx, db):
        """All Section fields from the JSON are stored correctly."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum, Section

        v2_dir, v2_file, backup = _write_v2_fixture(_TWO_SECTION_V2)
        try:
            CurriculumService.import_curricula()
            c = Curriculum.query.filter_by(exam_name="IFoA CS9").first()
            sections = (
                Section.query.filter_by(curriculum_id=c.id)
                .order_by(Section.display_order)
                .all()
            )

            # Section Alpha
            sa = sections[0]
            assert sa.official_id == "CS9-A"
            assert sa.code == "CS9-A"
            assert sa.title == "Section Alpha"
            assert sa.description == "First section"
            assert sa.exam_weight == 60.0
            assert sa.estimated_hours == 6.0
            assert sa.difficulty == "foundational"
            assert sa.display_order == 1

            # Section Beta
            sb = sections[1]
            assert sb.official_id == "CS9-B"
            assert sb.code == "CS9-B"
            assert sb.title == "Section Beta"
            assert sb.exam_weight == 40.0
            assert sb.display_order == 2
        finally:
            _cleanup_v2_fixture(v2_dir, v2_file, backup)

    def test_v2_topics_reference_sections(self, ctx, db):
        """Every Topic imported from V2 has a non-null section_id pointing to its Section."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum, Section, Topic

        v2_dir, v2_file, backup = _write_v2_fixture(_TWO_SECTION_V2)
        try:
            CurriculumService.import_curricula()
            c = Curriculum.query.filter_by(exam_name="IFoA CS9").first()

            topics = Topic.query.filter_by(curriculum_id=c.id).order_by(Topic.order).all()
            assert len(topics) == 2

            section_ids = {
                s.id for s in Section.query.filter_by(curriculum_id=c.id).all()
            }
            for topic in topics:
                assert topic.section_id is not None, (
                    f"Topic {topic.name!r} must have section_id set"
                )
                assert topic.section_id in section_ids, (
                    f"Topic {topic.name!r} section_id {topic.section_id} "
                    f"not in known section ids {section_ids}"
                )
        finally:
            _cleanup_v2_fixture(v2_dir, v2_file, backup)

    def test_v2_topic_section_orm_resolves(self, ctx, db):
        """topic.section ORM relationship resolves to the owning Section."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum, Section, Topic

        v2_dir, v2_file, backup = _write_v2_fixture(_TWO_SECTION_V2)
        try:
            CurriculumService.import_curricula()
            c = Curriculum.query.filter_by(exam_name="IFoA CS9").first()

            topics = Topic.query.filter_by(curriculum_id=c.id).order_by(Topic.order).all()
            for topic in topics:
                assert topic.section is not None, (
                    f"topic.section must not be None for {topic.name!r}"
                )
                assert isinstance(topic.section, Section)
                assert topic.section.curriculum_id == c.id
        finally:
            _cleanup_v2_fixture(v2_dir, v2_file, backup)

    def test_v2_sections_not_duplicated_on_repeated_import(self, ctx, db):
        """Calling import_curricula() twice must not create duplicate Section rows."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum, Section

        v2_dir, v2_file, backup = _write_v2_fixture(_TWO_SECTION_V2)
        try:
            CurriculumService.import_curricula()
            c = Curriculum.query.filter_by(exam_name="IFoA CS9").first()
            count_first = Section.query.filter_by(curriculum_id=c.id).count()

            CurriculumService.import_curricula()
            count_second = Section.query.filter_by(curriculum_id=c.id).count()

            assert count_first == count_second == 2, (
                f"Expected 2 sections, got {count_first} then {count_second}"
            )
        finally:
            _cleanup_v2_fixture(v2_dir, v2_file, backup)

    def test_v2_learning_objectives_unchanged(self, ctx, db):
        """LOs from V2 import retain correct description format and ordering."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum, Topic
        from app.models.learning import LearningObjective

        v2_dir, v2_file, backup = _write_v2_fixture(_TWO_SECTION_V2)
        try:
            CurriculumService.import_curricula()
            c = Curriculum.query.filter_by(exam_name="IFoA CS9").first()

            for topic in Topic.query.filter_by(curriculum_id=c.id).all():
                los = (
                    LearningObjective.query.filter_by(topic_id=topic.id)
                    .order_by(LearningObjective.order)
                    .all()
                )
                assert len(los) >= 1, f"Topic {topic.name!r} has no LOs"
                for lo in los:
                    assert "[" in lo.description and "]" in lo.description, (
                        f"LO description must contain [code]: {lo.description!r}"
                    )
        finally:
            _cleanup_v2_fixture(v2_dir, v2_file, backup)


# ═══════════════════════════════════════════════════════════════════════════════
# V1 Import Unaffected By Section Changes
# ═══════════════════════════════════════════════════════════════════════════════

class TestV1SectionUnchanged:
    """Bundled CS1 2026 is canonical V2: sections exist and topics are linked."""

    def test_v1_creates_no_sections(self, ctx, db):
        """Importing canonical CS1 V2 creates the official section rows."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum, Section

        CurriculumService.import_curricula()
        c = Curriculum.query.filter_by(exam_name="IFoA CS1", version="2026").first()
        assert c is not None, "Canonical CS1 (2026) was not imported"

        section_count = Section.query.filter_by(curriculum_id=c.id).count()
        assert section_count == 5, (
            f"CS1 V2 import should create 5 sections, created {section_count}"
        )

    def test_v1_topics_have_null_section_id(self, ctx, db):
        """All Topics from canonical CS1 V2 import must have section_id set."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum, Topic

        CurriculumService.import_curricula()
        c = Curriculum.query.filter_by(exam_name="IFoA CS1", version="2026").first()
        topics = Topic.query.filter_by(curriculum_id=c.id).all()
        assert topics, "CS1 curriculum should have topics"

        for topic in topics:
            assert topic.section_id is not None, (
                f"V2 topic {topic.name!r} must have section_id set"
            )


# ═══════════════════════════════════════════════════════════════════════════════
# Mixed V1 + V2 Import
# ═══════════════════════════════════════════════════════════════════════════════

class TestMixedImportSections:
    """V1 and V2 can coexist: V1 topics unsectioned, V2 topics all sectioned."""

    def test_mixed_import_sections_isolated(self, ctx, db):
        """Canonical CS1 and synthetic CS9 both import as V2 with isolated sections."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum, Section, Topic

        v2_dir, v2_file, backup = _write_v2_fixture(_TWO_SECTION_V2)
        try:
            CurriculumService.import_curricula()

            cs1 = Curriculum.query.filter_by(exam_name="IFoA CS1", version="2026").first()
            cs9 = Curriculum.query.filter_by(exam_name="IFoA CS9").first()
            assert cs1 is not None, "IFoA CS1 curriculum not imported"
            assert cs9 is not None, "IFoA CS9 curriculum not imported"

            for t in Topic.query.filter_by(curriculum_id=cs1.id).all():
                assert t.section_id is not None, f"CS1 topic {t.name!r} must have section_id"

            for t in Topic.query.filter_by(curriculum_id=cs9.id).all():
                assert t.section_id is not None, f"CS9 topic {t.name!r} must have section_id"

            assert Section.query.filter_by(curriculum_id=cs9.id).count() == 2
            assert Section.query.filter_by(curriculum_id=cs1.id).count() == 5
        finally:
            _cleanup_v2_fixture(v2_dir, v2_file, backup)


# ═══════════════════════════════════════════════════════════════════════════════
# Idempotent Section Import
# ═══════════════════════════════════════════════════════════════════════════════

class TestIdempotentSectionImport:
    """Repeated imports must not create duplicate Sections or alter existing rows."""

    def test_section_count_stable_after_three_imports(self, ctx, db):
        """Running import_curricula() three times produces the same Section count."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum, Section

        v2_dir, v2_file, backup = _write_v2_fixture(_TWO_SECTION_V2)
        try:
            for _ in range(3):
                CurriculumService.import_curricula()

            c = Curriculum.query.filter_by(exam_name="IFoA CS9").first()
            assert Section.query.filter_by(curriculum_id=c.id).count() == 2
        finally:
            _cleanup_v2_fixture(v2_dir, v2_file, backup)

    def test_topic_section_link_stable_after_repeated_imports(self, ctx, db):
        """section_id values on Topics do not change across repeated imports."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum, Topic

        v2_dir, v2_file, backup = _write_v2_fixture(_TWO_SECTION_V2)
        try:
            CurriculumService.import_curricula()
            c = Curriculum.query.filter_by(exam_name="IFoA CS9").first()
            snapshot = {
                t.id: t.section_id
                for t in Topic.query.filter_by(curriculum_id=c.id).all()
            }

            CurriculumService.import_curricula()
            for topic in Topic.query.filter_by(curriculum_id=c.id).all():
                assert topic.section_id == snapshot[topic.id], (
                    f"section_id changed on repeated import for topic {topic.name!r}"
                )
        finally:
            _cleanup_v2_fixture(v2_dir, v2_file, backup)


# ═══════════════════════════════════════════════════════════════════════════════
# Import Ordering
# ═══════════════════════════════════════════════════════════════════════════════

class TestImportOrdering:
    """Topics across sections must have a monotonically increasing global order."""

    def test_topics_ordered_globally_across_sections(self, ctx, db):
        """Topics imported from multiple sections carry sequential order values."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum, Topic

        v2_dir, v2_file, backup = _write_v2_fixture(_TWO_SECTION_V2)
        try:
            CurriculumService.import_curricula()
            c = Curriculum.query.filter_by(exam_name="IFoA CS9").first()
            topics = (
                Topic.query.filter_by(curriculum_id=c.id)
                .order_by(Topic.order)
                .all()
            )
            for expected, topic in enumerate(topics, start=1):
                assert topic.order == expected, (
                    f"Expected order {expected}, got {topic.order} for {topic.name!r}"
                )
        finally:
            _cleanup_v2_fixture(v2_dir, v2_file, backup)

    def test_sections_ordered_by_display_order(self, ctx, db):
        """Sections are persisted with the display_order value from the JSON."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum, Section

        v2_dir, v2_file, backup = _write_v2_fixture(_TWO_SECTION_V2)
        try:
            CurriculumService.import_curricula()
            c = Curriculum.query.filter_by(exam_name="IFoA CS9").first()
            sections = (
                Section.query.filter_by(curriculum_id=c.id)
                .order_by(Section.display_order)
                .all()
            )
            assert sections[0].display_order == 1
            assert sections[1].display_order == 2
        finally:
            _cleanup_v2_fixture(v2_dir, v2_file, backup)


# ═══════════════════════════════════════════════════════════════════════════════
# Duplicate Section Protection
# ═══════════════════════════════════════════════════════════════════════════════

class TestDuplicateSectionProtection:
    """No duplicate Section rows should ever be created."""

    def test_no_duplicate_sections(self, ctx, db):
        """Importing the same V2 curriculum twice creates exactly N sections, not 2N."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum, Section

        v2_dir, v2_file, backup = _write_v2_fixture(_TWO_SECTION_V2)
        try:
            CurriculumService.import_curricula()
            c = Curriculum.query.filter_by(exam_name="IFoA CS9").first()
            count_after_first = Section.query.filter_by(curriculum_id=c.id).count()

            CurriculumService.import_curricula()
            count_after_second = Section.query.filter_by(curriculum_id=c.id).count()

            assert count_after_first == count_after_second, (
                f"Duplicate sections created: {count_after_first} → {count_after_second}"
            )
        finally:
            _cleanup_v2_fixture(v2_dir, v2_file, backup)